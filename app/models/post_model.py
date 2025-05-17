class Post:
    def __init__(self, post_id, user_id, job_text,content, image_url=None, profile_image_url=None, 
            timestamp=None, likes=0, comments=None):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.image_url = image_url
        self.profile_image_url = profile_image_url
        self.job_text = job_text
        self.timestamp = timestamp
        self.likes = likes
        self.comments = comments if comments is not None else []

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "content": self.content,
            "image_url": self.image_url,
            "profile_image_url": self.profile_image_url,
            "job_text": self.job_text,
            "timestamp": self.timestamp,
            "likes": self.likes,
            "comments": self.comments  # Bu liste, yorumların string veya dict olarak saklanmasına izin verir
        }
