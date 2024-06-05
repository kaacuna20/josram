from django.core.mail import send_mail
from django.template.loader import render_to_string
from dotenv import load_dotenv
import os

load_dotenv(".env")

def send_email(subject:str, template:str, destination:str, context:dict):

    subject = subject
    template_name = template
    context = {
            "carts": context["carts"],
            "payer": context["payer"],
            "merchand_order": context["merchand_order"],
            "sum_prices": context["sum_prices"],
            "cost_shipments": context["cost_shipments"]
        }
    sender_email = os.getenv('JOSRAM_EMAIL')
    recipient_emails = [os.getenv('JOSRAM_EMAIL'), destination]
    html_message = render_to_string(template_name, context)
    send_mail(subject, '', sender_email, recipient_emails, html_message=html_message)