# run (pip install twilio) on the pi before use
from twilio.rest import Client

account_sid = "ACa1d332ce1f26570254f47e022e84ed71"
auth_token = "611ea992eb417ea8615e57cc3eb856d2"

client = Client(account_sid, auth_token)

message = client.api.account.messages.create(
    to = +3186131760,
    from_ = +18884882467,
    body = "Hello the code is working"
)