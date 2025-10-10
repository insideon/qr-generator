import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.qr_generator import generate_wifi_qr
from services.drive_uploader import upload_to_drive


app = FastAPI(title="Wi-Fi QR Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QRRequest(BaseModel):
    store_name: str
    ssid: str
    security: str = "WPA"
    password: str


class QRResponse(BaseModel):
    image_base64: str
    drive_file_id: str
    message: str
    drive_status: str = "success"  # success, warning, error
    drive_message: str = ""


@app.get("/")
async def root():
    return {"message": "Wi-Fi QR Generator API"}


@app.post("/api/generate-qr", response_model=QRResponse)
async def generate_qr(request: QRRequest):
    """
    Wi-Fi QR 코드를 생성하고 Google Drive에 저장을 시도합니다.
    """
    try:
        # QR 코드 생성 (항상 성공)
        qr_buffer = generate_wifi_qr(
            ssid=request.ssid,
            password=request.password,
            security=request.security
        )

        qr_buffer_copy = qr_buffer.getvalue()
        image_base64 = base64.b64encode(qr_buffer_copy).decode('utf-8')

        # Google Drive 업로드 시도 (실패해도 QR 코드는 제공)
        drive_file_id = ""
        drive_status = "success"
        drive_message = ""

        try:
            from io import BytesIO
            upload_buffer = BytesIO(qr_buffer_copy)
            drive_file_id = upload_to_drive(upload_buffer, request.store_name)
            drive_status = "success"
            drive_message = "Google Drive에 저장되었습니다."
        except ValueError as value_error:
            # 설정 관련 오류 (폴더 ID 미설정 등)
            error_msg = str(value_error)
            print(f"⚠️ Google Drive 설정 오류: {error_msg}")
            drive_status = "warning"
            drive_message = error_msg
        except FileNotFoundError as file_error:
            # 인증 파일 없음
            error_msg = str(file_error)
            print(f"⚠️ Google Drive 인증 파일 오류: {error_msg}")
            drive_status = "warning"
            drive_message = error_msg
        except Exception as drive_error:
            # 기타 Drive 저장 실패
            error_msg = str(drive_error)
            print(f"⚠️ Google Drive 저장 실패: {error_msg}")

            drive_status = "warning"
            # 에러 원인 간단히 요약
            if "storage quota" in error_msg.lower() or "403" in error_msg:
                drive_message = "폴더 접근 권한이 없습니다. Service Account 이메일을 폴더에 공유(편집자 권한)했는지 확인하세요."
            elif "404" in error_msg or "not found" in error_msg.lower():
                drive_message = "폴더를 찾을 수 없습니다. 폴더 ID가 올바른지, Service Account와 폴더를 공유했는지 확인하세요."
            elif "credentials" in error_msg.lower():
                drive_message = "인증 파일이 없거나 잘못되었습니다. service-account.json 파일을 확인하세요."
            else:
                drive_message = error_msg

        return QRResponse(
            image_base64=image_base64,
            drive_file_id=drive_file_id,
            message="QR 코드가 성공적으로 생성되었습니다!",
            drive_status=drive_status,
            drive_message=drive_message
        )

    except Exception as e:
        # QR 코드 생성 자체가 실패한 경우만 에러
        error_message = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"QR 코드 생성 중 오류가 발생했습니다: {error_message}"
        )


