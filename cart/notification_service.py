from twilio.rest import Client
import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from dotenv import load_dotenv
from queue import Queue
import time

load_dotenv(".env")


class NotificationService:
    message_queue = Queue()
    to_email = os.getenv('JOSRAM_EMAIL')
    to_sms = os.getenv('JOSRAM_NUMBER')
    

class ServiceSMS(NotificationService):
    
    def __init__(self, twilio_sid, twilio_token, twilio_number):
        self.__account_sid = twilio_sid #os.getenv('TWILIO_ACCOUNT_SID')
        self.__auth_token = twilio_token #os.getenv('TWILIO_AUTH_TOKEN')
        self.__twilio_number = twilio_number
    
    def send_message(self, body):
           
        client = Client(self.__account_sid, self.__auth_token)

        message = client.messages \
                        .create(
                            body=body,
                            from_=self.__twilio_number,#'+13374920319',
                            to=NotificationService.to_sms #os.getenv('JOSRAM_NUMBER')
                        )
        return message.sid

class ServiceEmail(NotificationService):
    
    def send_message(self, subject:str, template:str, destination:str, context:dict):
        subject = subject
        template_name = template
        context = {
                "carts": context["carts"],
                "payer": context["payer"],
                "merchand_order": context["merchand_order"],
                "sum_prices": context["sum_prices"],
                "cost_shipments": context["cost_shipments"]
            }
        sender_email = NotificationService.to_email #os.getenv('JOSRAM_EMAIL')
        recipient_emails = [NotificationService.to_email, destination]  #[os.getenv('JOSRAM_EMAIL'), destination]
        html_message = render_to_string(template_name, context)
        send_mail(subject, '', sender_email, recipient_emails, html_message=html_message)


sms = ServiceSMS(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'), '+13374920319')
email = ServiceEmail() 
        
def sms_queue():
    queue = sms.message_queue 
    while True:
        if not queue.empty():
            body = queue.get()
            sms.send_message(body)
            queue.task_done()  
            print("sms enviado")  
        time.sleep(1)
        
def email_queue():
    queue = email.message_queue 
    while True:
        if not queue.empty():
            
            item = queue.get()
            if isinstance(item, tuple) and len(item) == 4:
                
                subject, template, destination, context = item
                
                email.send_message(subject, template, destination, context)
                queue.task_done()
                print("email enviado")  
        time.sleep(1)