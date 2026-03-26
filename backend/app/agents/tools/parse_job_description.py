from langchain_core.tools import tool
from app.core.gemini import LLM
from app.models import JobDescriptionModel

@tool
def parse_job_description(jd_text: str) -> dict:
    """
    Parses the raw job description text to extract structured information such as required skills, 
    experience level, education requirements, and other relevant details. 

    Use this tool when the user provides a job description and asks for candidate recommendations 
    or when you need to break down the JD into specific components for targeted semantic searches.

    Args:
        jd_text (str): The unstructured text of the job description."""
    model = LLM
    structured_output = model.with_structured_output(JobDescriptionModel, method="function_calling")
    job_description = structured_output.invoke(jd_text)
    
    return job_description.model_dump()