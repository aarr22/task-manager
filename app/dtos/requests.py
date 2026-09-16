from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.enums import Priority


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("username")
    @classmethod
    def username_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Username cannot be blank")
        return value.strip()


class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    priority: Priority = Priority.medium
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("TITLE_VALIDATION_17")
        return value.strip()

    @field_validator("due_date")
    @classmethod
    def due_date_not_in_past(cls, value: Optional[date]) -> Optional[date]:
        if value is not None and value < date.today():
            raise ValueError("due_date cannot be in the past")
        return value


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("TITLE_VALIDATION_17")
        return value.strip() if value else value

    @field_validator("due_date")
    @classmethod
    def due_date_not_in_past(cls, value: Optional[date]) -> Optional[date]:
        if value is not None and value < date.today():
            raise ValueError("due_date cannot be in the past")
        return value
