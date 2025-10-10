import os
import json

# Google Drive 설정
# 본인의 Google Drive에서 폴더를 생성하고 Service Account와 공유한 후
# 해당 폴더의 ID를 여기에 입력하세요

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

# 폴더 생성 및 공유 방법:
# 1. Google Drive에 접속하여 "QR_Codes" 폴더 생성
# 2. 폴더 우클릭 → 공유 → {SERVICE_ACCOUNT_EMAIL} 추가
# 3. 권한을 "편집자"로 설정
# 4. 폴더를 열고 URL에서 폴더 ID 복사
#    예: https://drive.google.com/drive/folders/[여기가_폴더_ID]

# 아래에 폴더 ID를 입력하세요
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '')

# 폴더 ID가 설정되지 않은 경우 경고
if not GOOGLE_DRIVE_FOLDER_ID:
    print("⚠️  경고: GOOGLE_DRIVE_FOLDER_ID가 설정되지 않았습니다.")
    print("   backend/config.py 파일에서 GOOGLE_DRIVE_FOLDER_ID를 설정하거나")
    print("   환경 변수로 설정해주세요.")
    print(f"   Service Account 이메일: {SERVICE_ACCOUNT_EMAIL}")

