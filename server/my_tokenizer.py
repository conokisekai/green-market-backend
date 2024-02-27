import os
import json
import logging
import secrets
from datetime import datetime, timedelta
from mailjet_rest import Client

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def generate_token():
    token = secrets.token_urlsafe(6)
    expiration_time = datetime.now() + timedelta(minutes=3)
    return token, expiration_time


def send_token(email, username):
    logging.debug("Sending token...")
    token, expiration_time = generate_token()
    api_key = os.getenv("MAILJET_API_KEY")
    api_secret = os.getenv("MAILJET_API_SECRET")
    mailjet = Client(auth=(api_key, api_secret), version="v3.1")

    message = {
        "Messages": [
            {
                "From": {"Email": "your_email@example.com", "Name": "Agri-Soko Team"},
                "To": [{"Email": email, "Name": username}],
                "Subject": "Agri-Soko Token",
                "TextPart": f"Hello {username}, your token is {token}.",
                "HTMLPart": f"<h3>Hello {username},</h3><p>Your token is {token}.</p>",
            }
        ]
    }

    try:
        response = mailjet.send.create(data=message)
        logging.debug(json.dumps(response.json(), indent=2))
        return token  # Return the token if the email is sent successfully
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
