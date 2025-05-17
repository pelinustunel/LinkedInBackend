class User:
    def __init__(self, user_id, name, profile_picture, title, location, education, connection):
        self.user_id = user_id
        self.name = name
        self.profile_picture = profile_picture
        self.title = title
        self.location = location
        self.education = education
        self.connection = connection

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "profile_picture": self.profile_picture,
            "title": self.title,
            "location": self.location,
            "education": self.education,
            "connection": self.connection
        }