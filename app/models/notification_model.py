class Notification:
    def __init__(self, notification_id, user_id, notification_image:None, message, timestamp):
        self.notification_id = notification_id
        self.user_id = user_id
        self.notification_image = notification_image
        self.message = message
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "notification_image": self.notification_image,
            "message": self.message,
            "timestamp": self.timestamp
        }
