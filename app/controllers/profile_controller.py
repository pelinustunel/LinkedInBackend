from flask import Blueprint,request, jsonify
from flask_restx import Api, Resource, fields
from models.user_model import User
from controllers.auth_middleware import token_required

# Blueprint tanımı
profile_bp = Blueprint("profile", __name__, url_prefix="/profile")
profile_api = Api(profile_bp)

users = [
    User(1, "Pelin Üstünel", "http://127.0.0.1:5003/images/pelin.jpg", "iOS Developer", "Ankara", "Kırklareli Üniversitesi", "179 connections")
]

activities = [
    {"title": "Swift Workshop Speaker", "description": "Geliştirici topluluğunda Swift ile mobil uygulama geliştirme üzerine bir atölye verdim."},
    {"title": "Papara Women in Tech Bootcamp Graduate", "description": "Papara & Patika.dev iş birliği ile düzenlenen Women in Software Bootcamp'inde konuşmacı olmaktan mutluluk duydum."},
    {"title": "LinkedIn Clone Project", "description": "iOS ile LinkedIn benzeri bir sosyal ağ uygulaması geliştirdim, backend tarafında Flask kullanıldı."}
]

experiences = [
    {
        "id": 0,
        "company_logo": "http://127.0.0.1:5003/images/garanti.jpg",
        "company_name": "Provision",
        "position": "iOS Developer Intern",
        "experience_year": "7 July 2024 - 9 September 2024 ",
        "work_mode": "Hybrid"
    }
]

educations = [
    {
        "id": 0,  # ✅ BU ŞART
        "school": "Kırklareli Üniversitesi",
        "degree": "Bachelor's Degree",
        "education_image": "http://127.0.0.1:5003/images/kirklareli.jpg",
        "field_of_study": "Software Engineering",
        "education_year": "2021 - 2025",
    }
]

skills = [
    {
        "id": 0,
        "name": "Swift"
    },
    {
        "id": 1,
        "name": "UIKit"
    },
    {
        "id": 2,
        "name": "RxSwift"
    }
]

analytics = [
    {
        "profile_views": 254,
        "post_impressions": 1020,
        "search_appearances": 87
    }
]


SECRET_KEY = "your_secret_key"

analytic_model = profile_api.model("Analytic", {
    "profile_views": fields.Integer(required=True, description="Profil görüntülenme sayısı"),
    "post_impressions": fields.Integer(required=True, description="Post görüntülenme sayısı"),
    "search_appearances": fields.Integer(required=True, description="Arama görünürlük sayısı")
})

activity_model = profile_api.model("Activity", {
    "title": fields.String(required=True, description="Aktivite başlığı"),
    "description": fields.String(required=True, description="Aktivite açıklaması")
})

experience_model = profile_api.model("Experience", {
    "id": fields.Integer(readonly=True, description="Experience ID"),  
    "company_logo": fields.String(description="Şirket logosu URL"),
    "company_name": fields.String(required=True, description="Şirket adı"),
    "position": fields.String(required=True, description="Pozisyon"),
    "experience_year": fields.String(required=True, description="tarih"),
    "work_mode": fields.String(description="Çalışma şekli (örneğin: Remote, Hybrid, On-Site)")
})


education_model = profile_api.model("Education", {
    "id": fields.Integer(readonly=True, description="Education ID"), 
    "school": fields.String(required=True, description="Okul adı"),
    "degree": fields.String(required=True, description="Derece"),
    "education_image": fields.String(required = True, description="Eğitim Fotoğrafı"),
    "field_of_study": fields.String(description="Çalışma alanı"),
    "education_year": fields.String(required=True, description="tarih")
})

skills_model = profile_api.model("Skill", {
    "id": fields.Integer(readonly=True, description="Skill ID"), 
    "name": fields.String(required=True, description="Yetenek adı")
})


@profile_api.route("/list")
class ProfileList(Resource):
    @profile_api.doc(responses={200: "Kullanıcı bilgileri ve tüm profil verileri başarıyla getirildi"})
    @token_required
    def post(self):
        """Kullanıcı bilgilerini ve tüm profil verilerini getir (activity, education, skill, experience, analytic)"""
        # Kullanıcı bilgilerini al (örneğin, ilk kullanıcıyı alıyoruz)
        user = users[0] if users else None
        if not user:
            return {"error": "Kullanıcı bulunamadı"}, 404

        # Kullanıcı bilgilerini ve diğer verileri birleştir
        profile_data = {
            "user": user.to_dict(),  # Kullanıcı bilgileri
            "activities": activities,
            "educations": educations,
            "skills": skills,
            "experiences": experiences,
            "analytics": analytics
        }
        return profile_data, 200


@profile_api.route("/user")
class UserOnlyProfile(Resource):
    @token_required
    def post(self):
        user = users[0] if users else None
        if not user:
            return {"error": "Kullanıcı bulunamadı"}, 404

        return user.to_dict(), 200  # 👈 Sadece user bilgisini dönüyoruz


### Analitik (Analytic) Endpoint'leri ###
@profile_api.route("/analytic/list")
class AnalyticList(Resource):
    @profile_api.marshal_list_with(analytic_model)  # User.analytic_model yerine direkt analytic_model kullan
    @token_required 
    def post(self):
        """Tüm analitikleri getir"""
        return analytics


### Aktivite (Activity) Endpoint'leri ###
@profile_api.route("/activity/list")
class ActivityList(Resource):
    @profile_api.marshal_list_with(activity_model)
    @token_required 
    def post(self):
        """Tüm aktiviteleri getir"""
        return activities
    


