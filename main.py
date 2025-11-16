"""
요기요 입점 여부 조회 매크로 - 메인 프로그램
"""
import time
import random
import re
from datetime import datetime
from typing import List, Tuple

from google_sheets_client import GoogleSheetsClient
from yogiyo_checker import YogiyoChecker
import config


class Statistics:
    """통계 정보 관리"""
    def __init__(self):
        self.total = 0
        self.processed = 0
        self.success = 0
        self.failed = 0
        self.skipped = 0
        self.available = 0
        self.registered = 0
        self.invalid = 0
        self.unknown = 0
        self.error_rows = []
        self.start_time = None
        self.end_time = None

    def update(self, status: str, row: int = None, is_error: bool = False):
        """통계 업데이트"""
        if is_error and row:
            self.error_rows.append(row)
            self.failed += 1
        elif status == 'AVAILABLE':
            self.available += 1
            self.success += 1
        elif status == 'REGISTERED':
            self.registered += 1
            self.success += 1
        elif status == 'INVALID':
            self.invalid += 1
            self.success += 1
        elif status == 'UNKNOWN':
            self.unknown += 1
            self.success += 1

        self.processed += 1

    def skip(self):
        """스킵 카운트 증가"""
        self.skipped += 1

    def start(self):
        """시작 시간 기록"""
        self.start_time = datetime.now()

    def end(self):
        """종료 시간 기록"""
        self.end_time = datetime.now()

    def get_duration(self) -> str:
        """소요 시간 계산"""
        if not self.start_time or not self.end_time:
            return "알 수 없음"

        duration = self.end_time - self.start_time
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)

        return f"{minutes}분 {seconds}초"

    def get_avg_time(self) -> str:
        """평균 처리 시간 계산"""
        if not self.start_time or not self.end_time or self.processed == 0:
            return "알 수 없음"

        duration = self.end_time - self.start_time
        avg = duration.total_seconds() / self.processed

        return f"{avg:.2f}초/건"


def print_header():
    """프로그램 헤더 출력"""
    print("=" * 80)
    print("요기요 입점 여부 사업자번호 조회 매크로 v1.0")
    print("=" * 80)
    print()


def extract_sheet_id(url_or_id: str) -> str:
    """
    URL 또는 ID에서 Sheet ID 추출

    Args:
        url_or_id: 전체 URL 또는 Sheet ID

    Returns:
        추출된 Sheet ID
    """
    # URL에서 ID 추출 패턴: /d/{SHEET_ID}/
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url_or_id)
    if match:
        return match.group(1)

    # URL이 아니면 그대로 반환 (이미 ID인 경우)
    return url_or_id


def get_user_input() -> Tuple[str, int, int]:
    """
    사용자 입력 받기

    Returns:
        (sheet_id, start_row, end_row) 튜플
    """
    # Sheet URL 입력
    sheet_url = input("조회할 Google 스프레드시트 URL 전체를 입력하세요:\n> ").strip()

    if not sheet_url:
        raise ValueError("스프레드시트 URL이 비어있습니다!")

    # URL에서 ID 추출
    sheet_id = extract_sheet_id(sheet_url)
    print(f"[INFO] Sheet ID: {sheet_id}")

    # 시작 행 입력
    start_input = input("\n시작 행 (기본값 2):\n> ").strip()
    start_row = int(start_input) if start_input else 2

    # 종료 행 입력
    end_input = input("\n종료 행 (0=끝까지):\n> ").strip()
    end_row = int(end_input) if end_input else 0

    return sheet_id, start_row, end_row


def print_warning():
    """경고 메시지 출력"""
    print()
    print("⚠️  스프레드시트를 \"링크가 있는 모든 사용자 - 편집자\"로 공유하세요!")
    print("   1. 스프레드시트 우측 상단 \"공유\" 버튼 클릭")
    print("   2. \"일반 액세스\" → \"링크가 있는 모든 사용자\" 선택")
    print("   3. 권한: \"편집자\" 선택")
    print("   4. \"완료\" 클릭")
    print()


def process_row(
    checker: YogiyoChecker,
    sheets_client: GoogleSheetsClient,
    row_idx: int,
    business_number: str,
    existing_result: str,
    stats: Statistics
) -> bool:
    """
    한 행 처리

    Returns:
        성공 여부
    """
    # 빈 사업자번호 스킵
    if not business_number or business_number.strip() == "":
        print(f"  [SKIP] 빈 사업자번호")
        stats.skip()
        return False

    # 이미 결과가 있는 행 스킵 (옵션)
    if config.SKIP_EXISTING and existing_result and existing_result.strip():
        print(f"  [SKIP] 이미 처리됨: {existing_result[:30]}...")
        stats.skip()
        return False

    # 형식 검증
    if not re.match(r'^\d{10}$', business_number):
        print(f"  [WARNING] Invalid format ({business_number}), proceeding anyway")

    # 재시도 로직
    retry_count = 0
    max_retries = config.MAX_RETRIES

    while retry_count < max_retries:
        try:
            # 조회 실행
            print(f"  → 입력 완료")
            status, message = checker.check_business_number(business_number)

            print(f"  → 조회 버튼 클릭")
            print(f"  → 결과: \"{message}\"")

            # W열에 결과 저장
            result_value = message if config.RESULT_FORMAT == 'MESSAGE' else status
            sheets_client.write_cell(row_idx, config.COLUMN_RESULT, result_value)
            print(f"  → {config.COLUMN_RESULT}{row_idx} 저장 완료")

            # 통계 업데이트
            stats.update(status)

            print(f"  ✓ [SUCCESS] Row {row_idx} processed")
            return True

        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                print(f"  [ERROR] Row {row_idx}: Max retries exceeded - {e}")
                stats.update('ERROR', row_idx, is_error=True)
                return False

            print(f"  [RETRY] Attempt {retry_count} failed, retrying...")
            time.sleep(config.RETRY_DELAY)

    return False


