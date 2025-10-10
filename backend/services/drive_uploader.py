import os
from datetime import datetime
from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import sys

# config 파일에서 설정 가져오기
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import GOOGLE_DRIVE_FOLDER_ID, SERVICE_ACCOUNT_EMAIL


SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'credentials',
    'service-account.json'
)


def upload_to_drive(image_buffer: BytesIO, store_name: str) -> str:
    """
    Google Drive에 QR 코드 이미지를 업로드합니다.

    Args:
        image_buffer: PNG 이미지 데이터
        store_name: 매장명

    Returns:
        str: Drive 파일 ID
    """
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"Google Service Account 인증 파일을 찾을 수 없습니다.\n"
            f"경로: {CREDENTIALS_PATH}\n"
            f"Google Cloud Console에서 service-account.json 파일을 생성하여 위 경로에 저장해주세요.\n"
            f"자세한 설정 방법은 README.md를 참고하세요."
        )

    if not GOOGLE_DRIVE_FOLDER_ID:
        raise ValueError(
            f"Google Drive 폴더 ID가 설정되지 않았습니다.\n"
            f"backend/config.py 파일에서 GOOGLE_DRIVE_FOLDER_ID를 설정해주세요.\n\n"
            f"설정 방법:\n"
            f"1. Google Drive에 접속하여 폴더 생성 (예: QR_Codes)\n"
            f"2. 폴더 공유 → {SERVICE_ACCOUNT_EMAIL} 추가 (편집자 권한)\n"
            f"3. 폴더 URL에서 폴더 ID 복사\n"
            f"4. backend/config.py의 GOOGLE_DRIVE_FOLDER_ID에 입력"
        )

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )

    service = build('drive', 'v3', credentials=credentials)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{store_name}_{timestamp}.png"

    # 공유 폴더에 직접 파일 생성
    file_metadata = {
        'name': filename,
        'mimeType': 'image/png',
        'parents': [GOOGLE_DRIVE_FOLDER_ID]  # 공유 폴더에 직접 생성
    }

    media = MediaIoBaseUpload(
        image_buffer,
        mimetype='image/png',
        resumable=False,
        chunksize=-1
    )

    # 파일 생성 (공유 폴더에 직접 생성하므로 storage quota 문제 없음)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    ).execute()

    return file.get('id')


