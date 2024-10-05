import plyer

from ai_explorer.app import console


class NotificationService:
    def notify(self, message: str) -> None:
        console.print(f"Notification: {message}")
        plyer.notification.notify(
            title="AI Local Explorer",
            message=message,
            app_icon=None,
            timeout=10,
        )


notification = NotificationService()
