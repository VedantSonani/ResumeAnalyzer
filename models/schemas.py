from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
# from datetime import year

class Prompt(BaseModel):
    msg : str = Field(..., min_length=1)

from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class School(BaseModel):
    name: str = Field(description="Name of the university or college")
    course: str = Field(description="Degree or major, e.g., 'B.S. in Computer Science'")
    cgpa: Optional[float] = Field(
        None, ge=0, le=10, 
        description="CGPA/GPA score. If not mentioned, leave as null."
    )
    start_year: Optional[int] = Field(None, ge=1950, le=2026)
    end_year: Optional[int] = Field(None, ge=1950, le=2040)

class Certification(BaseModel):
    title: str = Field(description="Name of the certification")
    issuer: Optional[str] = Field(None, description="Organization that issued the certificate")
    year: Optional[int] = Field(None, ge=1950, le=2026)

class Project(BaseModel):
    name: str = Field(description="Title of the project")
    description: str = Field(description="Brief summary of what the project does and the candidate's contribution")
    tech_stack: List[str] = Field(default_factory=list, description="List of technologies, languages, or frameworks used")
    start_year: Optional[int] = Field(None, ge=1950, le=2026)
    end_year: Optional[int] = Field(None, ge=1950, le=2040)

class Company(BaseModel):
    name: str = Field(description="Name of the company")
    designation: str = Field(description="Job title or role held")
    responsibilities: List[str] = Field(
        default_factory=list, 
        description="Bullet points of key achievements and tasks performed"
    )
    start_year: int = Field(ge=1950, le=2026)
    end_year: Optional[int] = Field(None, ge=1950, le=2040, description="Leave null if currently working there")

class Resume(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: EmailStr = Field(description="Candidate's contact email address")
    github: Optional[str] = Field(None, description="URL or username for GitHub")
    linkedin: Optional[str] = Field(None, description="URL for LinkedIn profile")
    
    # Using default_factory=list ensures the model returns [] instead of crashing
    education: List[School] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list, description="Hard and soft skills extracted")
    projects: List[Project] = Field(default_factory=list)
    experience: List[Company] = Field(default_factory=list)
    certificates: List[Certification] = Field(default_factory=list)

    # Not Deterministic
    summary: str = Field(description="A 2-3 sentence professional summary of the candidate's profile.")
    career_level: str = Field(description="Categorize as: Entry-level, Mid-level, Senior, or Executive.")