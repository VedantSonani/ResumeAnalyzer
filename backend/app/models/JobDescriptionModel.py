from pydantic import BaseModel, Field
from typing import Optional, List

class JobDescriptionModel(BaseModel):
    title: str = Field(description="The formal job title")
    role_summary: str = Field(description="A concise summary of the role's mission")
    
    responsibilities: List[str] = Field(description="Key tasks and duties")
    
    technical_skills: List[str] = Field(description="Must-have technical tools and frameworks")
    preferred_skills: Optional[List[str]] = Field(default=None, description="Nice-to-have skills")
    
    education_criteria: str = Field(description="Degree and specialization required")
    min_experience_years: Optional[int] = Field(default=None, description="Minimum years of experience")
  