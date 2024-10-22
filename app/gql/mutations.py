from graphene import ObjectType

from app.gql.employer.mutations import AddEmployer, UpdateEmployer, DeleteEmployer
from app.gql.job.mutations import AddJob, UpdateJob, DeleteJob
from app.gql.user.mutations import LoginUser, RegisterUser, ApplyForJob


class Mutations(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()

    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()

    login_user = LoginUser.Field()
    register_user = RegisterUser.Field()

    apply_for_job = ApplyForJob.Field()
