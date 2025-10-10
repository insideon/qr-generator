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

    # Service Account의 드라이브에 파일 생성 (parents 없이)
    file_metadata = {
        'name': filename,
        'mimeType': 'image/png'
    }

    media = MediaIoBaseUpload(
        image_buffer,
        mimetype='image/png',
        resumable=False,
        chunksize=-1
    )

    # 파일 생성
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    file_id = file.get('id')

    # 파일을 공개로 설정하고 링크로 접근 가능하게 함
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(
        fileId=file_id,
        body=permission
    ).execute()

    # 파일을 사용자의 폴더로 복사 시도
    try:
        copied_file = service.files().copy(
            fileId=file_id,
            body={
                'name': filename,
                'parents': [GOOGLE_DRIVE_FOLDER_ID]
            },
            supportsAllDrives=True
        ).execute()

        # 복사 성공시 원본 삭제
        service.files().delete(fileId=file_id).execute()
        return copied_file.get('id')
    except Exception as copy_error:
        # 복사 실패시 원본 파일 ID 반환 (Service Account 드라이브에 있음)
        print(f"폴더 복사 실패: {copy_error}")
        return file_id


