class NotificationManager:
    def notify(self, message: str):
        # Implement the logic to send notifications
        print(f"Notification: {message}")

    def send_notification(self, message, title="Best Buy Stock Alert"):
        """Send desktop and sound notifications."""
        # Desktop notification
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Best Buy Monitor",
                timeout=10,
            )
        except Exception as e:
            print(f"Desktop notification failed: {e}")

        # Sound alert
        try:
            for _ in range(3):
                winsound.Beep(1000, 500)
                time_module.sleep(0.5)
        except Exception as e:
            print(f"Sound alert failed: {e}")
        
        # Console output
        print("\n" + "!" * 50)
        print(f"\033[91m{title}: {message}\033[0m")
        print("!" * 50 + "\n")