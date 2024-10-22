from functools import wraps

from graphene import ObjectType, Int, String, List, Field
from graphql import GraphQLError

from app.utils.jwt import get_authenticated_user

def is_admin(callable):
    @wraps(callable)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        if user.role != "admin":
            raise GraphQLError(f"Current user is not an admin but {user['role']}")
        return callable(*args, **kwargs)
    return wrapper

def is_authenticated(callable):
    @wraps(callable)
    def wrapper(*args, **kwargs):
        info = args[1]
        get_authenticated_user(info.context)
        return callable(*args, **kwargs)
    return wrapper


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return root.jobs


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)
    job_applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_employer(root, info):
        return root.employer

    @staticmethod
    def resolve_job_applications(root, info):
        return root.job_applications

class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()
    job_applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_job_applications(root, info):
        return root.job_applications

class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field(lambda: UserObject)
    job = Field(lambda: JobObject)

    @staticmethod
    def resolve_job(root, info):
        return root.job

    @staticmethod
    def resolve_user(root, info):
        return root.user
