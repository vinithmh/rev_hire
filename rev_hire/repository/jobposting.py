from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from rev_hire.database import get_db
from rev_hire.schemas import JobPosting, updateJobPosting
from rev_hire import models
from fastapi.responses import JSONResponse


def create_jobposting(request: JobPosting, db: Session = Depends(get_db)):
    employer = db.query(models.Employer).filter(models.Employer.email == request.email).first()
    if not employer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer doesn't exist. Please create an employer account.")
    try:
        job_posting = models.JobPosting(title=request.title, company=request.company, email=request.email, employer_id=employer.id)
        db.add(job_posting)
        db.commit()
        db.refresh(job_posting)
        return {"message": "Job posting created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create job posting")
    
def get_jobposting(id, db: Session = Depends(get_db)):
    job_posting = db.query(models.JobPosting).filter(models.JobPosting.id == id).first()
    if not job_posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Job posting with id {id} not found')
    return job_posting

def get_jobpostings_by_employer(employer_id: int, db: Session = Depends(get_db)):
    job_postings = db.query(models.JobPosting).filter(models.JobPosting.employer_id == employer_id).all()
    if not job_postings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No job postings found for employer ID: {employer_id}')
    return job_postings

def update_jobposting(id, request: updateJobPosting, db: Session = Depends(get_db)):
    try:
        updated_count = db.query(models.JobPosting).filter(models.JobPosting.id == id).update(request.dict(), synchronize_session=False)
        if updated_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Job posting with id {id} not found')
        db.commit()
        return {"message": "Job posting updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update job posting")
    
def delete_jobposting(id, db: Session = Depends(get_db)):
    try:
        deleted_count = db.query(models.JobPosting).filter(models.JobPosting.id == id).delete(synchronize_session=False)
        if deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Job posting with id {id} not found')
        db.commit()
        return JSONResponse(content={"message": "Job posting deleted successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete job posting")