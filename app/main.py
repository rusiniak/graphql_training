from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from app.db.database import prepare_database, Session
from app.db.models import Employer, Job
from app.gql.mutations import Mutations
from app.gql.queries import Query

schema = Schema(query=Query, mutation=Mutations)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    prepare_database()


@app.get("/employers")
def get_employers():
    with Session() as session:
        return session.query(Employer).all()

@app.get("/jobs")
def get_jobs():
    with Session() as session:
        return session.query(Job).all()

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
