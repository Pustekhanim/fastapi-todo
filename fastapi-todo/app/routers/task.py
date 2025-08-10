from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[schemas.TaskOut])
def read_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[schemas.TaskStatus] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_tasks_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = crud.get_task(db, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_task(db=db, task=task, user_id=current_user.id)

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = crud.get_task(db, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return crud.update_task(db=db, task_id=task_id, task_update=task_update)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = crud.get_task(db, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    crud.delete_task(db=db, task_id=task_id)
    return {"detail": "Task deleted"}

@router.put("/tasks/{task_id}/complete", response_model=schemas.TaskOut)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = crud.get_task(db, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")

    return crud.update_task(
        db=db,
        task_id=task_id,
        task_update=schemas.TaskUpdate(status=schemas.TaskStatus.completed)
    )
