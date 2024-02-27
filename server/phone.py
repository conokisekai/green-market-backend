import http.client
import json
import pyotp
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def send_otp(phone_number, username):
    logging.debug("Sending OTP...")
    key = "AMAROWENFAITHKHALIDCONRADJIMJOHNWILLY"
    totp = pyotp.TOTP(key, interval=180)  # Use a 30-second interval for TOTP
    conn = http.client.HTTPSConnection("e19152.api.infobip.com")

    payload = json.dumps(
        {
            "messages": [
                {
                    "destinations": [{"to": phone_number}],
                    "from": "ServiceSMS",
                    "text": f"Agri-Soko 🥀,\n\nThis is a message from Agri-Soko Team 👨‍🌾 \n\n{username}, your OTP is {totp.now()}.",
                }
            ]
        }
    )

    headers = {
        "Authorization": "App 725fe5e9b12501a74dfc3b65f518da10-cfc9f7cb-0a02-497c-8f53-234460a5d066",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        conn.request("POST", "/sms/2/text/advanced", payload, headers)
        res = conn.getresponse()
        data = res.read()
        logging.debug(data.decode("utf-8"))

        # Log success
        if res.status == 200:
            otp_value = totp.now()
            logging.info(f"OTP sent successfully to {phone_number}: {otp_value}")
            return otp_value
        else:
            logging.error(
                f"Failed to send OTP to {phone_number}: {res.status} - {res.reason}"
            )
            return None
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None
