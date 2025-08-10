# FastAPI ToDo List API
This is a simple and secure RESTful ToDo List API built using **FastAPI**, **PostgreSQL**, and **JWT authentication**. It allows users to register, log in, and manage their personal task list with CRUD operations, filtering, and pagination.

# Features
- User Registration & Login with JWT
- Create / Read / Update / Delete (CRUD) for tasks
- Filter tasks by status (`New`, `In Progress`, `Completed`)
- Only the task owner can update or delete their tasks
- Pagination support for task list
- PostgreSQL database with SQLAlchemy ORM
- Environment variables for secure configuration

                Project Structure
fastapi-todo/
├── app/
│ ├── security.py
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── database.py
│ ├── crud.py
│ ├── auth.py
│ ├── routers/
│ │ ├── user.py
│ │ └── task.py
├── tests/
│ └── test_tasks.py
│ └── conftest.py
├── .pytest_cache
├── alembic
├── create_tables.py
├── venv
├── .env
├── requirements.txt
└── README.md


Installation
1.Clone the repository
git clone https://github.com/Pustekhanim/fastapi-todo.git
cd fastapi-todo

2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
3. Install dependencie
pip install -r requirements.txt
4. Set up environment variables
DATABASE_URL="postgresql://todo_user:shpustexanim@localhost:5433/fastapi_todo"
SECRET_KEY="my_super_secret_key"
5. Initialize the database
Make sure PostgreSQL is running and the `todo_db` database exists. Then run:
python create_tables.py
6. Start the development server
uvicorn app.main:app --reload
Open your browser and visit:
📘 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Authentication
- `POST /signup` - Register new user
- `POST /token` - Login (returns JWT)

### Tasks (Require Auth)
- `GET /tasks` - List all user's tasks
- `POST /tasks` - Create new task
- `PUT /tasks/{id}/complete` - Mark task complete

## Test Credentials
Username: `testuser`  
Password: `testpass123`

Running Tests
pytest
Ensure PostgreSQL and the `.env` are properly set before running tests.

Technologies Used
* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [JWT (via python-jose)](https://python-jose.readthedocs.io/)
* [Pydantic](https://docs.pydantic.dev/)
* [Pytest](https://docs.pytest.org/)
