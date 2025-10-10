import qrcode
from io import BytesIO
from PIL import Image


def generate_wifi_qr(ssid: str, password: str, security: str = "WPA") -> BytesIO:
    """
    Wi-Fi QR 코드를 생성합니다.

    Args:
        ssid: Wi-Fi 네트워크 이름
        password: Wi-Fi 비밀번호
        security: 보안 타입 (WPA/WPA2)

    Returns:
        BytesIO: PNG 이미지 데이터
    """
    wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};;"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(wifi_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((600, 600), Image.Resampling.LANCZOS)

    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer




