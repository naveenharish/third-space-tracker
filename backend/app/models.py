'''
- Models define WHAT your data looks like and HOW it is stored in the database.
  SQLAlchemy is an Object Relational Mapper (ORM) that allows you to define your data models 
  as Python classes, which are then mapped to database tables.
- Will use alembic for database migrations
'''
from sqlalchemy import Column, Integer, String, JSON, Float
from sqlalchemy.orm import DeclarativeBase

#Base class for all models to inherit from 
class Base(DeclarativeBase):
    pass

#Each model class represents a table in the database, and each attribute of the class represents a column in that table.
class Place(Base):
    __tablename__ = "places"
    #columns have a name and a data type
    place_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    place_type = Column(String)
    lat = Column(Float, index=True)
    lng = Column(Float, index=True)
    source_ids = Column(JSON)  # Store source IDs as a JSON array
    amenities = Column(JSON)  # Store amenities as a JSON array
    hours = Column(JSON)  # Store hours as a JSON object