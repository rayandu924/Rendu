import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
# from twilio.rest import Client  # Commenter cette ligne si Twilio n'est pas utilisé

class AlertService:
    def __init__(self):
        # Initialiser le client Twilio
        # self.twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        pass  # Ajouter du code conditionnel si nécessaire

    def send_email_alert(self, to_email, subject, message):
        #msg = MIMEMultipart()
        #msg['From'] = Config.SMTP_USERNAME
        #msg['To'] = to_email
        #msg['Subject'] = subject

        #msg.attach(MIMEText(message, 'plain'))
        #
        #try:
        #    server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        #    server.starttls()
        #    server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        #    text = msg.as_string()
        #    server.sendmail(Config.SMTP_USERNAME, to_email, text)
        #    server.quit()
        #    print(f"Email envoyé à {to_email}")
        #except Exception as e:
        #    print(f"Erreur lors de l'envoi de l'email: {e}")
        print(f"Email envoyé à {to_email}")

    def send_sms_alert(self, to_number, message):
        try:
            # message = self.twilio_client.messages.create(
            #     body=message,
            #     from_=Config.TWILIO_PHONE_NUMBER,
            #     to=to_number
            # )
            print(f"SMS envoyé à {to_number}: {message}")  # Simuler l'envoi
        except Exception as e:
            print(f"Erreur lors de l'envoi du SMS: {e}")
