"""run this to create the first admin user in the database

there is no API route that creates an admin ,this is intentional,
so nobody can self-register their way into that role.

how to use:
    python create_admin.py
"""
import getpass

from sqlmodel import Session, select

from app.database import engine, init_db
from app.enums import Role
from app.models import User
from app.security import hash_password


def main():
    init_db()

    username = input("Admin username: ").strip()
    email = input("Admin email: ").strip()
    password = getpass.getpass("Admin password: ")

    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            print("A user with that username already exists.")
            return

        admin = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role=Role.admin,
        )
        session.add(admin)
        session.commit()
        print(f"Admin '{username}' created.")


if __name__ == "__main__":
    main()
