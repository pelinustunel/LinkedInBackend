from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from models.job_model import Job
from models.job_storage import jobs  
from controllers.auth_middleware import token_required

# Blueprint tanımı
job_bp = Blueprint("job", __name__, url_prefix="/job")
job_api = Api(job_bp)

# Swagger UI için Job Modeli
job_model = job_api.model("Job", {
    "job_id": fields.Integer(description="İş İlanı ID"),
    "title": fields.String(description="Pozisyon"),
    "company": fields.String(description="Şirket"),
    "company_logo": fields.String(description="Şirket Logosu"),
    "location": fields.String(description="Lokasyon"),
    "skill": fields.String(description="Yetenekler"),  
    "description": fields.String(description="Açıklama"),
    "posted_date": fields.String(description="Yayın Tarihi")
})
 

SECRET_KEY = "your_secret_key"

#  Tüm iş ilanlarını getirme (POST job/list)
@job_api.route("/list")
class JobListResource(Resource):
    @job_api.marshal_list_with(job_model)
    @token_required
    def post(self):
        """Tüm iş ilanlarını getir"""
        return jobs

#  Yeni bir iş ilanı ekleme (POST job/add_job)
@job_api.route("/add_job")
class AddJobResource(Resource):
    @job_api.expect(job_model)
    @job_api.marshal_with(job_model, code=201)
    @token_required
    def post(self):
        """Yeni bir iş ilanı ekle"""
        data = request.get_json()
        new_id = max([job.job_id for job in jobs], default=0) + 1
        new_job = Job(
            new_id,
            data["title"],
            data["company"],
            data["company_logo"],
            data["location"],
            data["description"],
            "2025-02-22"  # Tarih sabit, istersen datetime.now().strftime("%Y-%m-%d") ile dinamik yapabilirsin
        )
        jobs.append(new_job)
        return new_job, 201

#  İş ilanı güncelleme (PUT job/update_job)
@job_api.route("/update_job/<int:job_id>")
class UpdateJobResource(Resource):
    @job_api.expect(job_model)
    @job_api.marshal_with(job_model)
    @token_required
    def put(self, job_id):
        """Mevcut bir iş ilanını güncelle"""
        job = next((job for job in jobs if job.job_id == job_id), None)
        if not job:
            job_api.abort(404, "Job not found")

        data = request.get_json()
        job.title = data.get("title", job.title)
        job.company = data.get("company", job.company)
        job.company_logo = data.get("company_logo", job.company_logo)
        job.location = data.get("location", job.location)
        job.description = data.get("description", job.description)

        return job, 200

#  İş ilanı silme (DELETE job/{job_id})
@job_api.route("/delete_job/<int:job_id>")
class DeleteJobResource(Resource):
    @token_required
    def delete(self, job_id):
        """Belirtilen iş ilanını sil"""
        global jobs
        job = next((job for job in jobs if job.job_id == job_id), None)
        if not job:
            job_api.abort(404, "Job not found")

        jobs = [j for j in jobs if j.job_id != job_id]
        return {"message": "Job deleted"}, 200

#  Belirli bir iş ilanını getirme (POST job/{job_id})
@job_api.route("/<int:job_id>")
class JobResource(Resource):
    @job_api.marshal_with(job_model)
    @token_required
    def post(self, job_id):
        """Belirli bir iş ilanını getir"""
        job = next((job for job in jobs if job.job_id == job_id), None)
        if not job:
            job_api.abort(404, "Job not found")
        return job
