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
        drive_status = ""

        try:
            from io import BytesIO
            upload_buffer = BytesIO(qr_buffer_copy)
            drive_file_id = upload_to_drive(upload_buffer, request.store_name)
            drive_status = "📁 Drive 저장 성공"
        except Exception as drive_error:
            # Drive 저장 실패는 로그만 남기고 계속 진행
            print(f"⚠️ Google Drive 저장 실패: {drive_error}")
            drive_status = "⚠️ Drive 저장 실패"

        return QRResponse(
            image_base64=image_base64,
            drive_file_id=drive_file_id,
            message=f"✅ QR 코드 생성 성공! {drive_status}"
        )

    except Exception as e:
        # QR 코드 생성 자체가 실패한 경우만 에러
        error_message = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"QR 코드 생성 중 오류가 발생했습니다: {error_message}"
        )


