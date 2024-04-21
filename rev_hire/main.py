from fastapi import FastAPI, Depends, status, HTTPException
from rev_hire.schemas import JobSeeker, showJobSeeker, Employer, showEmployer, JobPosting, showJobPosting, JobApplication, showJobApplication
from sqlalchemy.orm import Session
from rev_hire import models, database
from rev_hire.hashing import Hash
from typing import List
from rev_hire.routers import jobseeker, employer, jobposting, jobapplication, jobseeker_login

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(jobseeker.router)
app.include_router(employer.router)
app.include_router(jobposting.router)
app.include_router(jobapplication.router)
app.include_router(jobseeker_login.router)















    