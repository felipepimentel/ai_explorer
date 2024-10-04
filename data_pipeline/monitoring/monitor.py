import time
import psutil
import smtplib
from email.mime.text import MIMEText

class SystemMonitor:
    def __init__(self, email_config):
        self.email_config = email_config

    def check_system_resources(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        if cpu_usage > 90 or memory_usage > 90 or disk_usage > 90:
            self.send_alert(f"High resource usage: CPU {cpu_usage}%, Memory {memory_usage}%, Disk {disk_usage}%")

    def send_alert(self, message):
        msg = MIMEText(message)
        msg['Subject'] = "System Alert"
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']

        with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            server.send_message(msg)

    def start_monitoring(self, interval=60):
        while True:
            self.check_system_resources()
            time.sleep(interval)

# Exemplo de uso:
# email_config = {
#     'from': 'alerts@example.com',
#     'to': 'admin@example.com',
#     'smtp_server': 'smtp.example.com',
#     'smtp_port': 587,
#     'username': 'alerts@example.com',
#     'password': 'password'
# }
# monitor = SystemMonitor(email_config)
# monitor.start_monitoring()