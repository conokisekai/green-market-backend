import http.client
import json
import pyotp


def send_otp(phone_number):
    print("Sending OTP...")  # Add this line for debugging
    key = "AMAROWENFAITHKHALIDCONRADJIMJOHNWILLY"
    totp = pyotp.TOTP(key)
    conn = http.client.HTTPSConnection("5y2v5g.api.infobip.com")

    name = "Anyone"

    payload = json.dumps(
        {
            "messages": [
                {
                    "destinations": [{"to": phone_number}],
                    "from": "ServiceSMS",
                    "text": f"Agri-Soko 🥀,\n\nThis is a message from Agri-Soko Team 👨‍🌾 \n\n{name} your OTP is {totp.now()}. ",
                }
            ]
        }
    )

    headers = {
        "Authorization": "App 5fc7ab255439b9869822123d397670ce-90bd0e5d-2226-4758-aadd-216c74262580",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    conn.request("POST", "/sms/2/text/advanced", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))  # Print response for debugging
