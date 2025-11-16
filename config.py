"""
요기요 입점 여부 조회 매크로 - 설정 파일
모든 셀렉터와 설정값을 여기서 관리
"""
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 요기요 URL
YOGIYO_URL = os.getenv(
    'YOGIYO_URL',
    'https://ceo.yogiyo.co.kr/join-request?event_type=ad&utm_source=yogiyo&utm_medium=portal&utm_campaign=partner&utm_content=up_btn'
)

# 셀렉터 우선순위 (우선순위 1 → 2 → 3 순으로 시도)
INPUT_SELECTORS = [
    'input[name="company_number"][placeholder="입력해 주세요"]',  # Primary
    'input.sc-hAZoDl.fdtDAM.sc-dIouRR.dGckYu',                 # Backup 1
    'div.sc-fnykZs.lgUEyv input[type="text"]'                  # Backup 2
]

BUTTON_SELECTORS = [
    'div.sc-dkzDqf.jUa-DCf[size="48"][color="accent100"]',     # Primary
    'div.sc-dkzDqf.jUa-DCf',                                   # Backup 1
    'button[type="button"]'                                     # Backup 2
]

MESSAGE_SELECTORS = [
    'div.sc-hHLeRK.gpWodO',                                    # Primary
    'div.sc-hHLeRK',                                           # Backup 1
    'div[class*="sc-hHLeRK"]'                                  # Backup 2
]

# 스프레드시트 열 위치
COLUMN_BUSINESS_NUMBER = os.getenv('COLUMN_BUSINESS_NUMBER', 'E')  # 사업자번호 입력 열
COLUMN_RESULT = os.getenv('COLUMN_RESULT', 'W')                    # 결과 출력 열

# 대기 시간 (초)
PAGE_LOAD_WAIT = float(os.getenv('PAGE_LOAD_WAIT', '5'))     # 초기 페이지 로드 대기
BUTTON_CLICK_WAIT = float(os.getenv('BUTTON_CLICK_WAIT', '3'))  # 버튼 클릭 후 대기
SEARCH_DELAY = float(os.getenv('SEARCH_DELAY', '1.0'))       # 조회 간 딜레이

# 옵션
SKIP_EXISTING = os.getenv('SKIP_EXISTING', 'false').lower() == 'true'
RESULT_FORMAT = os.getenv('RESULT_FORMAT', 'MESSAGE')  # MESSAGE or CODE
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'false').lower() == 'true'

# 재시도 설정
MAX_RETRIES = 3                    # 셀렉터 탐색 실패 시 재시도 횟수
API_MAX_RETRIES = 5                # Google API 호출 실패 시 재시도 횟수
RETRY_DELAY = 1                    # 재시도 간 대기 시간 (초)

# 메시지 분류
MESSAGE_PATTERNS = {
    'REGISTERED': '이미 등록된 사업자번호입니다',
    'AVAILABLE': '입점신청 가능한 사업자번호입니다',
    'INVALID': '사업자 번호를 확인해 주세요'
}
