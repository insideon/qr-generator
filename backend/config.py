import os
import json
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Google Drive 설정
# 본인의 Google Drive에서 폴더를 생성하고 Service Account와 공유한 후
# .env 파일에 폴더 ID를 설정하세요

# Service Account 이메일 자동 읽기
def get_service_account_email():
    """service-account.json에서 client_email을 읽어옵니다."""
    try:
        credentials_path = os.path.join(
            os.path.dirname(__file__),
            'credentials',
            'service-account.json'
        )
        if os.path.exists(credentials_path):
            with open(credentials_path, 'r') as f:
                data = json.load(f)
                return data.get('client_email', '서비스계정이메일@프로젝트.iam.gserviceaccount.com')
    except Exception:
        pass
    return '서비스계정이메일@프로젝트.iam.gserviceaccount.com'

SERVICE_ACCOUNT_EMAIL = get_service_account_email()

# Google Drive 폴더 ID (환경 변수에서 로드)
# 설정 방법:
# 1. cp env.example .env (예제 파일 복사)
# 2. Google Drive에 "QR_Codes" 폴더 생성
# 3. 폴더 공유 → Service Account 이메일 추가 (편집자 권한)
#    Service Account 이메일: {SERVICE_ACCOUNT_EMAIL}
# 4. .env 파일에 GOOGLE_DRIVE_FOLDER_ID=폴더ID 입력
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '')

# 폴더 ID가 설정되지 않은 경우 경고
if not GOOGLE_DRIVE_FOLDER_ID:
    print("⚠️  경고: GOOGLE_DRIVE_FOLDER_ID가 설정되지 않았습니다.")
    print("   backend/.env 파일을 생성하고 GOOGLE_DRIVE_FOLDER_ID를 설정해주세요.")
    print(f"   Service Account 이메일: {SERVICE_ACCOUNT_EMAIL}")
    print("   env.example 파일을 참고하세요.")

