from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TaskStatus(str, enum.Enum):
    new = "New"
    in_progress = "In Progress"
    completed = "Completed"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="owner", cascade="all, delete")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.new)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="tasks")
