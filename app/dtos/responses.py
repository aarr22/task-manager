from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.enums import Priority, Role, Status


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: Role
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    priority: Priority
    status: Status
    due_date: Optional[date]
    created_at: datetime
    user_id: int
