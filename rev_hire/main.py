from fastapi import FastAPI, Depends, status, HTTPException
from rev_hire.schemas import JobSeeker, showJobSeeker, Employer, showEmployer, JobPosting, showJobPosting, JobApplication, showJobApplication
from sqlalchemy.orm import Session
from rev_hire import models, database
from rev_hire.hashing import Hash
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/jobseeker', status_code=status.HTTP_201_CREATED, tags=['JobSeeker']) 
def create_jobseekers(request: JobSeeker, db : Session = Depends(get_db)):
    new_jobseeker = models.JobSeeker(name = request.name, email = request.email, phone = request.phone, password = Hash.hash(request.password))
    db.add(new_jobseeker)
    db.commit()
    db.refresh(new_jobseeker)
    return new_jobseeker

@app.get('/jobseekers', status_code=status.HTTP_200_OK, response_model=list[JobSeeker], tags=['JobSeeker'])
def get_jobseekers(db : Session = Depends(get_db)):
    jobseekers = db.query(models.JobSeeker).all()
    if not jobseekers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No jobseekers found')
    return jobseekers

@app.get('/jobseeker/{id}', status_code=status.HTTP_200_OK,response_model=showJobSeeker, tags=['JobSeeker'])
def get_jobseeker(id, db : Session = Depends(get_db)):
    jobseeker = db.query(models.JobSeeker).filter(models.JobSeeker.id == id).first()
    if not jobseeker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Jobseeker with id {id} not found')
    return jobseeker

@app.delete('/jobseeker/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['JobSeeker'])
def delete_jobseeker(id, db : Session = Depends(get_db)):
    jobseeker = db.query(models.JobSeeker).filter(models.JobSeeker.id == id).delete(synchronize_session=False)
    if not jobseeker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Jobseeker with id {id} not found')
    db.commit()
    return jobseeker

@app.put('/jobseeker/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['JobSeeker'])
def update_jobseeker(id, request: JobSeeker, db : Session = Depends(get_db)):
    jobseeker = db.query(models.JobSeeker).filter(models.JobSeeker.id == id).update(request.dict(), synchronize_session=False)
    if not jobseeker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Jobseeker with id {id} not found')
    db.commit()
    return jobseeker

@app.post('/employer', status_code=status.HTTP_201_CREATED, tags=['Employer'])
def create_employer(request: Employer, db : Session = Depends(get_db)):
    new_employer = models.Employer(name = request.name, email = request.email, phone = request.phone, password = Hash.hash(request.password))
    db.add(new_employer)
    db.commit()
    db.refresh(new_employer)
    return new_employer

@app.get('/employers', status_code=status.HTTP_200_OK, response_model=showEmployer, tags=['Employer']) 
def get_employer(db : Session = Depends(get_db)):
    employer = db.query(models.Employer).first()
    if not employer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No employer found')
    return employer 

@app.get('/employer/{id}', status_code=status.HTTP_200_OK, response_model=showEmployer, tags=['Employer'])    
def get_employer(id, db : Session = Depends(get_db)):
    employer = db.query(models.Employer).filter(models.Employer.id == id).first()
    if not employer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No employer found')
    return employer

@app.put('/employer/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Employer'])    
def update_employer(id, request: Employer, db : Session = Depends(get_db)):
    employer = db.query(models.Employer).filter(models.Employer.id == id).update(request.dict(), synchronize_session=False)
    if not employer: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No employer found') 
    db.commit()
    return employer

@app.delete('/employer/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Employer'])   
def delete_employer(id, db : Session = Depends(get_db)):
    employer = db.query(models.Employer).filter(models.Employer.id == id).delete(synchronize_session=False)
    if not employer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No employer found')
    db.commit()
    return employer

@app.post('/jobposting', status_code=status.HTTP_201_CREATED, tags=['JobPosting'])
def create_jobposting(request: JobPosting, db: Session = Depends(get_db)):
    # Check if the employer email exists
    employer = db.query(models.Employer).filter(models.Employer.email == request.email).first()
    if not employer:
        raise HTTPException(status_code=404, detail="Employer doesn't exist. Please create an employer account.")

    # Add job posting details
    job_posting = models.JobPosting(title=request.title, company=request.company, email=request.email, employer_id=employer.id)
    db.add(job_posting)
    db.commit()
    db.refresh(job_posting)
    return job_posting

@app.get('/jobposting/{id}', status_code=status.HTTP_200_OK, response_model=showJobPosting, tags=['JobPosting'])
def get_jobposting(id, db : Session = Depends(get_db)):
    job_posting = db.query(models.JobPosting).filter(models.JobPosting.id == id).first()
    if not job_posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No job posting found')
    return job_posting

@app.get('/jobpostings/employer/{employer_id}', status_code=status.HTTP_200_OK, response_model=List[showJobPosting], tags=['JobPosting'])
def get_jobpostings_by_employer(employer_id: int, db: Session = Depends(get_db)):
    job_postings = db.query(models.JobPosting).filter(models.JobPosting.employer_id == employer_id).all()
    if not job_postings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No job postings found for employer ID: {employer_id}')
    return job_postings

@app.put('/jobposting/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['JobPosting'])
def update_jobposting(id, request: JobPosting, db : Session = Depends(get_db)):
    job_posting = db.query(models.JobPosting).filter(models.JobPosting.id == id).update(request.dict(), synchronize_session=False)
    if not job_posting: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No job posting found') 
    db.commit()
    return job_posting

@app.delete('/jobposting/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['JobPosting'])
def delete_jobposting(id, db : Session = Depends(get_db)):
    job_posting = db.query(models.JobPosting).filter(models.JobPosting.id == id).delete(synchronize_session=False)
    if not job_posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No job posting found')
    db.commit()
    return job_posting

@app.post('/jobapplication', status_code=status.HTTP_201_CREATED, tags=['JobApplication'])
def create_job_application(request: JobApplication, db: Session = Depends(get_db)):
    # Check if the job seeker exists
    jobseeker = db.query(models.JobSeeker).filter(models.JobSeeker.email == request.email).first()
    if not jobseeker:
        raise HTTPException(status_code=404, detail="Job seeker doesn't exist. Please create a job seeker account.")
    

    # Add job application details
    job_application = models.JobApplication(jobseeker_id=jobseeker.id, email=request.email, resume=request.resume, skills=request.skills)
    db.add(job_application)
    db.commit()
    db.refresh(job_application)
    return job_application


    