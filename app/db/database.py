from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.data import employers_data, jobs_data, user_data, jobapplication_data
from app.db.models import Base, Job, Employer, User, JobApplication
from app.settings.config import DB_URL
from app.utils.pasword_hasher import hash_password

engine = create_engine(DB_URL)
connection = engine.connect()

Session = sessionmaker(bind=engine)


def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
        session.add(Employer(**employer))

    for job in jobs_data:
        session.add(Job(**job))

    for user in user_data:
        user['password_hash'] = hash_password(user.pop('password'))
        session.add(User(**user))

    for job_application in jobapplication_data:
        session.add(JobApplication(**job_application))

    session.commit()
    session.close()
