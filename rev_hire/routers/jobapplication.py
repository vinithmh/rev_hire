from fastapi import Depends, status, APIRouter
from rev_hire.schemas import JobApplication, showJobApplication, JobSeeker
from sqlalchemy.orm import Session
from rev_hire.database import get_db
from typing import List
from rev_hire.repository import jobapplication
from rev_hire.oauth2 import get_current_user

router = APIRouter(
    tags=['JobApplication']
)

@router.post('/jobapplication', status_code=status.HTTP_201_CREATED)
def create_job_application(request: JobApplication, db: Session = Depends(get_db), get_current_user: JobSeeker = Depends(get_current_user)):
    return jobapplication.create_job_application(request, db)


@router.get('/jobapplication/{id}', status_code=status.HTTP_200_OK, response_model=showJobApplication)
def get_job_application(id, db: Session = Depends(get_db), get_current_user: JobSeeker = Depends(get_current_user)):
    return jobapplication.get_job_application(id, db)

@router.get('/jobapplications/jobseeker/{jobseeker_id}', status_code=status.HTTP_200_OK, response_model=List[showJobApplication])
def get_job_applications_by_jobseeker(jobseeker_id: int, db: Session = Depends(get_db), get_current_user: JobSeeker = Depends(get_current_user)):
    return jobapplication.get_job_applications_by_jobseeker(jobseeker_id, db)

@router.put('/jobapplication/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_job_application(id, request: JobApplication, db : Session = Depends(get_db), get_current_user: JobSeeker = Depends(get_current_user)):
    return jobapplication.update_job_application(id, request, db)

@router.delete('/jobapplication/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_job_application(id, db : Session = Depends(get_db), get_current_user: JobSeeker = Depends(get_current_user)):
    return jobapplication.delete_job_application(id, db)

