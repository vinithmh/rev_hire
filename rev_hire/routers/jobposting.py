from fastapi import Depends, status, APIRouter
from rev_hire.schemas import JobPosting, showJobPosting, updateJobPosting, Employer
from sqlalchemy.orm import Session
from rev_hire.database import get_db
from typing import List
from rev_hire.repository import jobposting

router = APIRouter(
    tags=['JobPosting']
)

@router.post('/jobposting', status_code=status.HTTP_201_CREATED)
def create_jobposting(request: JobPosting, db: Session = Depends(get_db)):
    return jobposting.create_jobposting(request, db)


@router.get('/jobposting/{id}', status_code=status.HTTP_200_OK, response_model=showJobPosting)
def get_jobposting(id, db: Session = Depends(get_db)):
    return jobposting.get_jobposting(id, db)


@router.get('/jobpostings/employer/{employer_id}', status_code=status.HTTP_200_OK, response_model=List[showJobPosting])
def get_jobpostings_by_employer(employer_id: int, db: Session = Depends(get_db)):
    return jobposting.get_jobpostings_by_employer(employer_id, db)


@router.put('/jobposting/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_jobposting(id, request: updateJobPosting, db: Session = Depends(get_db)):
    return jobposting.update_jobposting(id, request, db)


@router.delete('/jobposting/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_jobposting(id, db: Session = Depends(get_db)):
    return jobposting.delete_jobposting(id, db)

