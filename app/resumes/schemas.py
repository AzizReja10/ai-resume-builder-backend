from pydantic import BaseModel
from typing import Any
class ResumeCreate(BaseModel):
    title:str="Untitled Resume"
class ResumeOut(BaseModel):
    id:int
    title:str
    personal_info:dict
    education:list
    experience:list
    projects:list
    skills:list
    extracurricular:list
    class Config:
        from_attributes=True
class ResumeUpdate(BaseModel):
    title:str|None=None
    personal_info:dict|None=None
    education:list|None=None
    experience:list|None=None
    projects:list|None=None
    skills:list|None=None
    extracurricular:list
class BulletOptimizeRequest(BaseModel):
    raw_bullet:str
    job_description:str|None=None
class BulletOptimizeResponse(BaseModel):
    rewritten:str
class GithubProjectRequest(BaseModel):
    github_url:str
class GeneratedProject(BaseModel):
    name:str
    tags:str
    bullets:list[str]
    skills:list[SkillGroup]
class SkillGroup(BaseModel):
    category:str
    items:list[str]
class GithubProfileRequest(BaseModel):
    github_url:str
class SkillsSyncResponse(BaseModel):
    skills:list[SkillGroup]
class ExtractedLink(BaseModel):
    label:str
    url:str
class ExtractedEducation(BaseModel):
    institution:str
    degree:str=""
    details:str=""
    dates:str=""
class GeneratedProject(BaseModel):
    name:str
    tags:str
    bullets:list[str]
    skills:list[SkillGroup]
    profile_links:list[ExtractedLink]=[]
    education:list[ExtractedEducation]=[]
class SectionFeedback(BaseModel):
    section:str
    feedback:str
class ResumeAnalysisResponse(BaseModel):
    score:int
    summary:str
    strengths:list[str]
    improvements:list[str]
    section_feedback:list[SectionFeedback]
class ResumeExportRequest(BaseModel):
    title: str = "Resume"
    personal_info: dict = {}
    education: list = []
    experience: list = []
    projects: list = []
    skills: list = []
    extracurricular: list = []