import base64
import io

import qrcode
from django.contrib.gis.geoip2 import GeoIP2


def create_qrcode(link):
    qr = qrcode.QRCode(version=1, box_size=9, border=1)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qrcode_png_data = base64.b64encode(buffer.read()).decode("utf-8")

    return qrcode_png_data


def get_country(request):
    try:
        g = GeoIP2()
        remote_addr = request.META.get("HTTP_X_FORWARDED_FOR")
        if remote_addr:
            address = remote_addr.split(",")[-1].strip()
        else:
            address = request.META.get("REMOTE_ADDR")
        country = g.country_name(address)
        return country
    except Exception as e:
        print(e)
        return None


def get_language(languages):
    return languages.split(";")[0].split("-")[0]


def get_user_agent_info(user_agent):
    browser = user_agent.browser.family
    operating_system = user_agent.os.family

    device_type = None
    if user_agent.is_mobile:
        device_type = "Mobile"
    elif user_agent.is_tablet:
        device_type = "Tablet"
    elif user_agent.is_pc:
        device_type = "PC"

    is_bot = False
    if user_agent.is_bot:
        is_bot = True

    return {
        "device_type": device_type,
        "operating_system": operating_system,
        "browser": browser,
        "is_bot": is_bot,
    }
