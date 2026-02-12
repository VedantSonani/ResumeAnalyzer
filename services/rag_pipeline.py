import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from pinecone import Pinecone
from typing import List, Tuple
from models import schemas
 
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ----PINECODE SETUP----
PINECODE_API_KEY = os.getenv("PINECODE_API_KEY")

pc = Pinecone(api_key=PINECODE_API_KEY)
index_name = "resume-analyzer"
index = pc.Index(index_name)
embeddings = PineconeEmbeddings(model="llama-text-embed-v2", api_key=PINECODE_API_KEY)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)
# ------------------------

SYSTEM_PROMPT = ""

LLM = ChatGoogleGenerativeAI(
        # model = "gemma-3-12b-it",
        # model = "gemini-2.5-flash",
        # model="gemini-2.5-flash-lite",
        # model="gemini-2.5-pro",
        model = "gemini-3-flash-preview",
        api_key = GEMINI_API_KEY,
        temperature=0.5,  
        max_tokens=None,
        timeout=None,
        max_retries=1
)

def get_prompt(user_prompt):
    # gemma models dont take system instructions
    prompt = [
        ("system", SYSTEM_PROMPT),
        ("human", user_prompt)
    ]

    return prompt

async def get_response(message):
    response = await agent_executor.ainvoke({"input": message, "chat_history": []})
    response = response['output'][0]['text']

    return response

@tool
def perform_sementic_search(query: str, top_k: int, filter: List[str]=None) -> List[Tuple]:
    """
        Performs a semantic (context-based) search across the vector database to retrieve 
        the most relevant information based on conceptual similarity rather than exact 
        keyword matches. 

        Use this tool when the user asks complex questions, seeks background information, 
        or when a direct keyword search fails to provide depth. 

        Args:
            query (str): The natural language search string or question.
            top_k (int): The number of highly relevant documents to return.
            filter (List[str], optional): A list of metadata tags to narrow the search scope.

        Returns:
            List[Tuple]: A ranked list of search results with their corresponding similarity scores. 
                Returns an empty list if no results meet the minimum relevance threshold (0.15).
        """
    search_results = vector_store.similarity_search_with_score(query, k=top_k, filter=filter)

    if search_results[0][-1] < 0.15:
        return []  # No relevant results found
    return search_results

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
    structured_output = model.with_structured_output(schemas.JobDescriptionModel, method="function_calling")
    job_description = structured_output.invoke(jd_text)
    
    return job_description.model_dump()


# --------------AGENT SETUP------------------------------------------------------------
AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
## ⚠️ STRICT RULE — READ FIRST
You have NO knowledge of any candidates or resumes. 
Every candidate name, skill, score, and detail in your response 
MUST come exclusively from the `perform_sementic_search` tool results.
NEVER invent, assume, or hallucinate candidate information.
If the tool returns no results, say: "No candidates found in the database."

---
You are an expert AI Recruitment Analyst specializing in matching candidates to job descriptions.
Your job is to parse a job description, extract structured requirements, and retrieve the most 
suitable candidates from the vector database using targeted semantic searches.

---

## YOUR WORKFLOW

Follow these steps precisely for every request — DO NOT SKIP ANY STEP:

### STEP 1 — Parse the Job Description (MANDATORY FIRST ACTION)
ALWAYS call `parse_job_description` first before doing anything else.
Pass the complete job description text as the argument.
This will return a structured object containing:
- `core_skills`: Primary technical skills required
- `domain_knowledge`: Field-specific expertise areas
- `education`: Degree, specialization, graduation year, GPA
- `experience_level`: Fresher / Junior / Mid / Senior
- `soft_skills`: Collaboration, problem-solving, communication
- `nice_to_haves`: Optional or bonus qualifications
- `search_queries`: Pre-extracted targeted queries to use in Step 2

You MUST wait for this tool's response before proceeding.

### STEP 2 — Run Targeted Semantic Searches
Using the structured output from `parse_job_description`, call `perform_sementic_search` 
ONCE for EACH of the following aspects — minimum 5 search calls:

  1. One query built from `core_skills` fields
  2. One query built from `domain_knowledge` fields  
  3. One query built from `education` + `experience_level` fields
  4. One query built from `nice_to_haves` fields
  5. One query built from project/work experience alignment

Use `top_k=10` for every query to cast a wide net before re-ranking.
DO NOT generate your own queries from scratch — derive them from Step 1's output only.

### STEP 3 — Aggregate & Deduplicate Results
- Collect all results across all search calls
- Remove duplicate candidates (same name appearing multiple times)
- Track how many queries each candidate appeared in (frequency score)

### STEP 4 — Score & Rank Candidates Deterministically
For each unique candidate, compute a holistic match score using ONLY 
information returned by the search tool:

| Factor                        | Weight  |
|-------------------------------|---------|
| Core technical skill overlap  | 35%     |
| Domain/project relevance      | 25%     |
| Education match               | 15%     |
| Soft skills & mindset fit     | 10%     |
| Bonus/nice-to-have skills     | 10%     |
| Frequency across search hits  | 5%      |

Scoring rules:
- Compute final_score = (weighted_score × 0.7) + (frequency_ratio × 0.3)
- frequency_ratio = queries_appeared_in / total_queries_run
- Only shortlist candidates with a final score of 65% or above
- In case of a tie, rank by frequency_ratio first, then core skill overlap

### STEP 5 — Return the Top N Candidates
Return exactly the number of candidates the user requested (top N).
If fewer than N candidates meet the 65% threshold, return however many do and explain why.

---

## OUTPUT FORMAT

Present your final answer in this exact structure:

## 🏆 Top [N] Candidates for: [Job Title from JD]

---

### Rank #1 — [Candidate Full Name]
**Overall Match Score**: XX%

**Why They're a Strong Fit**:
[2–3 sentences summarizing why this candidate matches the JD well]

**Matched Requirements**:
- ✅ [Requirement 1]: [Evidence from their profile]
- ✅ [Requirement 2]: [Evidence from their profile]
- ✅ [Requirement 3]: [Evidence from their profile]

**Gaps / Areas to Probe in Interview**:
- ⚠️ [Gap 1]
- ⚠️ [Gap 2]

---
[Repeat for all N candidates]

---
## 📊 Search Summary
- JD parsed via: parse_job_description ✅
- Queries run: [X]
- Total candidates retrieved: [Y]  
- Candidates meeting threshold (≥65%): [Z]

---

## RULES & GUARDRAILS

- `parse_job_description` MUST be the first tool call — no exceptions.
- `perform_sementic_search` queries MUST be derived from `parse_job_description` output — never invented.
- Always run at least 5 separate search queries.
- Never hallucinate candidate details — only use information returned by the search tool.
- If a candidate's profile lacks information for a category, mark it as "Not mentioned in profile".
- Be objective and bias-free — do not factor in names, gender, or nationality in scoring.
- If the vector database returns no results, clearly inform the user and suggest checking if resumes are indexed.
- Always deliver exactly N candidates if possible.
"""),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

tools = [perform_sementic_search, parse_job_description]

agent = create_tool_calling_agent(
    tools=tools,
    llm=LLM,
    prompt=AGENT_PROMPT
    )

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# response =  agent_executor.invoke({"input": """
#                                    We are looking for top 2 candidates who match this Job Description:
#     Job Description: Junior AI/ML Engineer (2026 Graduate Program)

# Role Overview We are seeking high-potential Junior AI/ML Engineers to join our 2026 Graduate Cohort. This role is designed for final-year students who have demonstrated a passion for Generative AI and production-grade Machine Learning. You will work on integrating Large Language Models (LLMs) into real-world applications and optimizing data pipelines.
# 1. Key Responsibilities

#     AI Feature Development: Build and deploy LLM-powered features using RAG (Retrieval-Augmented Generation) frameworks.

#     Full-Stack Integration: Integrate AI models into web applications using Python (Django/Flask).

#     Data Engineering: Develop automated data pipelines and perform exploratory data analysis (EDA) to improve model performance.

#     Evaluation: Implement evaluation metrics to measure model accuracy and reduce hallucinations in generative outputs.

# 2. Technical Requirements (Entry-Level)

#     Programming: Deep proficiency in Python (Pandas, NumPy, Scikit-learn, PyTorch/TensorFlow).

#     Generative AI: Hands-on experience with LangChain, Hugging Face, or OpenAI APIs.

#     Vector Databases: Familiarity with vector embeddings and tools like FAISS, Pinecone, or pgvector.

#     Cloud & Tools: Basic understanding of AWS (S3, Lambda) and version control using Git/GitHub.

# 3. Education & Soft Skills

#     Education: Currently pursuing a B.E./B.Tech in Computer Engineering, AI, or Machine Learning (Class of 2026).

#     Academic Excellence: A minimum CGPA of 8.0 or equivalent.

#     Mindset: Strong analytical problem-solving skills and the ability to work in a collaborative, fast-paced team environment.
#     """,
#     "chat_history": []})

# response =  agent_executor.invoke({"input": """ 
# Get me top 3 candidates that are good match for the following Job Description:

# Job Description: Junior Generative AI Developer (2026 Graduate Cohort)

# Role Overview:
# We are hiring a Junior Generative AI Developer for our 2026 graduate batch. 
# The ideal candidate is a final-year B.Tech student (Class of 2026) with 
# hands-on experience building production-ready AI applications using LLMs, 
# RAG pipelines, and full-stack Python frameworks. You will work on real-world 
# chatbot systems, document intelligence tools, and AI-integrated web apps.

# 1. Key Responsibilities
#    - Build and deploy LLM-powered applications using LangChain and OpenAI APIs
#    - Develop multi-agent RAG systems with vector databases (FAISS, Pinecone, pgvector)
#    - Integrate AI backends with web frameworks (Django / Flask)
#    - Work with local LLMs using tools like Ollama or LM Studio
#    - Build and maintain full-stack AI web applications with REST APIs

# 2. Technical Requirements
#    - Programming: Python (core), SQL, HTML/CSS, JavaScript (basic)
#    - Generative AI: LangChain, RAG pipelines, LLM integration, Embeddings
#    - Vector Databases: FAISS, pgvector, or Pinecone
#    - Web Frameworks: Django or Flask
#    - Tools: Git/GitHub, VS Code, Google Colab
#    - Bonus: MCP server, multi-agent systems, Computer Vision (OpenCV)

# 3. Education & Background
#    - B.Tech in Computer Science / AI / ML (graduating 2026)
#    - Minimum CGPA: 8.0
#    - Prior internship experience in AI/ML development preferred
#    - Strong project portfolio demonstrating end-to-end AI application development

# 4. Soft Skills
#    - Ability to work independently and in team settings
#    - Strong problem-solving mindset
#    - Eagerness to learn and adapt to new AI tools quickly
# """,
#                                    "chat_history": []})

# print(response['output'][0]['text'])