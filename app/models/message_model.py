class Message:
    def __init__(self, message_id, sender_id, sender_name, sender_image, receiver_id, receiver_name, receiver_image, content, image_url, timestamp):
        self.message_id = message_id
        self.sender_id = sender_id
        self.sender_name = sender_name                
        self.sender_image = sender_image  
        self.receiver_id = receiver_id
        self.receiver_name = receiver_name          
        self.receiver_image = receiver_image  
        self.content = content
        self.image_url = image_url 
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,         
            "sender_image": self.sender_image,  
            "receiver_id": self.receiver_id,
            "receiver_name": self.receiver_name,    
            "receiver_image": self.receiver_image,  
            "content": self.content,
            "image_url": self.image_url,
            "timestamp": self.timestamp
        }
