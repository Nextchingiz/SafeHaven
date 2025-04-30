import smtplib
import ssl
from providers import PROVIDERS

def send_message(number: str, message: str, provider: str, sender_credentials: tuple, subject: str = "SafeHaven Update", smtp_server: str = "smtp.gmail.com", smtp_port: int = 465):
    sender_email, email_password = sender_credentials

    provider_info = PROVIDERS.get(provider)
    if provider_info is None or "sms" not in provider_info:
        raise ValueError(f"Invalid provider or missing SMS gateway for provider: {provider}")
    
    receiver_email = f"{number}@{provider_info['sms']}"
    email_message = f"Subject:{subject}\nTo:{receiver_email}\n\n{message}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

def MESSAGE(time:str, alert_type:str, number:str):
    if number.len() == 10:
        number = number
    else:
        print("Improper Number")
    
    message = f"There was {alert_type} at {time}"
    provider = "AT&T"
    sender_credentials = ("thesafehaven0@gmail.com", "cmfb uxnk nwcn ngch")

    send_message(number, message, provider, sender_credentials)
