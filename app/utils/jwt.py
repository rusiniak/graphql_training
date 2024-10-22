from datetime import datetime, UTC, timedelta

import jwt
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User
from app.settings.config import TOKEN_EXPIRATION_TIME_MINUTES, SECRET_KEY, ALGORITHM


def generate_token(email):
    expiration_time = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_authenticated_user(context):
    request_object = context.get('request')
    auth_header = request_object.headers.get("Authorization")
    if not auth_header:
        raise GraphQLError("Missing authentication header")
    token = auth_header.split()[-1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.now(UTC) > datetime.fromtimestamp(payload['exp'], tz=UTC):
            raise GraphQLError(
                f"Token expired {datetime.fromtimestamp(payload['exp'], tz=UTC)}, now: {datetime.now(UTC)}")
        session = Session()
        user = session.query(User).filter(User.email == payload.get('sub')).first()
        if not user:
            raise GraphQLError("Could not authenticate user")
        return user
    except jwt.exceptions.ImmatureSignatureError:
        raise GraphQLError("Invalid authentication token")

