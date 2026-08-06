from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.models import User
from config.database import db


class AuthService:

    @staticmethod
    def register_user(
        username,
        email,
        password
    ):
        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            return False, "User already exists."

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return True, "Registration successful."

    @staticmethod
    def authenticate_user(
        email,
        password
    ):
        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            return None

        if not check_password_hash(
            user.password_hash,
            password
        ):
            return None

        return user