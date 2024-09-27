import secrets
from datetime import datetime
from datetime import timedelta

import qrcode
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers.svg import SvgPathCircleDrawer

from triangler_fastapi.config import HOST_NAME
from triangler_fastapi.config import OBSERVATION_TOKEN_EXPIRY_DAYS
from triangler_fastapi.config import OBSERVATION_TOKEN_LENGTH


def generate_unique_token() -> str:
    return secrets.token_urlsafe(OBSERVATION_TOKEN_LENGTH)


def calculate_expiry_date(n_days: int = OBSERVATION_TOKEN_EXPIRY_DAYS) -> datetime:
    return datetime.now() + timedelta(days=n_days)


def generate_qr_code_svg(token: str) -> str:
    qrcode_url = f"https://{HOST_NAME}/observation/response/{token}"
    return (
        qrcode.make(qrcode_url, module_drawer=SvgPathCircleDrawer)
        .get_image()
        .get_svg_str()
    )


def generate_qr_code_png(token: str) -> str:
    qrcode_url = f"https://{HOST_NAME}/observation/response/{token}"
    return qrcode.make(qrcode_url, module_drawer=RoundedModuleDrawer).get_image()
