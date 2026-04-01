from pydantic import BaseModel, StringConstraints
from typing import Annotated

CourseID = Annotated[
    str,
    StringConstraints(pattern=r'^\d{4}$')
]

class AssignmentBase(BaseModel):
    user_id: int
    name: str
    course: str
    course_id: str = "0000"
    due_date: str
    due_time: str | None = None
    assignment_type: str | None = None
    priority_level: int | None = None
    points: float | None = None


class AssignmentCreate(BaseModel):
    user_id: int
    name: str
    course: str
    course_id: str = "0000"
    due_date: str
    due_time: str | None = None #Added this because these fields are required but have no default value which would lead to a validation error. This automatically sets them to None if they are not provided in the request body.
    assignment_type: str | None = None
    priority_level: int | None = None
    points: float | None = None
    pass


class AssignmentUpdate(BaseModel):
    user_id: int | None = None
    name: str | None = None
    course: str | None = None
    course_id: CourseID | None = None
    due_date: str | None = None
    due_time: str | None = None
    assignment_type: str | None = None
    priority_level: int | None = None
    points: float | None = None


class AssignmentResponse(AssignmentBase):
    id: int

    class Config:
        from_attributes = True  
