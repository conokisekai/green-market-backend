import http.client
import json
import pyotp

key = "AMAROWENFAITHKHALIDCONRADJIMJOHNWILLY"
totp = pyotp.TOTP(key)
hotp = pyotp.HOTP(key)

conn = http.client.HTTPSConnection("5y2v5g.api.infobip.com")


name = "Anyone" 

payload = json.dumps(
    {
        "messages": [
            {
                "destinations": [
                    {"to": "254705780000"},
                    {"to": "254712764067"},
                    {"to": "254721601031"},
                    {"to": "254710224989"},
                ],
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
print(data.decode("utf-8"))
