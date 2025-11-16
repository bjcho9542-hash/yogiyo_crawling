"""
Google Sheets API 클라이언트
"""
import os
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config


class GoogleSheetsClient:
    """Google Sheets API 클라이언트"""

    def __init__(self, sheet_id: str):
        self.sheet_id = sheet_id
        self.service = None
        self.setup_api()

    def setup_api(self):
        """Google Sheets API 연결"""
        try:
            # credentials.json 파일 경로
            creds_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'credentials.json')

            if not os.path.exists(creds_file):
                raise FileNotFoundError(
                    f"\n[ERROR] credentials.json 파일을 찾을 수 없습니다!\n\n"
                    f"프로젝트 루트에 'credentials.json' 파일이 필요합니다.\n"
                )

            # Service Account 인증
            credentials = service_account.Credentials.from_service_account_file(
                creds_file,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )

            # Sheets API 서비스 빌드
            self.service = build('sheets', 'v4', credentials=credentials)
            print("[OK] Google Sheets API 연결 완료")

        except Exception as e:
            print(f"[ERROR] Google Sheets API 연결 실패: {e}")
            raise

    def read_column(self, column: str) -> List[str]:
        """
        특정 열 전체 데이터 읽기

        Args:
            column: 열 이름 (예: 'E')

        Returns:
            해당 열의 데이터 리스트
        """
        try:
            range_name = f'{column}:{column}'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])
            # 1차원 리스트로 변환 (각 행은 [값] 형태이므로)
            data = [row[0] if row else '' for row in values]

            print(f"[OK] {column}열 데이터 읽기 완료: {len(data)}개 행")
            return data

        except HttpError as e:
            print(f"[ERROR] {column}열 읽기 실패: {e}")
            raise

    def write_cell(self, row: int, column: str, value: str):
        """
        특정 셀에 값 쓰기

        Args:
            row: 행 번호 (1부터 시작)
            column: 열 이름 (예: 'W')
            value: 쓸 값
        """
        try:
            range_name = f'{column}{row}'
            body = {'values': [[value]]}

            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()

            print(f"[OK] {range_name} 셀 쓰기 완료")

        except HttpError as e:
            print(f"[ERROR] {range_name} 셀 쓰기 실패: {e}")
            raise

    def read_range(self, start_row: int, end_row: int, column: str) -> List[str]:
        """
        특정 범위의 데이터 읽기

        Args:
            start_row: 시작 행 (1부터 시작)
            end_row: 종료 행
            column: 열 이름 (예: 'E')

        Returns:
            해당 범위의 데이터 리스트
        """
        try:
            range_name = f'{column}{start_row}:{column}{end_row}'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])
            data = [row[0] if row else '' for row in values]

            print(f"[OK] {range_name} 범위 읽기 완료: {len(data)}개")
            return data

        except HttpError as e:
            print(f"[ERROR] {range_name} 범위 읽기 실패: {e}")
            raise

    def batch_update(self, updates: List[dict]):
        """
        여러 셀을 한 번에 업데이트

        Args:
            updates: [{'range': 'W3', 'value': '입점 가능'}, ...] 형태의 리스트
        """
        try:
            data = []
            for update in updates:
                data.append({
                    'range': update['range'],
                    'values': [[update['value']]]
                })

            body = {'valueInputOption': 'RAW', 'data': data}

            self.service.spreadsheets().values().batchUpdate(
                spreadsheetId=self.sheet_id,
                body=body
            ).execute()

            print(f"[OK] Batch 업데이트 완료: {len(updates)}개 셀")

        except HttpError as e:
            print(f"[ERROR] Batch 업데이트 실패: {e}")
            raise


def test_sheets_client():
    """Google Sheets 클라이언트 테스트"""
    print("=" * 80)
    print("Google Sheets API 테스트")
    print("=" * 80)

    # Sheet ID 입력
    sheet_id = input("\n조회할 Google 스프레드시트 ID를 입력하세요: ").strip()

    if not sheet_id:
        print("[ERROR] Sheet ID가 비어있습니다!")
        return

    try:
        # 클라이언트 생성
        client = GoogleSheetsClient(sheet_id)

        # E열 데이터 읽기 테스트
        print("\n[TEST] E열 데이터 읽기...")
        e_data = client.read_column('E')
        print(f"E열 데이터 (처음 5개): {e_data[:5]}")

        # W열에 테스트 값 쓰기
        print("\n[TEST] W3 셀에 테스트 값 쓰기...")
        client.write_cell(3, 'W', '[테스트] 입점신청 가능한 사업자번호입니다')

        print("\n[OK] 테스트 완료!")

    except Exception as e:
        print(f"\n[ERROR] 테스트 실패: {e}")


if __name__ == '__main__':
    test_sheets_client()
