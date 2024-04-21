from rev_hire.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class JobSeeker(Base):
    __tablename__ = "jobseekers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)

    jobapplication = relationship("JobApplication", back_populates="jobseeker")

class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    password = Column(String)

    jobposting = relationship("JobPosting", back_populates="creator")

class JobPosting(Base):
    __tablename__ = "jobpostings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    email = Column(String)
    employer_id = Column(Integer, ForeignKey("employers.id"))

    creator = relationship("Employer", back_populates="jobposting")

class JobApplication(Base):
    __tablename__ = "jobapplications"

    id = Column(Integer, primary_key=True, index=True)
    jobseeker_id = Column(Integer, ForeignKey("jobseekers.id"))
    email = Column(String)
    resume = Column(String)
    skills = Column(String)

    jobseeker = relationship("JobSeeker", back_populates="jobapplication")

