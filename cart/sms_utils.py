
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv(".env")

def send_sms(message):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=message,
                        from_='+13374920319',
                        to=os.getenv('JOSRAM_NUMBER')
                    )

    return message.sid