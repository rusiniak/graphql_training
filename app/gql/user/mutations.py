from graphene import Mutation, String, Field, Int
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User, JobApplication
from app.gql.types import UserObject, is_admin, JobApplicationObject
from app.utils.jwt import generate_token
from app.utils.pasword_hasher import verify_password, hash_password


class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError("Invalid email")
        verify_password(user.password_hash, password)

        token = generate_token(email)

        return LoginUser(token=token)


class RegisterUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)

    @is_admin
    @staticmethod
    def mutate(root, info, username, email, password, role):
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        if user:
            raise GraphQLError(f"User with email {email} is already registered!")
        user = User(username=username, email=email, password_hash=hash_password(password), role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return RegisterUser(user=user)


class ApplyForJob(Mutation):
    class Arguments:
        user_id = Int(required=True)
        job_id = Int(required=True)

    job_application = Field(lambda: JobApplicationObject)

    @staticmethod
    def mutate(root, info, user_id, job_id):
        session = Session()
        job_application = session.query(JobApplication).filter(JobApplication.user_id == user_id,
                                                               JobApplication.job_id == job_id).first()
        if job_application:
            raise GraphQLError("User already applied for this job!")

        job_application = JobApplication(user_id=user_id, job_id=job_id)
        session.add(job_application)
        session.commit()
        session.refresh(job_application)
        session.close()
        return ApplyForJob(job_application=job_application)
