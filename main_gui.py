"""
요기요 입점 여부 조회 매크로 - GUI 버전
"""
import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime

from google_sheets_client import GoogleSheetsClient
from yogiyo_checker import YogiyoChecker
import config


class YogiyoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("요기요 입점 여부 조회 매크로 v1.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # 상태 변수
        self.is_running = False
        self.search_thread = None
        self.checker = None
        self.sheets_client = None

        # 통계
        self.stats = {
            'total': 0,
            'processed': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'available': 0,
            'registered': 0,
            'invalid': 0,
            'unknown': 0,
            'start_time': None
        }

        # UI 변수
        self.sheet_url_var = tk.StringVar()
        self.start_row_var = tk.IntVar(value=2)
        self.end_row_var = tk.IntVar(value=0)

        # UI 구성
        self.setup_ui()

    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 1. 제목
        title_label = ttk.Label(
            main_frame,
            text="요기요 입점 여부 사업자번호 조회 매크로",
            font=("맑은 고딕", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # 2. 스프레드시트 설정
        sheet_frame = ttk.LabelFrame(main_frame, text="📊 Google Sheets 설정", padding="10")
        sheet_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(sheet_frame, text="스프레드시트 URL:", font=("맑은 고딕", 9, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        url_entry = ttk.Entry(sheet_frame, textvariable=self.sheet_url_var, width=80, font=("맑은 고딕", 9))
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        help_label = ttk.Label(
            sheet_frame,
            text="💡 https://docs.google.com/spreadsheets/d/[Sheet_ID]/edit 형태의 URL 전체를 입력",
            foreground="gray",
            font=("맑은 고딕", 8)
        )
        help_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)

        # 3. 행 범위 설정
        range_frame = ttk.LabelFrame(main_frame, text="📍 조회 범위 설정", padding="10")
        range_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(range_frame, text="시작 행:").grid(row=0, column=0, sticky=tk.W, pady=5)
        start_entry = ttk.Entry(range_frame, textvariable=self.start_row_var, width=15)
        start_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)

        ttk.Label(range_frame, text="종료 행 (0=끝까지):").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        end_entry = ttk.Entry(range_frame, textvariable=self.end_row_var, width=15)
        end_entry.grid(row=0, column=3, sticky=tk.W, pady=5, padx=5)

        # 4. 컨트롤 버튼
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)

        self.start_btn = ttk.Button(
            btn_frame,
            text="🚀 시작",
            command=self.start_search,
            width=20
        )
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = ttk.Button(
            btn_frame,
            text="⏹ 중지",
            command=self.stop_search,
            width=20,
            state=tk.DISABLED
        )
        self.stop_btn.grid(row=0, column=1, padx=5)

        # 5. 진행률 표시
        progress_frame = ttk.LabelFrame(main_frame, text="📈 진행 상황", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        self.progress_label = ttk.Label(
            progress_frame,
            text="대기 중...",
            font=("맑은 고딕", 10)
        )
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=860
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.stats_label = ttk.Label(
            progress_frame,
            text="처리: 0 | 성공: 0 | 실패: 0 | 스킵: 0 | 입점가능: 0 | 이미입점: 0 | 오류: 0",
            font=("맑은 고딕", 9)
        )
        self.stats_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        # 6. 로그 출력
        log_frame = ttk.LabelFrame(main_frame, text="📝 로그", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            width=100,
            height=15,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 로그 텍스트 태그 설정
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("warning", foreground="orange")
        self.log_text.tag_config("info", foreground="blue")

        # Grid 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

    def log(self, message, tag=None):
        """로그 메시지 출력"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        if tag:
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        else:
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def update_progress(self, current, total):
        """진행률 업데이트"""
        if total > 0:
            percentage = (current / total) * 100
            self.progress_bar['value'] = percentage
            self.progress_label.config(
                text=f"진행률: {current}/{total} ({percentage:.1f}%)"
            )

    def update_stats(self):
        """통계 업데이트"""
        self.stats_label.config(
            text=f"처리: {self.stats['processed']} | "
                 f"성공: {self.stats['success']} | "
                 f"실패: {self.stats['failed']} | "
                 f"스킵: {self.stats['skipped']} | "
                 f"입점가능: {self.stats['available']} | "
                 f"이미입점: {self.stats['registered']} | "
                 f"오류: {self.stats['invalid']}"
        )

    def extract_sheet_id(self, url_or_id: str) -> str:
        """URL에서 Sheet ID 추출"""
        import re
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', url_or_id)
        if match:
            return match.group(1)
        return url_or_id

    def start_search(self):
        """검색 시작"""
        if self.is_running:
            messagebox.showwarning("경고", "이미 실행 중입니다!")
            return

        # 입력 검증
        sheet_url = self.sheet_url_var.get().strip()
        if not sheet_url:
            messagebox.showerror("오류", "스프레드시트 URL을 입력해주세요!")
            return

        # Sheet ID 추출
        sheet_id = self.extract_sheet_id(sheet_url)
        start_row = self.start_row_var.get()
        end_row = self.end_row_var.get()

        # 상태 변경
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        # 로그 초기화
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

        # 통계 초기화
        self.stats = {
            'total': 0,
            'processed': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'available': 0,
            'registered': 0,
            'invalid': 0,
            'unknown': 0,
            'start_time': datetime.now()
        }

        self.log("=" * 80)
        self.log(f"조회 시작 - Sheet ID: {sheet_id}", "info")
        self.log(f"범위: {start_row}행 ~ {end_row if end_row > 0 else '끝까지'}", "info")
        self.log("=" * 80)

        # 백그라운드 스레드에서 실행
        self.search_thread = threading.Thread(
            target=self.run_search,
            args=(sheet_id, start_row, end_row),
            daemon=True
        )
        self.search_thread.start()

    def run_search(self, sheet_id, start_row, end_row):
        """검색 실행 (백그라운드)"""
        try:
            # Google Sheets 연결
            self.log("Google Sheets API 연결 중...", "info")
            self.sheets_client = GoogleSheetsClient(sheet_id)
            self.log("Google Sheets API 연결 완료!", "success")

            # E열 데이터 읽기
            self.log(f"{config.COLUMN_BUSINESS_NUMBER}열 데이터 읽기 중...", "info")
            business_numbers = self.sheets_client.read_column(config.COLUMN_BUSINESS_NUMBER)

            # W열 데이터 읽기
            self.log(f"{config.COLUMN_RESULT}열 데이터 읽기 중...", "info")
            existing_results = self.sheets_client.read_column(config.COLUMN_RESULT)

            # 종료 행 설정
            if end_row == 0 or end_row > len(business_numbers):
                end_row = len(business_numbers)

            self.stats['total'] = end_row - start_row + 1
            self.log(f"총 {self.stats['total']}개 행 처리 예정", "info")

            # Chrome 브라우저 실행
            self.log("Chrome 브라우저 실행 중...", "info")
            self.checker = YogiyoChecker()
            self.log("Chrome 브라우저 실행 완료!", "success")

            # 각 행 처리
            for row_idx in range(start_row, end_row + 1):
                if not self.is_running:
                    self.log("사용자에 의해 중단됨", "warning")
                    break

                list_idx = row_idx - 1
                business_number = business_numbers[list_idx] if list_idx < len(business_numbers) else ''
                existing_result = existing_results[list_idx] if list_idx < len(existing_results) else ''

                current = row_idx - start_row + 1
                self.log(f"[{current}/{self.stats['total']}] Row {row_idx}: {business_number}")

                # 빈 사업자번호 스킵
                if not business_number or business_number.strip() == "":
                    self.log("  [SKIP] 빈 사업자번호", "warning")
                    self.stats['skipped'] += 1
                    self.update_progress(current, self.stats['total'])
                    self.update_stats()
                    continue

                # 이미 결과가 있는 행 스킵
                if config.SKIP_EXISTING and existing_result and existing_result.strip():
                    self.log(f"  [SKIP] 이미 처리됨: {existing_result[:30]}...", "warning")
                    self.stats['skipped'] += 1
                    self.update_progress(current, self.stats['total'])
                    self.update_stats()
                    continue

                # 조회 실행
                try:
                    status, message = self.checker.check_business_number(business_number)
                    self.log(f"  [결과] {message}", "success")

                    # W열에 결과 저장
                    result_value = message if config.RESULT_FORMAT == 'MESSAGE' else status
                    self.sheets_client.write_cell(row_idx, config.COLUMN_RESULT, result_value)

                    # 통계 업데이트
                    self.stats['processed'] += 1
                    self.stats['success'] += 1
                    if status == 'AVAILABLE':
                        self.stats['available'] += 1
                    elif status == 'REGISTERED':
                        self.stats['registered'] += 1
                    elif status == 'INVALID':
                        self.stats['invalid'] += 1

                except Exception as e:
                    self.log(f"  [ERROR] {e}", "error")
                    self.stats['processed'] += 1
                    self.stats['failed'] += 1

                self.update_progress(current, self.stats['total'])
                self.update_stats()

                # 딜레이
                if row_idx < end_row:
                    time.sleep(0.5)

            # 완료
            self.log("=" * 80)
            self.log("조회 완료!", "success")
            duration = datetime.now() - self.stats['start_time']
            self.log(f"소요 시간: {duration}", "info")
            self.log("=" * 80)

            messagebox.showinfo("완료", f"조회가 완료되었습니다!\n\n"
                                       f"처리: {self.stats['processed']}\n"
                                       f"성공: {self.stats['success']}\n"
                                       f"실패: {self.stats['failed']}")

        except Exception as e:
            self.log(f"오류 발생: {e}", "error")
            messagebox.showerror("오류", f"오류가 발생했습니다:\n{e}")

        finally:
            # 정리
            if self.checker:
                self.checker.close()

            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

    def stop_search(self):
        """검색 중지"""
        if messagebox.askyesno("중지 확인", "정말로 중지하시겠습니까?"):
            self.is_running = False
            self.log("중지 요청됨...", "warning")


def main():
    """메인 함수"""
    root = tk.Tk()
    app = YogiyoGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
