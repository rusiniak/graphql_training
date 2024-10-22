from graphene import String, Int, Mutation, Field

from app.db.database import Session
from app.db.models import Job
from app.gql.types import JobObject, is_admin


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)
    @is_admin
    @staticmethod
    def mutate(root, info, title, description, employer_id):
        session =Session()
        job = Job(title=title, description=description, employer_id=employer_id)
        session.add(job)
        session.commit()
        session.refresh(job)
        return AddJob(job=job)

class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)
    @is_admin
    @staticmethod
    def mutate(root, info, job_id, title=None, description=None, employer_id=None):
        session =Session()
        job = session.query(Job).get(job_id)
        if not job:
            raise ValueError("Job not found")

        if title is not None:
            job.title = title
        if description is not None:
            job.description = description
        if employer_id is not None:
            job.employer_id = employer_id

        session.commit()
        session.refresh(job)
        session.close()
        return UpdateJob(job=job)

class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    job = Field(lambda: JobObject)
    @is_admin
    @staticmethod
    def mutate(root, info, id):
        session =Session()
        job = session.query(Job).get(id)
        if not job:
            raise ValueError(f"Job with {id} not found")
        session.delete(job)
        session.commit()
        session.close()
        return DeleteJob(job=job)