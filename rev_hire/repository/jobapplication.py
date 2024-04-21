from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from rev_hire.database import get_db
from rev_hire.schemas import JobApplication
from rev_hire import models
from fastapi.responses import JSONResponse

def create_job_application(request: JobApplication, db: Session = Depends(get_db)):
    jobseeker = db.query(models.JobSeeker).filter(models.JobSeeker.email == request.email).first()
    if not jobseeker:
        raise HTTPException(status_code=404, detail="Job seeker doesn't exist. Please create a job seeker account.")
    try:
        job_application = models.JobApplication(jobseeker_id=jobseeker.id, email=request.email, resume=request.resume, skills=request.skills)
        db.add(job_application)
        db.commit()
        db.refresh(job_application)
        return {"message": "Job application created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create job application")
    
def get_job_application(id, db : Session = Depends(get_db)):
    job_application = db.query(models.JobApplication).filter(models.JobApplication.id == id).first()
    if not job_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No job application found')
    return job_application

def get_job_applications_by_jobseeker(jobseeker_id: int, db: Session = Depends(get_db)):
    job_applications = db.query(models.JobApplication).filter(models.JobApplication.jobseeker_id == jobseeker_id).all()
    if not job_applications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No job applications found for job seeker ID: {jobseeker_id}')
    return job_applications

def update_job_application(id, request: JobApplication, db : Session = Depends(get_db)):
    try:
        job_application = db.query(models.JobApplication).filter(models.JobApplication.id == id).update(request.dict(), synchronize_session=False)
        if not job_application: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No job application found') 
        db.commit()
        return {"message": "Job application updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update job application")
    
def delete_job_application(id, db : Session = Depends(get_db)):
    try:
        job_application = db.query(models.JobApplication).filter(models.JobApplication.id == id).delete(synchronize_session=False)
        if not job_application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No job application found')
        db.commit()
        return JSONResponse(content={"message": "Job posting deleted successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete job application")