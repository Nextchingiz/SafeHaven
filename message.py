# Libraries we will need for the message notification system
import smtplib
import ssl
from providers import PROVIDERS

# Send Message function
def send_message(number: str, message: str, provider: str, sender_credentials: tuple, subject: str = "SafeHaven Update", smtp_server: str = "smtp.gmail.com", smtp_port: int = 465):
    sender_email, email_password = sender_credentials

    # Get the providers info from the providers.py file
    provider_info = PROVIDERS.get(provider)
    if provider_info is None or "sms" not in provider_info:
        raise ValueError(f"Invalid provider or missing SMS gateway for provider: {provider}") # Check for any errors we may have
    
    # Set the email that will be converted into a phone number
    receiver_email = f"{number}@{provider_info['sms']}"
    email_message = f"Subject:{subject}\nTo:{receiver_email}\n\n{message}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context = context) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

# MESSAGE function that will set the text of the notification
def MESSAGE(time: str, alert_type: str, number: str):
    
    text = f" There was a {alert_type} at {time}" # Text
    provider = "AT&T" # Provider
    sender_credentials = ("thesafehaven0@gmail.com", "cmfb uxnk nwcn ngch") # Credentials

    send_message(number, text, provider, sender_credentials) # Use the function defined above to send the actual alert

    print(f'\nAlert sent to ({number[0:3]}) {number[3:6]}-{number[6:10]}: "{text[1:]}"\n')  # Display the phone number to which the message was sent