import smtplib
from email.mime.text import MIMEText
from data_pipeline.utils.logger import setup_logger

logger = setup_logger(__name__, 'logs/alerts.log')

class AlertSystem:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_alert(self, subject, message, recipient_email):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = recipient_email

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            logger.info(f"Alert sent to {recipient_email}")
        except Exception as e:
            logger.error(f"Failed to send alert: {str(e)}")

# Uso:
# alert_system = AlertSystem('smtp.gmail.com', 587, 'sender@example.com', 'password')
# alert_system.send_alert('High CPU Usage', 'CPU usage is above 90%', 'recipient@example.com')