from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from pydantic import BaseModel
from app import crud, models, schemas, database, auth
from app.database import get_db
from app.auth import get_current_user
from app.routers import user, task
from app.schemas import TaskStatus 

app = FastAPI(title="ToDo List API")

models.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
app.include_router(task.router)

@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/tasks", response_model=List[schemas.TaskOut])
def read_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[schemas.TaskStatus] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_tasks_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = crud.get_task(db, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_task(db=db, task=task, user_id=current_user.id)

@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = crud.get_task(db, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return crud.update_task(db=db, task_id=task_id, task_update=task_update)

@app.put("/tasks/{task_id}/complete", response_model=schemas.TaskOut)
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

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = crud.get_task(db, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    crud.delete_task(db=db, task_id=task_id)
    return {"detail": "Task deleted"}

@app.get("/")
def root():
    return {"message": "Welcome to the ToDo API"}