def print_progress(current: int, total: int, stats: Statistics):
    """진행률 출력"""
    percentage = (current / total * 100) if total > 0 else 0
    print()
    print(f"Progress: {current}/{total} ({percentage:.1f}%)")
    print(f"Processed: {stats.processed} | Success: {stats.success} | Failed: {stats.failed} | Skipped: {stats.skipped}")
    print(f"Available: {stats.available} | Registered: {stats.registered} | Invalid: {stats.invalid}")
    print()


def print_summary(stats: Statistics):
    """최종 요약 출력"""
    print()
    print("=" * 80)
    print("처리 완료!")
    print("=" * 80)
    print(f"총 처리 행: {stats.total}")
    print(f"  - 성공: {stats.success}")
    print(f"  - 실패: {stats.failed}")
    print(f"  - 스킵: {stats.skipped}")
    print()
    print("상태별 집계:")
    print(f"  - 입점 가능 (AVAILABLE): {stats.available}")
    print(f"  - 이미 입점 (REGISTERED): {stats.registered}")
    print(f"  - 번호 오류 (INVALID): {stats.invalid}")
    print(f"  - 알 수 없음 (UNKNOWN): {stats.unknown}")
    print()

    if stats.error_rows:
        print(f"에러 발생 행: {stats.error_rows[:10]}")
        if len(stats.error_rows) > 10:
            print(f"  ... 외 {len(stats.error_rows) - 10}개")
    else:
        print("에러 발생 행: 없음")

    print()
    print(f"총 소요 시간: {stats.get_duration()}")
    if stats.processed > 0:
        print(f"평균 처리 시간: {stats.get_avg_time()}")
    print("=" * 80)


def main():
    """메인 함수"""
    # 헤더 출력
    print_header()

    # 사용자 입력
    try:
        sheet_id, start_row, end_row = get_user_input()
    except Exception as e:
        print(f"[ERROR] 입력 오류: {e}")
        return

    # 경고 메시지
    print_warning()

    # 통계 객체 생성
    stats = Statistics()
    stats.start()

    # Google Sheets 클라이언트 생성
    sheets_client = None
    checker = None

    try:
        print("[INFO] Google Sheets API 연결 중...")
        sheets_client = GoogleSheetsClient(sheet_id)

        # E열 데이터 읽기
        print(f"[INFO] {config.COLUMN_BUSINESS_NUMBER}열 데이터 읽기 중...")
        business_numbers = sheets_client.read_column(config.COLUMN_BUSINESS_NUMBER)

        # W열 데이터 읽기 (기존 결과 확인용)
        print(f"[INFO] {config.COLUMN_RESULT}열 데이터 읽기 중...")
        existing_results = sheets_client.read_column(config.COLUMN_RESULT)

        # 종료 행 설정
        if end_row == 0 or end_row > len(business_numbers):
            end_row = len(business_numbers)

        # 통계 초기화
        stats.total = end_row - start_row + 1

        print()
        print(f"[INFO] 처리 범위: {start_row}행 ~ {end_row}행 (총 {stats.total}개)")
        print()

        # Chrome 브라우저 실행
        print("[INFO] Chrome 브라우저 실행 중...")
        checker = YogiyoChecker()

        print()
        print("=" * 80)
        print("조회 시작")
        print("=" * 80)
        print()

        # 각 행 처리
        for row_idx in range(start_row, end_row + 1):
            # 인덱스 조정 (리스트는 0부터 시작)
            list_idx = row_idx - 1

            # 데이터 가져오기
            business_number = business_numbers[list_idx] if list_idx < len(business_numbers) else ''
            existing_result = existing_results[list_idx] if list_idx < len(existing_results) else ''

            # 진행 상황 출력
            current = row_idx - start_row + 1
            print(f"[{current}/{stats.total}] Row {row_idx}: {business_number}")

            # 행 처리
            process_row(
                checker,
                sheets_client,
                row_idx,
                business_number,
                existing_result,
                stats
            )

            # 진행률 출력 (10개마다)
            if current % 10 == 0:
                print_progress(current, stats.total, stats)

            # 딜레이 (차단 방지)
            if row_idx < end_row:
                delay = random.uniform(0.5, 1.0)
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\n\n[INFO] 사용자에 의해 중단됨")

    except Exception as e:
        print(f"\n[ERROR] 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # 종료 시간 기록
        stats.end()

        # 브라우저 종료
        if checker:
            checker.close()

        # 최종 요약
        print_summary(stats)


if __name__ == '__main__':
    main()
