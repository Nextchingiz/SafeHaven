import email, smtplib, ssl
from providers import PROVIDERS

def send_message(number:str, message:str, provider:str, sender_credentials:tuple, subject:str = "SafeHaven Update", smtp_server = "smtp.gmail.com", smtp_port:int = 465):
    sender_email, email_password = sender_credentials
    receiver_email = f"{number}@{PROVIDERS.get(provider).get("sms")}"

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context = ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

def main():
    number = "3186131760"
    message = "There was an alert"
    provider = "AT&T"

    sender_credentials = ("thesafehaven0@gmail.com", "cmfb uxnk nwcn ngch")
    send_message(number, message, provider, sender_credentials)


main()