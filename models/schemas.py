from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import Optional, List
from datetime import date

class Prompt(BaseModel):
    msg : str = Field(..., min_length=1)

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
    # add a default value for start_year
    start_month: Optional[int] = Field(None, ge=1, le=12, description="The numerical month (1-12) the candidate began this specific job")
    start_year: Optional[int] = Field(None, ge=1950, le=2026, description="The four-digit calendar year the candidate started this role.")
    end_month: Optional[int] = Field(None, ge=1, le=12, description="The numerical month (1-12) the candidate completed this role. If null, the role is assumed to be 'Present'.")
    end_year: Optional[int] = Field(None, ge=1950, le=2040, description="The year the candidate left this role. Use 'None' (null) if the candidate is currently employed here.")

    @property
    def total_months(self) -> int:
        # If end_year is null, use current year/month for "Present"
        end_y = self.end_year or date.today().year
        end_m = self.end_month or date.today().month
        
        return (end_y * 12 + end_m) - (self.start_year * 12 + self.start_month) + 1 # +1 to include the starting month in the count

    @computed_field
    @property
    def duration_string(self) -> str:
        if not self.start_year:
            return 0
    
        years = self.total_months // 12
        months = self.total_months % 12
        if years > 0:
            return f"{years} years" + (f" {months} months" if months > 0 else "")
        
        if months > 0:
            return f"{months} months"
        
        return "Less than a month"
        
class Resume(BaseModel):
    name: str = Field(description="Full name of the candidate")
    phone: Optional[str] = Field(None, description="Contact phone number")
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