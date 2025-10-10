# Wi-Fi QR 코드 생성기

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/qr-generator)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61dafb.svg)](https://reactjs.org/)

식당 사장님들을 위한 Wi-Fi 접속용 QR 코드 생성 서비스입니다. 간단한 정보 입력만으로 QR 코드를 생성하고 즉시 다운로드할 수 있습니다. Google Workspace 계정이 있다면 Google Drive에 자동 백업도 가능합니다.

## 주요 기능

- ✨ 간편한 Wi-Fi QR 코드 생성 (600×600 PNG)
- 🔒 WPA/WPA2 보안 지원
- 📱 즉시 다운로드 가능
- ☁️ Google Drive 자동 백업 (Google Workspace 계정 필요)
- 🚫 로그인/계정 불필요 (개인 Gmail 사용자도 QR 생성/다운로드 가능)
- 📲 반응형 웹 디자인

## 기술 스택

### 백엔드
- Python 3.13+
- FastAPI 0.115.0
- Uvicorn 0.32.0
- qrcode 8.0
- Pillow 11.0.0
- Google API Python Client 2.149.0
- Google Auth 2.35.0

### 프론트엔드
- React 18.2.0
- Vite 5.0.8
- Axios 1.6.2

## 설치 및 실행 방법

### 1. Google Cloud 및 Drive 설정

QR 코드를 Google Drive에 저장하려면 Service Account와 공유 폴더 설정이 필요합니다.

#### 1-1. Service Account 생성

1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. 새 프로젝트 생성
3. **Google Drive API 활성화**:
   - API 및 서비스 > 라이브러리 > "Google Drive API" 검색 후 활성화
4. **Service Account 생성**:
   - API 및 서비스 > 사용자 인증 정보 > 사용자 인증 정보 만들기 > 서비스 계정
   - 서비스 계정 이름 입력 (예: "wifi-qr-generator")
   - 역할은 선택하지 않아도 됨
   - 완료 버튼 클릭
5. **JSON 키 생성**:
   - 생성된 서비스 계정 클릭
   - 키 탭 선택
   - 키 추가 > 새 키 만들기 > JSON 선택
   - 다운로드된 JSON 파일을 `backend/credentials/service-account.json`으로 저장
6. **Service Account 이메일 확인**:
   - 서비스 계정 목록에서 이메일 주소 확인
   - 예: `wifi-qr-generator@your-project.iam.gserviceaccount.com`
   - 이 이메일은 나중에 Drive 폴더 공유 시 사용됩니다

#### 1-2. Google Drive 폴더 설정

⚠️ **중요 - Google Drive 제한사항**:

**Service Account는 개인 Gmail 계정의 드라이브에 파일을 생성할 수 없습니다.**

이것은 Google의 정책이며, 다음 두 가지 방법만 가능합니다:

1. **Google Workspace 계정** 사용 (유료)
   - Shared Drive (공유 드라이브) 기능 이용
   - Service Account가 파일 생성 가능

2. **OAuth 2.0 인증** 사용
   - 사용자가 Google 로그인하여 권한 부여
   - 로그인 필요 (현재 프로젝트의 "무계정" 요구사항과 맞지 않음)

**현재 상태**: QR 코드 생성 및 다운로드는 정상 작동하며, Google Drive 저장 기능은 위 조건 충족 시 사용 가능합니다.

---

#### Google Workspace 계정용 설정 (Google Drive 저장 가능)

Google Workspace 계정을 사용 중이라면 다음 단계를 따라 Shared Drive를 설정하세요:

1. **Shared Drive (공유 드라이브) 생성**:
   - Google Drive 좌측 메뉴 > 공유 드라이브 > 새로 만들기
   - 이름: "QR_Codes"

2. **Service Account 멤버 추가**:
   - 공유 드라이브 우클릭 > 멤버 관리
   - 멤버 추가: Service Account 이메일 입력
   - 권한: **콘텐츠 관리자** 또는 **관리자** 선택

3. **공유 드라이브 ID 복사**:
   - 공유 드라이브를 열고 URL에서 ID 복사
   - 예: `https://drive.google.com/drive/folders/0Axxx...`

4. **환경 변수 설정**:
   ```bash
   cd backend
   cp env.example .env
   # .env 파일 편집
   ```
   `.env` 파일:
   ```
   GOOGLE_DRIVE_FOLDER_ID=공유드라이브ID
   ```

---

#### 개인 Gmail 계정용 (Drive 저장 불가 - 대안 제공)

개인 Gmail 계정을 사용 중이라면 Google Drive 저장은 작동하지 않습니다.

**현재 사용 가능한 기능**:
- ✅ Wi-Fi QR 코드 생성
- ✅ 화면에서 미리보기
- ✅ 즉시 다운로드

**Google Drive 저장을 원한다면**:
- Google Workspace 계정으로 업그레이드
- 또는 OAuth 2.0 로그인 방식으로 개발 요청 (Issue 등록)

### 2. 백엔드 실행

```bash
cd backend

# 가상환경 생성 (권장)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

백엔드는 `http://localhost:8000`에서 실행됩니다.

### 3. 프론트엔드 실행

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드는 `http://localhost:3000`에서 실행됩니다.

### 4. 브라우저에서 접속

`http://localhost:3000`으로 접속하여 QR 코드를 생성할 수 있습니다.

## 사용 방법

1. 매장명 입력
2. Wi-Fi 이름(SSID) 입력
3. 보안 타입 선택 (WPA/WPA2)
4. Wi-Fi 비밀번호 입력
5. "QR 코드 생성" 버튼 클릭
6. 생성된 QR 코드 미리보기 확인
7. "다운로드" 버튼으로 이미지 저장

생성된 QR 코드는 즉시 다운로드할 수 있으며, Google Workspace 계정에서 Shared Drive를 설정한 경우 자동으로 `{매장명}_{날짜시간}.png` 형식으로 저장됩니다.

## 프로젝트 구조

```
qr-generator/
├── backend/
│   ├── main.py                 # FastAPI 애플리케이션
│   ├── requirements.txt        # Python 의존성
│   ├── services/
│   │   ├── qr_generator.py    # QR 코드 생성 로직
│   │   └── drive_uploader.py  # Google Drive 업로드
│   └── credentials/
│       └── service-account.json  # Google Service Account 키 (직접 추가)
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx            # 메인 컴포넌트
│       ├── main.jsx
│       └── index.css
└── README.md
```

## API 엔드포인트

### POST `/api/generate-qr`

Wi-Fi QR 코드를 생성합니다.

**요청 본문:**
```json
{
  "store_name": "스타벅스 강남점",
  "ssid": "StarbucksWiFi",
  "security": "WPA",
  "password": "password123"
}
```

**응답:**
```json
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "drive_file_id": "1abc123def456...",
  "message": "QR 코드가 성공적으로 생성되었습니다."
}
```

## 주의사항

### 보안
- ⚠️ Service Account 키 파일(`service-account.json`)은 민감한 정보입니다
- `.gitignore`에 이미 포함되어 있으니 Git 커밋 시 자동 제외됩니다
- 절대로 공개 저장소에 업로드하지 마세요

### Google Drive 제한사항
- **개인 Gmail 계정**: Service Account로 파일 생성 불가 (Google 정책)
  - QR 생성 및 다운로드는 정상 작동
  - Google Drive 저장 기능만 사용 불가
- **Google Workspace 계정**: Shared Drive에서 정상 작동

### 기타
- 생성된 QR 코드는 페이지 이탈 후 서비스 내에서 재조회할 수 없습니다
- Google Drive에 저장된 파일은 계속 보존됩니다 (Workspace 계정 사용 시)

## 버전 히스토리

### v1.0.0 (2025-10-10)
- 초기 릴리스
- Wi-Fi QR 코드 생성 기능
- Google Drive 자동 저장 기능
- 반응형 웹 UI
- 즉시 다운로드 기능

## 시스템 요구사항

- **운영체제**: macOS, Linux, Windows
- **Python**: 3.13 이상
- **Node.js**: 18.0 이상
- **브라우저**: Chrome, Firefox, Safari, Edge (최신 버전)

## 라이선스

MIT License


