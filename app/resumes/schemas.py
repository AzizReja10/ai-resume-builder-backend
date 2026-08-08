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