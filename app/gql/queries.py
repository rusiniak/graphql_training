from graphene import ObjectType, List, Int, Field

from app.db.database import Session
from app.db.models import Job, Employer, User, JobApplication
from app.gql.types import JobObject, EmployerObject, UserObject, JobApplicationObject


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))

    users = List(UserObject)

    job_applications = List(JobApplicationObject)

    @staticmethod
    def resolve_jobs(root, info):
        return Session().query(Job).all()

    @staticmethod
    def resolve_job(root, info, id):
        return Session().query(Job).get(id)

    @staticmethod
    def resolve_employers(root, info):
        return Session().query(Employer).all()

    @staticmethod
    def resolve_employer(root, info, id):
        return Session().query(Employer).get(id)

    @staticmethod
    def resolve_users(root, info):
        return Session().query(User).all()

    @staticmethod
    def resolve_job_applications(root, info):
        return Session().query(JobApplication).all()
