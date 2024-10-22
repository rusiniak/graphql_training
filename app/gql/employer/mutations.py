from graphene import String, Mutation, Field, Int, Boolean

from app.db.database import Session
from app.db.models import Employer
from app.gql.types import EmployerObject, is_admin
from app.utils.jwt import get_authenticated_user


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerObject)

    @is_admin
    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        session = Session()
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session.add(employer)
        session.commit()
        session.refresh(employer)
        return AddEmployer(employer=employer)


class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)
    @is_admin
    @staticmethod
    def mutate(root, info, id, name=None, contact_email=None, industry=None):
        session = Session()
        employer = session.query(Employer).get(id)
        if not employer:
            raise ValueError("Employer not found")

        if name is not None:
            employer.name = name
        if contact_email is not None:
            employer.contact_email = contact_email
        if industry is not None:
            employer.industry = industry

        session.commit()
        session.refresh(employer)
        session.close()
        return UpdateEmployer(employer=employer)


class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    result = Boolean()
    @is_admin
    @staticmethod
    def mutate(root, info, id):
        session = Session()
        employer = session.query(Employer).get(id)
        if not employer:
            raise ValueError(f"Employer with {id} not found")
        session.delete(employer)
        session.commit()
        session.close()
        return DeleteEmployer(result=True)
