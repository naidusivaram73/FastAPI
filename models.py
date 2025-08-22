# models.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class Education(BaseModel):
    institution: str
    degree: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    description: Optional[str] = None

class Experience(BaseModel):
    company: str
    title: Optional[str] = None
    start_date: Optional[str] = None  # ISO date or free text
    end_date: Optional[str] = None
    description: Optional[str] = None

class Project(BaseModel):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None

class ResumeBase(BaseModel):
    fullname: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    phone: Optional[str] = Field(None, example="+1 555 1234")
    summary: Optional[str] = Field(None, example="Software engineer...")
    skills: Optional[List[str]] = []
    education: Optional[List[Education]] = []
    experience: Optional[List[Experience]] = []
    projects: Optional[List[Project]] = []

class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    summary: Optional[str]
    skills: Optional[List[str]]
    education: Optional[List[Education]]
    experience: Optional[List[Experience]]
    projects: Optional[List[Project]]
