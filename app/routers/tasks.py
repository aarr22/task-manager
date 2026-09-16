from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies import get_current_user
from app.dtos.requests import TaskCreateRequest, TaskUpdateRequest
from app.dtos.responses import TaskResponse
from app.enums import Priority, Role, Status
from app.models import Task, User

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_or_404(task_id: int, current_user: User, session: Session) -> Task:
    """Same 404 whether the task doesn't exist or just isn't yours — never leak which."""
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != Role.admin and task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = Task(**payload.model_dump(), user_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    task_status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    query = select(Task)
    if current_user.role != Role.admin:
        query = query.where(Task.user_id == current_user.id)
    if task_status is not None:
        query = query.where(Task.status == task_status)
    if priority is not None:
        query = query.where(Task.priority == priority)

    query = query.offset(skip).limit(limit)
    return session.exec(query).all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return get_task_or_404(task_id, current_user, session)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = get_task_or_404(task_id, current_user, session)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    summary="Mark a task as done",
    description="Sets status to done. Returns 400 if the task is already done.",
)
def complete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = get_task_or_404(task_id, current_user, session)
    if task.status == Status.done:
        raise HTTPException(status_code=400, detail="Task is already done")

    task.status = Status.done
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = get_task_or_404(task_id, current_user, session)
    session.delete(task)
    session.commit()
