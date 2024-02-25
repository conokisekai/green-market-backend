import http.client
import json
import secrets
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Dictionary to store tokens and their expiration times
token_dict = {}


def generate_token():
    token = secrets.token_urlsafe(6)
    expiration_time = datetime.now() + timedelta(minutes=3)
    return token, expiration_time


def send_token(phone_number, username):
    logging.debug("Sending token...")
    if phone_number in token_dict and datetime.now() < token_dict[phone_number][1]:
        token = token_dict[phone_number][0]
    else:
        token, expiration_time = generate_token()
        token_dict[phone_number] = (token, expiration_time)

    conn = http.client.HTTPSConnection("e19152.api.infobip.com")

    payload = json.dumps(
        {
            "messages": [
                {
                    "destinations": [{"to": phone_number}],
                    "from": "ServiceSMS",
                    "text": f"Agri-Soko 🥀,\n\nThis is a message from Agri-Soko Team 👨‍🌾 \n\n{username}, your token is {token}.",
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
        return token  # Return the token if the SMS is sent successfully
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
