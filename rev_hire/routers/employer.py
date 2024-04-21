from fastapi import FastAPI, Depends, status, APIRouter
from rev_hire.schemas import Employer, showEmployer
from sqlalchemy.orm import Session
from rev_hire.database import get_db
from rev_hire.repository import employer

router = APIRouter(
    tags=['Employer']
)

@router.post('/employer', status_code=status.HTTP_201_CREATED)
def create_employer(request: Employer, db: Session = Depends(get_db)):
    return employer.create_employer(request, db)


@router.get('/employers', status_code=status.HTTP_200_OK, response_model=list[showEmployer])
def get_employers(db: Session = Depends(get_db)):
    return employer.get_employers(db)


@router.get('/employer/{id}', status_code=status.HTTP_200_OK, response_model=showEmployer)  
def get_employer(id, db: Session = Depends(get_db)):
    return employer.get_employer(id, db)  


@router.put('/employer/{id}', status_code=status.HTTP_202_ACCEPTED) 
def update_employer(id, request: Employer, db: Session = Depends(get_db)):
    return employer.update_employer(id, request, db)   


@router.delete('/employer/{id}', status_code=status.HTTP_204_NO_CONTENT)   
def delete_employer(id, db: Session = Depends(get_db)):
    return employer.delete_employer(id, db)

