from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models import Base
import os
'''
Setting up postgresql database connection using SQLAlchemy. 
The engine is created using the DATABASE_URL from environment variables, 
and a session factory is defined for managing database sessions.

In command line, you can run the following command to create the database tables based on the defined models:
    - brew services start postgresql@16
    - createdb third_space_db    

python3 -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
- creating all tables in the database based on the defined models in app/models.py
- create_all only creates tables that don't exist yet. If you add a column to an existing model, create_all won't touch the already-existing table. 
  You'd have to manually alter it or drop and recreate it, losing your data.

Alembic fixes this problem by allowing you to create migrations that can be applied to the database to update its schema without losing data.
'''

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL")) #creating engine for database connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #creating a session factory for database sessions

