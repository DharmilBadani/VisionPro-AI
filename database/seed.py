"""
Database Seeder
Creates default admin user.
"""

from werkzeug.security import generate_password_hash

from app import app
from config.database import db
from database.models import User


def seed_database():
    """
    Insert initial records.
    """

    with app.app_context():

        existing_admin = User.query.filter_by(
            email="admin@visionai.com"
        ).first()

        if existing_admin:
            print("Admin user already exists.")
            return

        admin = User(
            username="admin",
            email="admin@visionai.com",
            password_hash=generate_password_hash(
                "Admin@123"
            ),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully.")


if __name__ == "__main__":
    seed_database()