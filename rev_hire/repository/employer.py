from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from rev_hire.database import get_db
from rev_hire.schemas import Employer
from rev_hire import models
from rev_hire.hashing import Hash
from fastapi.responses import JSONResponse

def create_employer(request: Employer, db: Session = Depends(get_db)):
    existing_employer = db.query(models.Employer).filter(models.Employer.email == request.email).first()
    if existing_employer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    try:
        new_employer = models.Employer(name=request.name, email=request.email, phone=request.phone, password=Hash.hash(request.password))
        db.add(new_employer)
        db.commit()
        db.refresh(new_employer)
        return {"message": "Employer account created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create employer")
    
def get_employers(db: Session = Depends(get_db)):
    employers = db.query(models.Employer).all()
    if not employers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No employers found')
    return employers

def get_employer(id, db: Session = Depends(get_db)):
    employer = db.query(models.Employer).filter(models.Employer.id == id).first()
    if not employer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Employer not found')
    return employer

def update_employer(id, request: Employer, db: Session = Depends(get_db)):
    try:
        updated_count = db.query(models.Employer).filter(models.Employer.id == id).update(request.dict(), synchronize_session=False)
        if updated_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Employer not found')
        db.commit()
        return {"message": "Employer updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update employer")
    

def delete_employer(id, db: Session = Depends(get_db)):
    try:
        deleted_count = db.query(models.Employer).filter(models.Employer.id == id).delete(synchronize_session=False)
        if deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Employer not found')
        db.commit()
        return JSONResponse(content={"message": "Employer deleted successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete employer")



