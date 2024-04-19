from pydantic import BaseModel
from typing import List

class JobSeeker(BaseModel):
    name: str
    email: str
    phone: str
    password: str

class showJobSeeker(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    class Config():
        orm_mode = True

class Employer(BaseModel):
    name: str
    email: str
    phone: str
    password: str

class showEmployer(BaseModel):
    id: int
    name: str
    email: str
    phone: str 

    class Config():
        orm_mode = True

class JobPostingBase(BaseModel):
    title: str
    company: str
    email: str

class JobPosting(JobPostingBase):
    pass


class showJobPosting(BaseModel):
    id: int
    employer_id: int
    title: str
    company: str
    creator: showEmployer
    class Config():
        orm_mode = True

class JobApplicationBase(BaseModel):
    email: str
    resume: str
    skills: str
    jobpost: JobPosting

class JobApplication(JobApplicationBase):
    pass

class showJobApplication(BaseModel):
    id: int
    jobseeker_id: int
    jobposting_id: int
    email: str
    resume: str
    skills: str
    title: str
    class Config(): 
        orm_mode = True

