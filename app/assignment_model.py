from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    ics_uid = Column(String(255), nullable=True, index=True)
    course_id = Column(String(4), nullable=True, default="SYNC")
    name = Column(String, index=True)
    course = Column(String)
    due_date = Column(String)
    due_time = Column(String)
    assignment_type = Column(String)
    priority_level = Column(Integer)
    points = Column(Float)