from twilio.rest import Client
 
ACCOUNT_SID = 'ACd8e37c6f6e9d5c51ec9886925a615a5b'
AUTH_TOKEN  = 'c07d0072065f37a58770a75724975c2a'
SERVICE_SID = 'MG1c00b90a200a3a9107150903c879527c'
TO_NUMBER   = '+4552777860'
 
def send_alarm_sms(body='Alarm! der er ildebrand'):
    """Send an SMS alert via Twilio. Returns the message SID on success."""
    try:
        client  = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            messaging_service_sid=SERVICE_SID,
            body=body,
            to=TO_NUMBER
        )
        print(f"SMS sent: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"SMS error: {e}")
        return None