### Deneyim (Experience) Endpoint'leri ###
@profile_api.route("/experience/list")
class ExperienceList(Resource):
    @profile_api.marshal_list_with(experience_model)
    @token_required 
    def post(self):
        """Tüm deneyimleri getir"""
        return experiences
   
@profile_api.route("/experience/add_experience")
class AddExperience(Resource):
    @profile_api.expect(experience_model)
    @token_required 
    def post(self):
        """Yeni experience ekle"""
        data = request.get_json()
        experience_id = max([e["id"] for e in experiences], default=-1) + 1
        experience = {"id": experience_id, **data}
        experiences.append(experience)
        return {"message": "Experience eklendi", "experience": experience}, 201

@profile_api.route("/experience/update_experience/<int:experience_id>")
class UpdateExperience(Resource):
    @profile_api.expect(experience_model)
    @token_required 
    def put(self, experience_id):
        """Experience güncelle"""
        experience = next((a for a in experiences if a["id"] == experience_id), None)
        if not experience:
            return {"error": "Experience bulunamadı"}, 404
        data = request.get_json()
        experience.update(data)
        return {"message": "Experience güncellendi", "experience": experience}, 200

@profile_api.route("/experience/delete_experience/<int:experience_id>")
class DeleteExperience(Resource):
    @token_required 
    def delete(self, experience_id):
        """Experience sil"""
        global experiences
        experiences = [a for a in experiences if a["id"] != experience_id]
        return {"message": "Experience silindi"}, 200

@profile_api.route("/experience/<int:experience_id>")
class GetExperience(Resource):
    @profile_api.marshal_with(experience_model)
    @token_required 
    def post(self, experience_id):
        """Belirli bir experience getir"""
        experience = next((a for a in experiences if a["id"] == experience_id), None)
        if not experience:
            profile_api.abort(404, "Experience bulunamadı")
        return experience


### Eğitim (Education) Endpoint'leri ###
@profile_api.route("/education/list")
class EducationList(Resource):
    @profile_api.marshal_list_with(education_model)
    @token_required 
    def post(self):
        """Tüm deneyimleri getir"""
        return educations
    
@profile_api.route("/education/add_education")
class AddEducation(Resource):
    @profile_api.expect(education_model)
    @token_required 
    def post(self):
        """Yeni eğitim ekle"""
        data = request.get_json()
        education_id = max([e["id"] for e in educations], default=-1) + 1
        education = {"id": education_id, **data}  # ✅ id'yi ekliyoruz
        educations.append(education)
        return {"message": "Education eklendi", "education": education}, 201

@profile_api.route("/education/update_education/<int:education_id>")
class UpdateEducation(Resource):
    @profile_api.expect(education_model)
    @token_required 
    def put(self, education_id):
        """Aktivite güncelle"""
        education = next((a for a in educations if a["id"] == education_id), None)
        if not education:
            return {"error": "Education bulunamadı"}, 404
        data = request.get_json()
        education.update(data)
        return {"message": "Education güncellendi", "education": education}, 200

@profile_api.route("/education/delete_education/<int:education_id>")
class DeleteEducation(Resource):
    @token_required 
    def delete(self, education_id):
        """Aktiviteyi sil"""
        global educations
        educations = [a for a in educations if a["id"] != education_id]
        return {"message": "Education silindi"}, 200

@profile_api.route("/education/<int:education_id>")
class GetEducation(Resource):
    @profile_api.marshal_with(education_model)
    @token_required 
    def post(self, education_id):
        """Belirli bir education getir"""
        education = next((a for a in educations if a["id"] == education_id), None)
        if not education:
            profile_api.abort(404, "Education bulunamadı")
        return education


### Yetenek (Skills) Endpoint'leri ###
@profile_api.route("/skill/list")
class SkillList(Resource):
    @profile_api.marshal_list_with(skills_model)
    @token_required 
    def post(self):
        """Tüm skill getir"""
        return skills
    

@profile_api.route("/skill/add_skill")
class AddSkill(Resource):
    @profile_api.expect(skills_model)
    @token_required 
    def post(self):
        """Yeni skill ekle"""
        data = request.get_json()
        skill_id = max([e["id"] for e in skills], default=-1) + 1
        skill = {"id": skill_id, **data}
        skills.append(skill)
        return {"message": "Skill eklendi", "skill": skill}, 201
    
@profile_api.route("/skill/update_skill/<int:skill_id>")
class UpdateSkill(Resource):
    @profile_api.expect(skills_model)
    @token_required 
    def put(self, skill_id):
        """Skill güncelle"""
        skill = next((a for a in skills if a["id"] == skill_id), None)
        if not skill:
            return {"error": "Skill bulunamadı"}, 404
        data = request.get_json()
        skill.update(data)
        return {"message": "Skill güncellendi", "skill": skill}, 200
    

@profile_api.route("/skill/delete_skill/<int:skill_id>")
class DeleteSkill(Resource):
    @token_required 
    def delete(self, skill_id):
        """Aktiviteyi sil"""
        global skills
        skills = [a for a in skills if a["id"] != skill_id]
        return {"message": "Skill silindi"}, 200
    
@profile_api.route("/skill/<int:skill_id>")
class GetSkill(Resource):
    @profile_api.marshal_with(skills_model)
    @token_required 
    def post(self, skill_id):
        """Belirli bir skill getir"""
        skill = next((a for a in skills if a["id"] == skill_id), None)
        if not skill:
            profile_api.abort(404, "Skill bulunamadı")
        return skill




    
    




