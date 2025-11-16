# 요기요 입점 여부 사업자번호 조회 매크로 PRD

## 1. 문서 정보

| 항목 | 내용 |
|------|------|
| **문서 제목** | 요기요 입점 여부 사업자번호 조회 매크로 PRD (터미널 버전) |
| **버전** | v1.0 |
| **작성일** | 2025-01-16 |
| **작성자** | bjcho9542-hash |
| **관련 문서** | [참고자료_네이버크롤링분석.txt](./참고자료_네이버크롤링분석.txt) |

---

## 2. 프로젝트 개요

### 프로젝트명
**요기요 입점 여부 사업자번호 조회 매크로 (Yogiyo Business Registration Checker)**

### 한 줄 요약
구글 스프레드시트에 저장된 사업자번호를 요기요 입점 신청 페이지에 자동으로 조회하여, 입점 가능 여부를 판별하고 결과를 자동으로 기록하는 터미널 기반 크롤링 매크로

### 상세 설명
본 프로젝트는 요기요 사장님 사이트의 입점 신청 페이지(https://ceo.yogiyo.co.kr/join-request)에서 사업자번호 입력 및 조회 과정을 자동화하는 Python 기반 매크로입니다.

사용자는 구글 스프레드시트에 조회 대상 사업자번호 목록을 준비하고, 본 매크로를 실행하여 각 사업자번호의 요기요 입점 가능 여부를 자동으로 확인할 수 있습니다. 매크로는 Selenium을 사용하여 요기요 웹페이지에 접속하고, 사업자번호를 입력한 후 조회 버튼을 클릭하여 결과 메시지를 파싱합니다. 파싱된 결과는 Google Sheets API를 통해 자동으로 스프레드시트에 기록됩니다.

이 매크로는 기존에 개발된 "네이버 지도 전화번호 검색 프로그램"의 설계 원칙과 기술 스택을 계승하며, 안정적인 크롤링을 위한 여러 CSS 셀렉터 시도, 충분한 대기 시간, 에러 핸들링, 진행 상황 로그 등의 검증된 설계 패턴을 재사용합니다.

---

## 3. 목표 및 비즈니스 가치

### 해결하고자 하는 문제
- **수동 조회의 비효율성**: 수백~수천 개의 사업자번호를 요기요 사이트에서 하나씩 수동으로 조회하는 것은 시간 소모가 크고 오류 발생 가능성이 높음
- **입점 가능 대상 필터링 어려움**: 전체 사업자번호 중 실제 영업 대상이 되는 "입점 미등록" 사업자를 구별하는 데 많은 인력 투입 필요
- **데이터 정리 및 기록의 불일치**: 수동 작업 시 조회 결과를 일관되게 기록하고 관리하기 어려움

### 시간/노동 절감 효과
- **자동화 처리 속도**: 사업자번호 1건당 약 3~5초 처리 (수동 대비 10배 이상 빠름)
- **대량 처리 가능**: 500건 기준 약 25~40분 소요 (수동 시 8시간 이상 소요)
- **인적 오류 제거**: 입력 실수, 기록 누락 등의 휴먼 에러 최소화
- **24시간 무인 운영 가능**: 터미널에서 실행 후 다른 업무 병행 가능

### 활용 시나리오
1. **영업 리스트 생성**: 입점 가능한 사업자번호만 필터링하여 신규 가맹점 영업 대상 리스트 작성
2. **데이터 클렌징**: 기존 사업자번호 DB에서 중복 입점 시도를 사전에 방지
3. **시장 조사**: 특정 지역/업종의 요기요 미입점 사업자 현황 파악

---

## 4. 범위(Scope)

### 포함 범위
✅ **요기요 입점 조회 자동화**
- 요기요 사장님 사이트 입점 신청 페이지 접속
- 사업자번호 입력 필드 자동 입력
- 조회 버튼 자동 클릭
- 결과 메시지 파싱 및 분류

✅ **Google Sheets 연동**
- E열에서 사업자번호 자동 읽기
- W열에 조회 결과 자동 기록
- Service Account 인증 방식 지원

✅ **터미널 기반 CLI 인터페이스**
- 스프레드시트 ID 입력 방식
- 시작 행/종료 행 지정 기능
- 실시간 진행 상황 로그 출력
- 처리 완료 후 요약 통계 제공

✅ **안정성 및 에러 핸들링**
- 여러 CSS 셀렉터 백업 전략
- 네트워크/페이지 로딩 대기 처리
- 오류 발생 시 스킵 및 로그 기록

### 제외 범위
❌ **GUI 버전**: 향후 확장으로 계획 (현재는 터미널 CLI만)
❌ **요기요 로그인/인증**: 공개 페이지 조회만 수행
❌ **다른 페이지 크롤링**: 입점 신청 페이지 외 메뉴 조회, 가격 정보 등은 제외
❌ **사업자번호 유효성 검증**: 국세청 API 연동 등은 제외 (형식 검증만 수행)
❌ **자동 입점 신청**: 조회만 수행하며, 실제 입점 신청 절차는 수행하지 않음

---

## 5. 주요 사용자 · 유스케이스

### 사용자 유형
- **내부 운영자**: 요기요 입점 관련 업무를 담당하는 운영팀
- **영업 담당자**: 신규 가맹점 모집을 위한 영업 리스트 생성 담당자
- **데이터 분석가**: 시장 조사 및 입점 현황 분석을 수행하는 인력

### 대표 유스케이스

#### UC-01: 대량 사업자번호 일괄 조회
**시나리오**:
1. 영업팀이 외부에서 수집한 500개의 사업자번호를 구글 스프레드시트 E열에 입력
2. 터미널에서 매크로 실행 및 스프레드시트 ID 입력
3. 매크로가 자동으로 500개 사업자번호를 순차 조회 (약 30분 소요)
4. W열에 "입점신청 가능한 사업자번호입니다" 또는 "이미 등록된 사업자번호입니다" 등의 결과 기록
5. 스프레드시트에서 필터 기능으로 "입점신청 가능" 항목만 추출하여 영업 리스트 완성

#### UC-02: 중간 재개 및 에러 처리
**시나리오**:
1. 1000개 사업자번호 조회 중 300번째에서 네트워크 오류 발생
2. 매크로는 에러 로그를 남기고 해당 행 스킵 후 다음 행 계속 처리
3. 처리 완료 후 터미널에 "에러 발생 행: 300" 등의 요약 정보 출력
4. 사용자는 에러 발생 행만 수동 확인 후 재실행 (시작 행 300, 종료 행 300 지정)

#### UC-03: 특정 범위만 선택 조회
**시나리오**:
1. 스프레드시트에 2000개 사업자번호가 있지만, 이번에는 501~1000행만 조회 필요
2. 터미널에서 시작 행 501, 종료 행 1000 입력
3. 매크로는 501~1000행만 처리하고 나머지는 무시

---

## 6. 기능 요구사항 (Functional Requirements)

### [F-01] 스프레드시트 연결 및 데이터 읽기/쓰기

#### F-01-01: 스프레드시트 ID 입력
- 터미널 실행 시 "조회할 Google 스프레드시트 ID를 입력하세요:" 프롬프트 표시
- 사용자가 시트 ID 입력 (예: `1A2B3C4D5E6F...`)
- 입력값 검증: 공백 체크, 최소 길이 체크

#### F-01-02: E열에서 사업자번호 읽기
- Google Sheets API를 사용하여 E열 전체 데이터 읽기
- 데이터 범위: `E:E` (E열 전체)
- 읽어온 데이터는 리스트 형태로 저장 (예: `['1234567890', '9876543210', ...]`)
- 빈 셀은 빈 문자열(`''`)로 처리

#### F-01-03: W열에 결과 쓰기
- 조회 결과는 해당 행의 W열에 기록
- 예: 3행의 사업자번호 조회 결과 → W3 셀에 기록
- 기록 형식: **원문 메시지를 그대로 저장** (예: "이미 등록된 사업자번호입니다. 고객만족센터로 문의해 주세요.")
- Google Sheets API `values().update()` 메서드 사용

#### F-01-04: 시작/종료 행 지정
- 터미널에서 시작 행 입력 프롬프트: "시작 행 (기본값 3):"
  - 기본값 3 (1~2행은 헤더로 간주)
  - 엔터만 입력 시 기본값 적용
- 종료 행 입력 프롬프트: "종료 행 (0=끝까지):"
  - 0 입력 시 E열의 마지막 데이터 행까지 처리
  - 숫자 입력 시 해당 행까지만 처리

#### F-01-05: Google API 인증
- Service Account 방식 사용
- `credentials.json` 파일을 코드에 내장 (네이버 프로젝트와 동일 방식)
- 실행 시 임시 파일로 저장 후 API 연결, 종료 시 임시 파일 삭제
- 스프레드시트 공유 설정: "링크가 있는 모든 사용자 - 편집자" 권한 필요

---

### [F-02] 요기요 페이지 접속 및 셀렉터 구조

#### F-02-01: 접속 URL
```
https://ceo.yogiyo.co.kr/join-request?event_type=ad&utm_source=yogiyo&utm_medium=portal&utm_campaign=partner&utm_content=up_btn
```

#### F-02-02: 사업자번호 입력 필드 셀렉터
**우선순위 1 (Primary)**:
```css
input[name="company_number"][placeholder="입력해 주세요"]
```

**우선순위 2 (Backup 1)**:
```css
input.sc-hAZoDl.fdtDAM.sc-dIouRR.dGckYu
```

**우선순위 3 (Backup 2)**:
```css
div.sc-fnykZs.lgUEyv input[type="text"]
```

**처리 로직**:
- 우선순위 1부터 시도하여 요소가 발견되면 해당 셀렉터 사용
- 모든 셀렉터로 요소를 찾지 못하면 에러 로그 기록 후 해당 행 스킵

#### F-02-03: 조회 버튼 셀렉터
**우선순위 1 (Primary)**:
```css
div.sc-dkzDqf.jUa-DCf[size="48"][color="accent100"]
```

**우선순위 2 (Backup 1)**:
```css
div.sc-dkzDqf.jUa-DCf
```

**우선순위 3 (Backup 2)**:
```css
button[type="button"]
```

**처리 로직**:
- 입력 필드와 동일하게 우선순위별 시도
- 버튼 클릭 후 결과 로딩을 위해 **3초 대기** (명시적 대기)

#### F-02-04: 결과 메시지 영역 셀렉터
**우선순위 1 (Primary)**:
```css
div.sc-hHLeRK.gpWodO
```

**우선순위 2 (Backup 1)**:
```css
div.sc-hHLeRK
```

**우선순위 3 (Backup 2)**:
```css
div[class*="sc-hHLeRK"]
```

**처리 로직**:
- 메시지 영역의 텍스트를 `.text` 속성으로 추출
- 추출된 텍스트를 트리밍 후 다음 단계로 전달

#### F-02-05: 셀렉터 변경 대응 전략
- 모든 셀렉터는 `config.py` 또는 환경변수로 분리하여 관리
- 요기요 사이트 구조 변경 시 코드 수정 없이 설정 파일만 수정 가능
- 로그에 "사용된 셀렉터 우선순위" 기록 (예: "Primary selector used")

---

### [F-03] 메시지 파싱 및 상태 분류

#### F-03-01: 메시지 분류 규칙
조회 후 추출된 메시지를 다음 3가지 상태로 분류:

| 상태 코드 | 메시지 텍스트 | 의미 |
|-----------|---------------|------|
| `REGISTERED` | "이미 등록된 사업자번호입니다. 고객만족센터로 문의해 주세요." | 이미 요기요에 입점한 사업자 |
| `AVAILABLE` | "입점신청 가능한 사업자번호입니다" | 입점 가능한 사업자번호 (목표 대상) |
| `INVALID` | "사업자 번호를 확인해 주세요." | 사업자번호 형식 오류 (10자리 미만 등) |

#### F-03-02: W열 저장 형식
**기본 방식**: 원문 메시지를 그대로 저장
```
예시:
W3: "이미 등록된 사업자번호입니다. 고객만족센터로 문의해 주세요."
W4: "입점신청 가능한 사업자번호입니다"
W5: "사업자 번호를 확인해 주세요."
```

**대안 방식** (설정 옵션으로 제공):
- 상태 코드 저장 옵션 추가 가능 (`REGISTERED`, `AVAILABLE`, `INVALID`)
- 환경변수 `RESULT_FORMAT=CODE` 설정 시 상태 코드만 저장

#### F-03-03: 메시지 매칭 로직
```python
def classify_message(message_text):
    message = message_text.strip()

    if "이미 등록된 사업자번호입니다" in message:
        return "REGISTERED", message
    elif "입점신청 가능한 사업자번호입니다" in message:
        return "AVAILABLE", message
    elif "사업자 번호를 확인해 주세요" in message:
        return "INVALID", message
    else:
        # 예상치 못한 메시지 (사이트 변경 가능성)
        return "UNKNOWN", message
```

#### F-03-04: UNKNOWN 상태 처리
- 예상치 못한 메시지가 나타날 경우 `UNKNOWN` 상태로 분류
- W열에는 원문 메시지 저장
- 터미널에 경고 로그 출력: `[WARNING] Unknown message detected: {message}`
- 개발자가 나중에 확인하여 분류 로직 업데이트

---

### [F-04] 반복 처리 및 스킵 규칙

#### F-04-01: 빈 사업자번호 행 스킵
```python
if not business_number or business_number.strip() == "":
    print(f"[SKIP] Row {row_idx}: Empty business number")
    skipped_count += 1
    continue
```

#### F-04-02: 이미 결과가 있는 행 스킵 (선택 옵션)
- 환경변수 `SKIP_EXISTING=true` 설정 시
- W열에 이미 값이 있으면 해당 행 스킵
```python
if existing_result and SKIP_EXISTING:
    print(f"[SKIP] Row {row_idx}: Already processed (Result: {existing_result[:30]}...)")
    skipped_count += 1
    continue
```

#### F-04-03: 사업자번호 형식 검증
- 10자리 숫자가 아닌 경우 경고 로그 출력 후 계속 진행 (요기요에서 "사업자 번호를 확인해 주세요" 메시지 반환 예상)
```python
if not re.match(r'^\d{10}$', business_number):
    print(f"[WARNING] Row {row_idx}: Invalid format ({business_number}), proceeding anyway")
```

#### F-04-04: 오류 발생 시 재시도/스킵 전략
- 셀렉터 탐색 실패: 3회 재시도 (각 1초 대기 후)
- 3회 재시도 실패 시 해당 행 스킵하고 다음 행으로 이동
- 에러 행 번호를 리스트에 기록 (`error_rows = []`)
```python
retry_count = 0
max_retries = 3

while retry_count < max_retries:
    try:
        # 크롤링 로직
        break
    except Exception as e:
        retry_count += 1
        if retry_count >= max_retries:
            print(f"[ERROR] Row {row_idx}: Max retries exceeded - {e}")
            error_rows.append(row_idx)
            break
        time.sleep(1)
```

---

### [F-05] 로그 및 진행상태 표시

#### F-05-01: 실시간 진행 로그
각 사업자번호 처리 시 다음 정보 출력:
```
[3/500] Row 3: 1234567890
  → 입력 완료
  → 조회 버튼 클릭
  → 결과: "입점신청 가능한 사업자번호입니다"
  → W3 저장 완료
  ✓ [SUCCESS] Row 3 processed (1.2초 소요)
```

#### F-05-02: 진행률 표시
```
Progress: 3/500 (0.6%)
Processed: 3 | Success: 2 | Failed: 1 | Skipped: 0
```

#### F-05-03: 통계 카운트
- `processed_count`: 실제 조회 시도한 건수
- `success_count`: 정상적으로 결과를 받아온 건수
- `failed_count`: 에러 발생 건수
- `skipped_count`: 스킵한 건수 (빈 값, 이미 처리된 행 등)
- `available_count`: "입점신청 가능" 건수
- `registered_count`: "이미 등록" 건수
- `invalid_count`: "번호 오류" 건수

#### F-05-04: 처리 완료 후 요약 출력
```
================================================================================
처리 완료!
================================================================================
총 처리 행: 500
  - 성공: 485
  - 실패: 10
  - 스킵: 5

상태별 집계:
  - 입점 가능 (AVAILABLE): 320
  - 이미 입점 (REGISTERED): 150
  - 번호 오류 (INVALID): 15
  - 알 수 없음 (UNKNOWN): 0

에러 발생 행: [15, 87, 203, 401, ...]
총 소요 시간: 25분 30초
평균 처리 시간: 3.06초/건
================================================================================
```

---

## 7. 비기능 요구사항 (Non-Functional Requirements)

### [NF-01] 안정성

#### NF-01-01: 페이지 로딩 대기
- **초기 페이지 로드**: 페이지 접속 후 5초 대기 (페이지 전체 로딩 완료)
- **버튼 클릭 후 대기**: 조회 버튼 클릭 후 3초 대기 (결과 메시지 로딩)
- **명시적 대기**: `WebDriverWait` 사용 (최대 10초)
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
```

#### NF-01-02: 셀렉터 관리 전략
- 모든 셀렉터를 `config.py`에 우선순위별로 정의
- 셀렉터 변경 시 코드 수정 없이 설정 파일만 수정
- 로그에 사용된 셀렉터 우선순위 기록

#### NF-01-03: 에러 복구 메커니즘
- 네트워크 오류: 3회 재시도 (각 1초 대기)
- 셀렉터 탐색 실패: 백업 셀렉터 순차 시도
- Google Sheets API 오류: 5회 재시도 (지수 백오프 방식)

---

### [NF-02] 성능

#### NF-02-01: 처리 가능 행 수
- **목표**: 1회 실행당 1,000건 이상 처리 가능
- **예상 처리 시간**: 사업자번호 1건당 3~5초
  - 1,000건 기준: 50~83분 소요

#### NF-02-02: 차단 방지 딜레이
- 각 사업자번호 조회 후 **0.5~1초 랜덤 딜레이** 추가
```python
import random
time.sleep(random.uniform(0.5, 1.0))
```
- 환경변수로 딜레이 조절 가능: `SEARCH_DELAY=1.0`

#### NF-02-03: 리소스 사용
- 브라우저 재사용: 전체 작업 동안 브라우저 1개만 사용 (매번 새로 열지 않음)
- 메모리 관리: 100건마다 로그 버퍼 비우기

---

### [NF-03] 유지보수성

#### NF-03-01: 설정 파일 분리
**config.py 예시**:
```python
# 요기요 URL
YOGIYO_URL = "https://ceo.yogiyo.co.kr/join-request?event_type=ad&..."

# 셀렉터 우선순위
INPUT_SELECTORS = [
    'input[name="company_number"][placeholder="입력해 주세요"]',
    'input.sc-hAZoDl.fdtDAM.sc-dIouRR.dGckYu',
    'div.sc-fnykZs.lgUEyv input[type="text"]'
]

BUTTON_SELECTORS = [
    'div.sc-dkzDqf.jUa-DCf[size="48"][color="accent100"]',
    'div.sc-dkzDqf.jUa-DCf',
    'button[type="button"]'
]

MESSAGE_SELECTORS = [
    'div.sc-hHLeRK.gpWodO',
    'div.sc-hHLeRK',
    'div[class*="sc-hHLeRK"]'
]

# 스프레드시트 열 위치
COLUMN_BUSINESS_NUMBER = 'E'  # 사업자번호 입력 열
COLUMN_RESULT = 'W'           # 결과 출력 열

# 대기 시간
PAGE_LOAD_WAIT = 5    # 초기 페이지 로드 대기 (초)
BUTTON_CLICK_WAIT = 3 # 버튼 클릭 후 대기 (초)
SEARCH_DELAY = 1.0    # 조회 간 딜레이 (초)
```

#### NF-03-02: 환경변수 관리 (.env)
```bash
GOOGLE_SHEET_ID=<Sheet ID>
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json
SEARCH_DELAY=1.0
SKIP_EXISTING=false
RESULT_FORMAT=MESSAGE  # MESSAGE or CODE
HEADLESS_MODE=false
```

---

### [NF-04] 보안

#### NF-04-01: Google 인증 정보 관리
- Service Account JSON 파일을 코드에 내장
- 실행 시 임시 파일로 저장 후 사용, 종료 시 자동 삭제
- Git에 커밋 시 `.gitignore`에 `credentials.json` 추가 (실제 파일은 제외)

#### NF-04-02: 스프레드시트 공유 권한
- 사용자 안내 메시지:
```
⚠️  스프레드시트를 "링크가 있는 모든 사용자 - 편집자"로 공유하세요!
   1. 스프레드시트 우측 상단 "공유" 버튼 클릭
   2. "일반 액세스" → "링크가 있는 모든 사용자" 선택
   3. 권한: "편집자" 선택
   4. "완료" 클릭
```

#### NF-04-03: 민감 정보 보호
- 터미널 로그에 사업자번호 전체를 표시하지 않음 (옵션)
```python
# 전체 표시 대신
print(f"Processing: {biz_number[:3]}****{biz_number[-2:]}")
```

---

## 8. 기술 스택 및 아키텍처

### 기술 스택

| 분류 | 기술 | 버전 | 용도 |
|------|------|------|------|
| **언어** | Python | 3.10+ | 메인 개발 언어 |
| **웹 자동화** | Selenium | 4.27.1 | 요기요 웹페이지 크롤링 |
| **브라우저 드라이버** | webdriver-manager | 4.0.2 | ChromeDriver 자동 관리 |
| **Google API** | google-api-python-client | 2.154.0 | Google Sheets API 연동 |
| **인증** | google-auth | 2.36.0 | Service Account 인증 |
| **환경변수** | python-dotenv | 1.0.1 | .env 파일 관리 |

### 아키텍처 개요

#### 모듈 구조
```
yogiyo_crawling/
├── main.py                      # 메인 진입점 (CLI 인터페이스)
├── yogiyo_checker.py            # 요기요 크롤링 로직
├── google_sheets_client.py      # Google Sheets API 클라이언트
├── config.py                    # 설정값 (URL, 셀렉터 등)
├── utils.py                     # 유틸리티 함수 (로그, 포맷팅 등)
├── requirements.txt             # 패키지 의존성
├── .env.example                 # 환경변수 예시 파일
├── .gitignore                   # Git 제외 파일
└── README.md                    # 사용 설명서
```

#### 클래스 다이어그램 (텍스트)
```
┌─────────────────────────────┐
│   GoogleSheetsClient        │
├─────────────────────────────┤
│ + setup_api()               │
│ + read_column(col)          │
│ + write_cell(row, col, val) │
│ + read_range(start, end)    │
└─────────────────────────────┘
           ▲
           │
           │ uses
           │
┌─────────────────────────────┐
│   YogiyoChecker             │
├─────────────────────────────┤
│ - driver: WebDriver         │
│ - sheets_client             │
│ - config                    │
├─────────────────────────────┤
│ + setup_browser()           │
│ + check_business_number(num)│
│ + parse_result_message()    │
│ + run(start_row, end_row)   │
└─────────────────────────────┘
           ▲
           │
           │ uses
           │
┌─────────────────────────────┐
│   main.py                   │
├─────────────────────────────┤
│ + get_user_input()          │
│ + display_summary()         │
│ + main()                    │
└─────────────────────────────┘
```

#### 데이터 플로우
```
사용자 입력 (Sheet ID, 시작/종료 행)
    ↓
GoogleSheetsClient: E열 데이터 읽기
    ↓
YogiyoChecker: 각 사업자번호 순차 처리
    ├─ Selenium: 요기요 페이지 접속
    ├─ 사업자번호 입력
    ├─ 조회 버튼 클릭
    ├─ 결과 메시지 파싱
    └─ 상태 분류 (REGISTERED/AVAILABLE/INVALID)
    ↓
GoogleSheetsClient: W열에 결과 기록
    ↓
진행 로그 출력 (터미널)
    ↓
처리 완료 후 요약 통계 출력
```

---

## 9. 상세 플로우 정의

### 9.1 메인 실행 플로우

```
[사용자]
    │
    ├─ 터미널에서 실행: python main.py
    │
    ↓
[main.py]
    │
    ├─ 환경변수 로드 (.env)
    │
    ├─ 사용자 입력 받기
    │   ├─ Sheet ID 입력
    │   ├─ 시작 행 입력 (기본값: 3)
    │   └─ 종료 행 입력 (기본값: 0 = 끝까지)
    │
    ├─ GoogleSheetsClient 초기화
    │   ├─ Service Account 인증
    │   └─ Sheets API 연결
    │
    ├─ YogiyoChecker 초기화
    │   ├─ Selenium WebDriver 설정
    │   ├─ Chrome 브라우저 실행
    │   └─ 요기요 URL 접속
    │
    ├─ E열 데이터 읽기 (GoogleSheetsClient)
    │   └─ 사업자번호 리스트 반환
    │
    ├─ 반복 루프 (시작 행 ~ 종료 행)
    │   │
    │   ├─ [각 행 처리]
    │   │   │
    │   │   ├─ 사업자번호 가져오기 (E열)
    │   │   │
    │   │   ├─ 검증
    │   │   │   ├─ 빈 값? → 스킵
    │   │   │   ├─ 이미 처리됨(W열 값 존재)? → 스킵 (옵션)
    │   │   │   └─ 형식 검증 (10자리 숫자 아니면 경고)
    │   │   │
    │   │   ├─ 요기요 조회
    │   │   │   ├─ 입력 필드 찾기 (우선순위별 시도)
    │   │   │   ├─ 사업자번호 입력
    │   │   │   ├─ 조회 버튼 찾기 (우선순위별 시도)
    │   │   │   ├─ 버튼 클릭
    │   │   │   ├─ 3초 대기
    │   │   │   ├─ 결과 메시지 영역 찾기
    │   │   │   └─ 메시지 텍스트 추출
    │   │   │
    │   │   ├─ 메시지 분류
    │   │   │   ├─ "이미 등록된..." → REGISTERED
    │   │   │   ├─ "입점신청 가능..." → AVAILABLE
    │   │   │   ├─ "사업자 번호를..." → INVALID
    │   │   │   └─ 기타 → UNKNOWN
    │   │   │
    │   │   ├─ W열에 결과 저장 (GoogleSheetsClient)
    │   │   │
    │   │   ├─ 로그 출력 (터미널)
    │   │   │   └─ "[SUCCESS] Row X: 메시지"
    │   │   │
    │   │   ├─ 통계 업데이트
    │   │   │
    │   │   └─ 딜레이 (0.5~1초)
    │   │
    │   └─ [반복 종료]
    │
    ├─ 브라우저 종료
    │
    ├─ 요약 통계 출력
    │   ├─ 총 처리 건수
    │   ├─ 상태별 집계
    │   ├─ 에러 행 목록
    │   └─ 소요 시간
    │
    └─ 종료
```

### 9.2 예외 상황 처리 플로우

#### 예외 1: 네트워크 오류
```
요기요 페이지 접속 시도
    ↓
[TimeoutException]
    ↓
재시도 카운터 증가 (max: 3회)
    ↓
1초 대기
    ↓
다시 시도
    ↓
3회 실패 시
    ↓
에러 로그 출력: "[ERROR] Network timeout"
    ↓
해당 행 스킵
    ↓
error_rows 리스트에 추가
    ↓
다음 행으로 이동
```

#### 예외 2: 셀렉터 탐색 실패
```
입력 필드 셀렉터 1 시도
    ↓
[NoSuchElementException]
    ↓
로그: "[INFO] Primary selector not found, trying backup..."
    ↓
입력 필드 셀렉터 2 시도
    ↓
성공 → 계속 진행
    ↓
실패 → 셀렉터 3 시도
    ↓
모든 셀렉터 실패 시
    ↓
에러 로그: "[ERROR] All selectors failed for input field"
    ↓
해당 행 스킵
    ↓
error_rows 리스트에 추가
```

#### 예외 3: Google Sheets API 오류
```
W열에 결과 쓰기 시도
    ↓
[Google API Error]
    ↓
재시도 카운터 증가 (max: 5회)
    ↓
지수 백오프 대기 (2^retry_count 초)
    ↓
다시 시도
    ↓
5회 실패 시
    ↓
에러 로그: "[ERROR] Failed to write to Sheets after 5 retries"
    ↓
해당 행 스킵
    ↓
error_rows 리스트에 추가
```

#### 예외 4: CAPTCHA 감지 (수동 처리 필요)
```
조회 후 예상치 못한 페이지 구조 감지
    ↓
"CAPTCHA" 또는 "reCAPTCHA" 텍스트 존재 확인
    ↓
감지 시
    ↓
경고 로그 출력:
"[WARNING] CAPTCHA detected. Please solve manually."
    ↓
프로그램 일시 정지 (사용자 입력 대기)
    ↓
사용자가 수동으로 CAPTCHA 해결
    ↓
엔터 입력 시 계속 진행
```

---

## 10. 에러 핸들링 및 예외 케이스

### 에러 분류 및 처리 전략

| 에러 유형 | 발생 시점 | 처리 방법 | 재시도 | 로그 레벨 |
|-----------|-----------|-----------|--------|-----------|
| **네트워크 타임아웃** | 페이지 접속 | 3회 재시도 후 스킵 | ✅ 3회 | ERROR |
| **셀렉터 탐색 실패** | 요소 찾기 | 백업 셀렉터 시도 → 전체 실패 시 스킵 | ✅ 셀렉터 개수만큼 | ERROR |
| **Google API 오류** | Sheets 읽기/쓰기 | 5회 재시도 (지수 백오프) | ✅ 5회 | ERROR |
| **빈 사업자번호** | 데이터 검증 | 즉시 스킵 | ❌ | WARNING |
| **형식 오류 사업자번호** | 데이터 검증 | 경고 후 계속 진행 | ❌ | WARNING |
| **CAPTCHA 감지** | 조회 후 | 수동 해결 대기 | ❌ | WARNING |
| **예상치 못한 메시지** | 메시지 파싱 | UNKNOWN 상태로 저장 | ❌ | WARNING |
| **Chrome 크래시** | 브라우저 실행 | 프로그램 종료 | ❌ | CRITICAL |

### 에러 핸들링 코드 예시

```python
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def safe_find_element(driver, selectors, element_name):
    """
    여러 셀렉터를 순차적으로 시도하여 요소 찾기
    """
    for i, selector in enumerate(selectors):
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            print(f"[INFO] {element_name} found with selector {i+1}")
            return element
        except NoSuchElementException:
            print(f"[DEBUG] Selector {i+1} failed for {element_name}")
            continue

    raise Exception(f"All selectors failed for {element_name}")

def retry_with_backoff(func, max_retries=5, initial_delay=1):
    """
    지수 백오프 방식으로 재시도
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            print(f"[RETRY] Attempt {attempt+1} failed, waiting {delay}s...")
            time.sleep(delay)
```

---

## 11. 리스크 및 대응 전략

### 리스크 매트릭스

| 리스크 | 발생 가능성 | 영향도 | 우선순위 | 대응 전략 |
|--------|-------------|--------|----------|-----------|
| **요기요 사이트 구조 변경** | 높음 | 높음 | 🔴 P1 | 백업 셀렉터 전략, 설정 파일 분리, 모니터링 |
| **봇 감지 및 차단** | 중간 | 높음 | 🔴 P1 | 랜덤 딜레이, User-Agent 설정, 느린 실행 속도 |
| **CAPTCHA 출현** | 낮음 | 중간 | 🟡 P2 | 수동 해결 대기 모드, 1일 조회 제한 설정 |
| **Google API 쿼터 초과** | 낮음 | 중간 | 🟡 P2 | Batch API 사용, 지수 백오프, 1분당 요청 제한 |
| **법적/약관 이슈** | 중간 | 높음 | 🔴 P1 | 약관 검토, 내부 용도로만 사용, 상업적 이용 금지 |
| **Chrome 버전 호환성** | 낮음 | 낮음 | 🟢 P3 | webdriver-manager 자동 업데이트 |

### 리스크별 상세 대응

#### R-01: 요기요 사이트 구조 변경
**대응 전략**:
1. 셀렉터를 `config.py`에 분리하여 코드 수정 없이 변경 가능
2. 여러 백업 셀렉터 준비 (우선순위 1~3)
3. 매주 1회 사이트 구조 모니터링 (수동)
4. UNKNOWN 메시지 감지 시 즉시 확인

**감지 방법**:
- UNKNOWN 메시지가 전체의 20% 이상 발생 시 경고
- 로그에 "Selector change detected" 메시지 자동 출력

#### R-02: 봇 감지 및 차단
**대응 전략**:
1. **랜덤 딜레이**: 각 조회 후 0.5~1초 랜덤 대기
2. **User-Agent 설정**: 실제 사용자처럼 보이는 User-Agent 사용
```python
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...')
```
3. **Automation 플래그 제거**:
```python
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option('useAutomationExtension', False)
```
4. **1일 조회 제한**: 1일 최대 1,000건으로 제한 (옵션)

#### R-03: Google API 쿼터 초과
**대응 전략**:
1. **Batch API 사용**: 여러 셀 업데이트를 한 번에 처리
```python
# 10개씩 모아서 batch update
batch_data = []
if len(batch_data) >= 10:
    sheets_client.batch_update(batch_data)
    batch_data.clear()
```
2. **1분당 요청 제한**: 60 requests/minute 준수
3. **에러 감지 시 대기**: 쿼터 초과 에러 발생 시 60초 대기 후 재시도

#### R-04: 법적/약관 이슈
**준수 사항**:
- ⚠️ **robots.txt 확인**: 요기요 사이트의 robots.txt 확인
- ⚠️ **이용약관 검토**: 자동화 도구 사용 금지 조항 확인
- ⚠️ **개인정보 보호**: 사업자번호는 공개 정보이나 결과 데이터 외부 유출 금지
- ⚠️ **상업적 이용 제한**: 내부 운영 목적으로만 사용

**권고 사항**:
```
본 매크로는 내부 운영 및 업무 효율화 목적으로 개발되었습니다.
상업적 이용 시 법률 전문가의 검토를 권장합니다.
요기요 서비스의 이용약관을 준수하여 사용하시기 바랍니다.
```

---

## 12. 마일스톤 및 일정

### 전체 일정 개요

| 단계 | 기간 | 담당 | 주요 활동 |
|------|------|------|-----------|
| **M1: 요구사항 정리** | 1일 | PM | PRD 작성 및 검토 |
| **M2: 기본 크롤링 PoC** | 2일 | 개발자 | 단일 사업자번호 조회 테스트 |
| **M3: Sheets 연동 및 반복** | 3일 | 개발자 | E/W열 연동, 반복 처리 구현 |
| **M4: 에러 핸들링 보완** | 2일 | 개발자 | 재시도 로직, 로그, 요약 통계 |
| **M5: 내부 테스트** | 2일 | QA | 100건 이상 실제 데이터 테스트 |
| **M6: 파라미터 튜닝** | 1일 | 개발자 | 대기 시간, 딜레이 최적화 |
| **Total** | **11일** | | |

### 마일스톤 상세

#### M1: 요구사항 정리 및 PRD 확정 (1일)
**목표**:
- PRD 문서 완성 및 이해관계자 검토
- 기술 스택 확정
- 개발 환경 설정

**산출물**:
- ✅ PRD 문서 (본 문서)
- ✅ 기술 스택 확정
- ✅ 개발 환경 준비 (Python 3.10+, Chrome)

---

#### M2: 기본 크롤링 PoC (2일)
**목표**:
- 요기요 페이지 접속 및 단일 사업자번호 조회 성공
- 결과 메시지 파싱 검증

**주요 작업**:
- Selenium + ChromeDriver 설정
- 요기요 URL 접속 테스트
- 사업자번호 입력 필드 셀렉터 확인
- 조회 버튼 클릭 테스트
- 결과 메시지 추출 및 파싱

**산출물**:
- ✅ `yogiyo_checker.py` (기본 버전)
- ✅ 3가지 상태 메시지 파싱 로직 검증
- ✅ 셀렉터 백업 전략 구현

**테스트 케이스**:
1. 이미 등록된 사업자번호 조회 → "이미 등록된..." 메시지 확인
2. 미등록 사업자번호 조회 → "입점신청 가능..." 메시지 확인
3. 9자리 사업자번호 조회 → "사업자 번호를..." 메시지 확인

---

#### M3: Google Sheets 연동 및 반복 처리 구현 (3일)
**목표**:
- Google Sheets API 연동 완료
- E열 읽기, W열 쓰기 구현
- 반복 처리 루프 구현

**주요 작업**:
- Service Account 설정 및 인증
- `GoogleSheetsClient` 클래스 구현
- E열 데이터 읽기 메서드
- W열 데이터 쓰기 메서드 (단일/배치)
- 반복 루프 및 진행 로그 구현

**산출물**:
- ✅ `google_sheets_client.py`
- ✅ `main.py` (CLI 인터페이스)
- ✅ 시작/종료 행 지정 기능

**테스트 케이스**:
1. 10개 사업자번호 조회 → W열에 결과 정상 기록 확인
2. 시작 행 5, 종료 행 10 지정 → 5~10행만 처리 확인
3. 빈 사업자번호 행 스킵 확인

---

#### M4: 에러 핸들링 및 로그/요약 출력 보완 (2일)
**목표**:
- 안정적인 에러 핸들링 구현
- 상세 로그 및 요약 통계 출력

**주요 작업**:
- 재시도 로직 구현 (네트워크, API)
- 셀렉터 탐색 실패 처리
- 에러 행 기록 및 요약 출력
- 진행률 표시 개선
- 통계 카운트 (성공/실패/스킵/상태별)

**산출물**:
- ✅ `utils.py` (로깅, 통계 유틸리티)
- ✅ 재시도 로직 (지수 백오프)
- ✅ 요약 통계 출력 형식

**테스트 케이스**:
1. 네트워크 오류 시뮬레이션 → 3회 재시도 확인
2. 잘못된 셀렉터 사용 → 백업 셀렉터 시도 확인
3. 100개 처리 후 요약 통계 정확성 확인

---

#### M5: 내부 테스트 및 QA (2일)
**목표**:
- 실제 데이터로 대량 처리 테스트
- 버그 발견 및 수정

**테스트 시나리오**:
1. **소량 테스트**: 10개 사업자번호
2. **중량 테스트**: 100개 사업자번호
3. **대량 테스트**: 500개 사업자번호
4. **경계 케이스**:
   - 모두 빈 값
   - 모두 이미 처리됨
   - 모두 형식 오류
   - 혼합 상태

**검증 항목**:
- ✅ 처리 완료율 (95% 이상 목표)
- ✅ 에러 발생률 (5% 이하 목표)
- ✅ 평균 처리 시간 (3~5초/건)
- ✅ Sheets 기록 정확도 (100%)

---

#### M6: 파라미터 튜닝 및 최적화 (1일)
**목표**:
- 대기 시간 최적화
- 차단 방지 딜레이 조정

**튜닝 항목**:
- 페이지 로드 대기: 5초 → 최적값 찾기
- 버튼 클릭 후 대기: 3초 → 최적값 찾기
- 조회 간 딜레이: 0.5~1초 → 차단 안 되는 최소값

**산출물**:
- ✅ 최적화된 `config.py`
- ✅ 성능 테스트 리포트

---

## 13. 향후 확장 방향

### 단기 확장 (1~2개월)

#### E-01: GUI 버전 개발
**목표**: tkinter 기반 사용자 친화적 인터페이스 제공

**기능**:
- Sheet ID 입력 필드
- 시작/종료 행 설정 UI
- 시작/일시정지/중지 버튼
- 실시간 진행률 바
- 로그 출력 창 (색상 구분)
- 통계 요약 패널

**참고**: 네이버 전화번호 검색 프로그램의 GUI 구조 재사용

---

#### E-02: 자동 태깅 및 필터링
**목표**: 조회 결과를 기반으로 자동 분류

**기능**:
- "입점 가능" 사업자번호만 별도 시트로 복사
- 색상 태깅 (초록: 가능, 빨강: 등록됨, 노랑: 오류)
- 자동 정렬 (상태별)

---

#### E-03: 리포트 생성
**목표**: 조회 결과를 PDF/Excel 리포트로 출력

**기능**:
- 요약 통계 차트 (파이 차트, 막대 그래프)
- 에러 행 목록 및 원인 분석
- 처리 시간 분석 (시간대별 성능)

---

### 중기 확장 (3~6개월)

#### E-04: 배달의민족 통합 조회
**목표**: 요기요 외에 배달의민족 입점 여부도 조회

**기능**:
- 배민 사장님 사이트 크롤링 로직 추가
- 요기요/배민 결과를 별도 열에 기록 (W/X열)
- 통합 필터링 (둘 다 미입점, 하나만 입점 등)

---

#### E-05: 쿠팡이츠 통합 조회
**목표**: 쿠팡이츠 입점 여부 조회

---

#### E-06: 스케줄링 및 자동 실행
**목표**: 주기적으로 자동 조회

**기능**:
- 매일 특정 시간에 자동 실행 (cron)
- 신규 사업자번호 자동 감지 (E열 변경 감지)
- 결과를 이메일/슬랙으로 알림

---

### 장기 확장 (6개월+)

#### E-07: 클라우드 배포
**목표**: AWS Lambda, Google Cloud Functions 등으로 서버리스 배포

**장점**:
- 로컬 PC 없이 실행 가능
- 대량 처리 시 병렬 실행 (Lambda 동시 호출)

---

#### E-08: 웹 대시보드
**목표**: 웹 기반 관리 인터페이스

**기능**:
- 웹에서 Sheet ID 입력 및 실행
- 실시간 진행 상황 모니터링
- 과거 조회 이력 관리
- 사용자 권한 관리 (팀 단위)

---

#### E-09: AI 기반 사업자번호 추천
**목표**: 입점 성공률이 높은 사업자번호 우선 추천

**기능**:
- 과거 조회 데이터 분석
- 지역/업종별 입점 가능성 예측
- 영업 우선순위 자동 산정

---

## 부록

### A. 용어 정리

| 용어 | 설명 |
|------|------|
| **사업자번호** | 사업자등록번호 10자리 (예: 1234567890) |
| **입점** | 요기요 플랫폼에 가맹점으로 등록되는 것 |
| **Service Account** | Google API 인증 방식 중 하나 (OAuth 없이 서버 간 인증) |
| **셀렉터 (Selector)** | HTML 요소를 찾기 위한 CSS 선택자 |
| **CAPTCHA** | 자동화 봇을 방지하기 위한 사람 인증 시스템 |
| **Headless 모드** | 브라우저 창을 띄우지 않고 백그라운드에서 실행하는 모드 |

---

### B. 참고 자료

1. **네이버 전화번호 검색 프로그램 분석**: [참고자료_네이버크롤링분석.txt](./참고자료_네이버크롤링분석.txt)
2. **Selenium 공식 문서**: https://selenium-python.readthedocs.io/
3. **Google Sheets API 가이드**: https://developers.google.com/sheets/api/guides/concepts
4. **Python-dotenv**: https://pypi.org/project/python-dotenv/

---

### C. 환경 설정 예시

#### .env 파일
```bash
# Google Sheets 설정
GOOGLE_SHEET_ID=1A2B3C4D5E6F7G8H9I0J
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json

# 크롤링 설정
YOGIYO_URL=https://ceo.yogiyo.co.kr/join-request?event_type=ad&utm_source=yogiyo&utm_medium=portal&utm_campaign=partner&utm_content=up_btn
SEARCH_DELAY=1.0
PAGE_LOAD_WAIT=5
BUTTON_CLICK_WAIT=3

# 옵션 설정
SKIP_EXISTING=false
RESULT_FORMAT=MESSAGE
HEADLESS_MODE=false

# 열 위치
COLUMN_BUSINESS_NUMBER=E
COLUMN_RESULT=W
```

#### requirements.txt
```
selenium==4.27.1
webdriver-manager==4.0.2
google-api-python-client==2.154.0
google-auth==2.36.0
google-auth-oauthlib==1.2.1
google-auth-httplib2==0.2.0
python-dotenv==1.0.1
```

---

### D. 실행 예시

#### 터미널 실행
```bash
$ python main.py

================================================================================
요기요 입점 여부 사업자번호 조회 매크로 v1.0
================================================================================

조회할 Google 스프레드시트 ID를 입력하세요:
> 1A2B3C4D5E6F7G8H9I0J

시작 행 (기본값 3):
> 3

종료 행 (0=끝까지):
> 0

⚠️  스프레드시트를 "링크가 있는 모든 사용자 - 편집자"로 공유하세요!

[INFO] Google Sheets API 연결 중...
[OK] Google Sheets API 연결 완료
[INFO] E열 데이터 읽기 중...
[OK] 500개 사업자번호 읽기 완료

[INFO] Chrome 브라우저 실행 중...
[OK] 브라우저 실행 완료
[INFO] 요기요 페이지 접속 중...
[OK] 페이지 로드 완료

================================================================================
조회 시작
================================================================================

[3/500] Row 3: 1234567890
  → 입력 완료
  → 조회 버튼 클릭
  → 결과: "입점신청 가능한 사업자번호입니다"
  → W3 저장 완료
  ✓ [SUCCESS] Row 3 processed (3.2초 소요)

Progress: 3/500 (0.6%)
Processed: 3 | Success: 3 | Failed: 0 | Skipped: 0
Available: 2 | Registered: 1 | Invalid: 0

...

================================================================================
처리 완료!
================================================================================
총 처리 행: 500
  - 성공: 485
  - 실패: 10
  - 스킵: 5

상태별 집계:
  - 입점 가능 (AVAILABLE): 320
  - 이미 입점 (REGISTERED): 150
  - 번호 오류 (INVALID): 15
  - 알 수 없음 (UNKNOWN): 0

에러 발생 행: [15, 87, 203, 401, 456, 478, 489, 490, 492, 500]
총 소요 시간: 26분 42초
평균 처리 시간: 3.21초/건
================================================================================
```

---

## 문서 변경 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| v1.0 | 2025-01-16 | bjcho9542-hash | 최초 작성 |

---

**문서 끝**
