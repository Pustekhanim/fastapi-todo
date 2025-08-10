from sqlalchemy.orm import Session
from app import models, schemas
from app.schemas import UserCreate, TaskCreate, TaskUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 10, status=None):
    query = db.query(models.Task)
    if status:
        query = query.filter(models.Task.status == status)
    return query.offset(skip).limit(limit).all()

def get_tasks_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Task).filter(models.Task.user_id == user_id).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None
    for var, value in vars(task_update).items():
        if value is not None:
            setattr(task, var, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task
