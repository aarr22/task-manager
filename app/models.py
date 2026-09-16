from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.enums import Priority, Role, Status


class User(SQLModel, table=True):
    __table_args__ = {"sqlite_autoincrement": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: Role = Field(default=Role.user)
    is_active: bool = Field(default=True)


class Task(SQLModel, table=True):
    __table_args__ = {"sqlite_autoincrement": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    priority: Priority = Field(default=Priority.medium)
    status: Status = Field(default=Status.todo)
    due_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
