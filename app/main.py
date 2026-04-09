# FastAPI backend server for managing assignments
# This server provides REST API endpoints for CRUD operations on assignments

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.schemas import AssignmentCreate, AssignmentUpdate, AssignmentResponse
from app.assignment_model import Assignment

# Please run this command to run the backend api:
# python -m uvicorn app.main:app --reload

# Create all database tables based on defined models
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI()

# CREATE - POST endpoint to create a new assignment
# Status: 201 Created on success
# Accepts: AssignmentCreate object with assignment details
# Returns: Created assignment with auto-generated id
@app.post("/assignments/", status_code=status.HTTP_201_CREATED, response_model=AssignmentResponse)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    # Convert Pydantic model to dict and create SQLAlchemy object
    db_assignment = Assignment(**assignment.model_dump())
    # Add to database session
    db.add(db_assignment)
    # Commit transaction to save to database
    db.commit()
    # Refresh object to get auto-generated id and other fields
    db.refresh(db_assignment)
    return db_assignment


# READ - GET endpoint to retrieve a single assignment by id
# Returns: Assignment data if found, or 404 error if not found
@app.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
def read_assignment(assignment_id: int, db: Session = Depends(get_db)):
    # Query database for assignment with matching id
    db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    # Raise 404 error if assignment doesn't exist
    if db_assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return db_assignment


# UPDATE - PUT endpoint to update an existing assignment
# Only fields with non-None values are updated (partial updates supported)
# Returns: Updated assignment data
@app.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(assignment_id: int, assignment: AssignmentUpdate, db: Session = Depends(get_db)):
    # Find assignment by id
    db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    # Raise 404 if not found
    if db_assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    # Update only fields that were provided (not None)
    for var, value in vars(assignment).items():
        if value is not None:
            setattr(db_assignment, var, value)
    # Commit changes to database
    db.commit()
    # Refresh to get latest data
    db.refresh(db_assignment)
    return db_assignment


# DELETE - DELETE endpoint to remove an assignment
# Status: 204 No Content on success (no response body)
# Returns: 404 error if assignment not found
@app.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    # Find assignment by id
    db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    # Raise 404 if not found
    if db_assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    # Delete from database
    db.delete(db_assignment)
    # Commit transaction to persist deletion
    db.commit()
    return