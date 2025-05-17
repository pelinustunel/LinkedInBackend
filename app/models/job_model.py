class Job:
    def __init__(self, job_id, title, company, company_logo, location, skill, description, posted_date):
        self.job_id = job_id
        self.title = title
        self.company = company
        self.company_logo = company_logo  
        self.location = location
        self.skill = skill
        self.description = description
        self.posted_date = posted_date

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "company_logo": self.company_logo,  
            "location": self.location,
            "skill": self.skill,
            "description": self.description,
            "posted_date": self.posted_date
        }
