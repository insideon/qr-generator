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
    Wi-Fi QR 코드를 생성하고 Google Drive에 저장합니다.
    """
    try:
        qr_buffer = generate_wifi_qr(
            ssid=request.ssid,
            password=request.password,
            security=request.security
        )

        qr_buffer_copy = qr_buffer.getvalue()

        from io import BytesIO
        upload_buffer = BytesIO(qr_buffer_copy)
        drive_file_id = upload_to_drive(upload_buffer, request.store_name)

        image_base64 = base64.b64encode(qr_buffer_copy).decode('utf-8')

        return QRResponse(
            image_base64=image_base64,
            drive_file_id=drive_file_id,
            message="QR 코드가 성공적으로 생성되었습니다."
        )

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        error_message = str(e)
        if "credentials" in error_message.lower() or "auth" in error_message.lower():
            detail = f"Google Drive 인증 오류: {error_message}\nREADME.md를 참고하여 Service Account를 설정해주세요."
        else:
            detail = f"QR 코드 생성 중 오류가 발생했습니다: {error_message}"

        raise HTTPException(status_code=500, detail=detail)


