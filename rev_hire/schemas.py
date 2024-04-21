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

class updateJobPosting(BaseModel):
    title: str
    company: str
    class Config():
        orm_mode = True
    
class showJobPosting(BaseModel):
    title: str
    company: str
    creator: showEmployer
    class Config():
        orm_mode = True

class JobApplicationBase(BaseModel):
    email: str
    resume: str
    skills: str

class JobApplication(JobApplicationBase):
    pass

class updateJobApplication(BaseModel):
    email: str
    resume: str
    skills: str
    class Config():
        orm_mode = True

class showJobApplication(BaseModel):
    email: str
    resume: str
    skills: str
    class Config(): 
        orm_mode = True

class jobSeekerLogin(BaseModel):
    email: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


