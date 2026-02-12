"""
Compatibility module - re-exports from reorganized structure.
For new code, import directly from database.py and models.py
"""
from database import engine, Base
from models import House, Pupil, Society, student_society, create_database

__all__ = ['engine', 'Base', 'House', 'Pupil', 'Society', 'student_society', 'create_database']


