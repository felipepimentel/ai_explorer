import smtplib
from email.mime.text import MIMEText
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class NotificationManager:
    def __init__(self, email_config=None, slack_token=None):
        self.email_config = email_config
        self.slack_client = WebClient(token=slack_token) if slack_token else None

    def send_email(self, subject, message, to_email):
        if not self.email_config:
            raise ValueError("Email configuration not provided")

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.email_config['from']
        msg['To'] = to_email

        with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            server.send_message(msg)

    def send_slack_message(self, channel, message):
        if not self.slack_client:
            raise ValueError("Slack client not initialized")

        try:
            response = self.slack_client.chat_postMessage(channel=channel, text=message)
            assert response["message"]["text"] == message
        except SlackApiError as e:
            print(f"Error sending message: {e}")

    def notify(self, message, notification_type='all', **kwargs):
        if notification_type in ['all', 'email']:
            self.send_email(kwargs.get('subject', 'Notification'), message, kwargs.get('to_email'))
        if notification_type in ['all', 'slack']:
            self.send_slack_message(kwargs.get('channel', '#general'), message)

# Uso:
# email_config = {
#     'smtp_server': 'smtp.gmail.com',
#     'smtp_port': 587,
#     'username': 'your_email@gmail.com',
#     'password': 'your_password',
#     'from': 'your_email@gmail.com'
# }
# slack_token = 'your-slack-token'
# notifier = NotificationManager(email_config, slack_token)
# notifier.notify("Pipeline completed successfully!", to_email="admin@example.com", channel="#data-pipeline")