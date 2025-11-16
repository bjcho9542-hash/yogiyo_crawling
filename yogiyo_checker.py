"""
요기요 입점 여부 조회 크롤링 로직
"""
import time
import random
import re
from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

import config


class YogiyoChecker:
    """요기요 입점 여부 조회 클래스"""

    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_browser()

    def setup_browser(self):
        """Chrome 브라우저 설정 및 실행"""
        chrome_options = Options()

        # 기본 옵션
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1400,900')

        # 봇 감지 우회
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # User-Agent 설정 (실제 사용자처럼)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # Chrome 로그 억제
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Headless 모드 (옵션)
        if config.HEADLESS_MODE:
            chrome_options.add_argument('--headless')

        # ChromeDriver 자동 관리
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        print("[OK] Chrome 브라우저 실행 완료")

    def safe_find_element(self, selectors: list, element_name: str):
        """
        여러 셀렉터를 순차적으로 시도하여 요소 찾기

        Args:
            selectors: CSS 셀렉터 리스트 (우선순위 순)
            element_name: 요소 이름 (로그용)

        Returns:
            찾은 WebElement 또는 None
        """
        for i, selector in enumerate(selectors):
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                print(f"[INFO] {element_name} found with selector {i+1}")
                return element
            except NoSuchElementException:
                print(f"[DEBUG] Selector {i+1} failed for {element_name}")
                continue

        raise Exception(f"All selectors failed for {element_name}")

    def check_business_number(self, business_number: str) -> Tuple[str, str]:
        """
        사업자번호 조회

        Args:
            business_number: 10자리 사업자번호

        Returns:
            (상태 코드, 메시지 텍스트) 튜플
            상태 코드: REGISTERED, AVAILABLE, INVALID, UNKNOWN
        """
        try:
            # 요기요 페이지 접속 (첫 실행 시)
            if self.driver.current_url != config.YOGIYO_URL:
                print(f"[INFO] 요기요 페이지 접속 중...")
                self.driver.get(config.YOGIYO_URL)
                time.sleep(config.PAGE_LOAD_WAIT)
                print("[OK] 페이지 로드 완료")

            # 1. 사업자번호 입력 필드 찾기
            input_field = self.safe_find_element(
                config.INPUT_SELECTORS,
                "사업자번호 입력 필드"
            )

            # 기존 값 지우고 새 값 입력
            input_field.clear()
            input_field.send_keys(business_number)
            print(f"[INFO] 사업자번호 입력 완료: {business_number}")

            # 2. 조회 버튼 찾기 및 클릭
            button = self.safe_find_element(
                config.BUTTON_SELECTORS,
                "조회 버튼"
            )
            button.click()
            print("[INFO] 조회 버튼 클릭")

            # 3. 결과 로딩 대기
            time.sleep(config.BUTTON_CLICK_WAIT)

            # 4. 결과 메시지 추출
            message_element = self.safe_find_element(
                config.MESSAGE_SELECTORS,
                "결과 메시지 영역"
            )
            message_text = message_element.text.strip()
            print(f"[INFO] 결과 메시지: {message_text}")

            # 5. 메시지 분류
            status, message = self.classify_message(message_text)

            return status, message

        except Exception as e:
            print(f"[ERROR] 조회 실패: {e}")
            raise

    def classify_message(self, message_text: str) -> Tuple[str, str]:
        """
        메시지 텍스트를 상태 코드로 분류

        Args:
            message_text: 결과 메시지 텍스트

        Returns:
            (상태 코드, 원문 메시지) 튜플
        """
        message = message_text.strip()

        # 패턴 매칭
        if config.MESSAGE_PATTERNS['REGISTERED'] in message:
            return 'REGISTERED', message
        elif config.MESSAGE_PATTERNS['AVAILABLE'] in message:
            return 'AVAILABLE', message
        elif config.MESSAGE_PATTERNS['INVALID'] in message:
            return 'INVALID', message
        else:
            # 예상치 못한 메시지
            print(f"[WARNING] Unknown message detected: {message}")
            return 'UNKNOWN', message

    def close(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            print("[INFO] 브라우저 종료")


def test_single_business_number():
    """단일 사업자번호 테스트"""
    print("=" * 80)
    print("요기요 입점 여부 조회 PoC 테스트")
    print("=" * 80)

    # 테스트할 사업자번호 (실제 번호로 대체 필요)
    test_numbers = [
        "1234567890",  # 테스트 번호 1
        "9876543210",  # 테스트 번호 2
        "123456789"    # 형식 오류 (9자리)
    ]

    checker = YogiyoChecker()

    try:
        for biz_num in test_numbers:
            print(f"\n[TEST] 사업자번호: {biz_num}")
            print("-" * 80)

            # 형식 검증
            if not re.match(r'^\d{10}$', biz_num):
                print(f"[WARNING] Invalid format ({biz_num}), proceeding anyway")

            # 조회 실행
            status, message = checker.check_business_number(biz_num)

            print(f"[RESULT] 상태: {status}")
            print(f"[RESULT] 메시지: {message}")

            # 딜레이 (차단 방지)
            delay = random.uniform(0.5, 1.0)
            print(f"[DELAY] {delay:.2f}초 대기...")
            time.sleep(delay)

    finally:
        checker.close()

    print("\n" + "=" * 80)
    print("테스트 완료")
    print("=" * 80)


if __name__ == '__main__':
    test_single_business_number()
