"""
Database base configuration
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic
from app.models.user import User
from app.models.suspect import Suspect
from app.models.case import Case
from app.models.sketch import Sketch
from app.models.face_encoding import FaceEncoding
