from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from rev_hire.database import get_db
from rev_hire.schemas import JobSeeker
from rev_hire.hashing import Hash
from rev_hire import models
from fastapi.responses import JSONResponse

def create_jobseeker(request: JobSeeker, db: Session = Depends(get_db)):
    existing_jobseeker = db.query(models.JobSeeker).filter(models.JobSeeker.email == request.email).first()
    if existing_jobseeker:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    try:
        new_jobseeker = models.JobSeeker(name=request.name, email=request.email, phone=request.phone, password=Hash.hash(request.password))
        db.add(new_jobseeker)
        db.commit()
        db.refresh(new_jobseeker)
        return {"message": "Jobseeker account created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create jobseeker")
    
def get_jobseekers(db: Session = Depends(get_db)):
    jobseekers = db.query(models.JobSeeker).all()
    if not jobseekers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No jobseekers found')
    return jobseekers

def get_jobseeker(id, db: Session = Depends(get_db)):
    jobseeker = db.query(models.JobSeeker).filter(models.JobSeeker.id == id).first()
    if not jobseeker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Jobseeker with id {id} not found')
    return jobseeker

def update_jobseeker(id, request: JobSeeker, db: Session = Depends(get_db)):
    try:
        updated_count = db.query(models.JobSeeker).filter(models.JobSeeker.id == id).update(request.dict(), synchronize_session=False)
        if updated_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Jobseeker with id {id} not found')
        db.commit()
        return {"message": "Jobseeker updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update jobseeker")
    
def delete_jobseeker(id, db: Session = Depends(get_db)):
    try:
        deleted_count = db.query(models.JobSeeker).filter(models.JobSeeker.id == id).delete(synchronize_session=False)
        if deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Jobseeker with id {id} not found')
        db.commit()
        return JSONResponse(content={"message": "Jobseeker deleted successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete jobseeker")