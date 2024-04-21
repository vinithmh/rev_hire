from fastapi import Depends, status, APIRouter
from rev_hire.schemas import JobSeeker, showJobSeeker
from sqlalchemy.orm import Session
from rev_hire.database import get_db
from rev_hire.repository import jobseeker

router = APIRouter(
    tags=['JobSeeker']
)

@router.post('/jobseeker', status_code=status.HTTP_201_CREATED)
def create_jobseeker(request: JobSeeker, db: Session = Depends(get_db)):
    return jobseeker.create_jobseeker(request, db)


@router.get('/jobseekers', status_code=status.HTTP_200_OK, response_model=list[showJobSeeker])
def get_jobseekers(db: Session = Depends(get_db)):
    return jobseeker.get_jobseekers(db)


@router.get('/jobseeker/{id}', status_code=status.HTTP_200_OK, response_model=showJobSeeker)
def get_jobseeker(id, db: Session = Depends(get_db)):
    return jobseeker.get_jobseeker(id, db)


@router.put('/jobseeker/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_jobseeker(id, request: JobSeeker, db: Session = Depends(get_db)):
    return jobseeker.update_jobseeker(id, request, db)


@router.delete('/jobseeker/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_jobseeker(id, db: Session = Depends(get_db)):
    return jobseeker.delete_jobseeker(id, db)

