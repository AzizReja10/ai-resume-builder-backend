from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.auth.models import User
from app.auth.router import get_current_user
from app.resumes.models import Resume
from app.resumes.schemas import ResumeCreate,ResumeOut,ResumeUpdate
import json
import os
import tempfile
from app.ai.github import fetch_github_profile_languages
from app.ai.prompts import build_skills_from_languages_prompt
from app.resumes.schemas import GithubProfileRequest, SkillsSyncResponse
from app.ai.github import fetch_github_repo_data
from app.ai.prompts import build_project_from_github_prompt
from app.resumes.schemas import GithubProjectRequest, GeneratedProject
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool
from app.export.pdf import build_resume_pdf
from pydantic import ValidationError
from app.ai.client import generate_json
from app.ai.prompts import build_bullet_optimize_prompt
from app.resumes.schemas import BulletOptimizeRequest,BulletOptimizeResponse
router=APIRouter(prefix="/resumes",tags=["resumes"])
@router.post("/",response_model=ResumeOut)
async def create_resume(data:ResumeCreate,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    resume=Resume(owner_id=current_user.id,title=data.title)
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    return resume
@router.get("/",response_model=list[ResumeOut])
async def list_resume(
    current_user:User=Depends(get_current_user),
    db:AsyncSession=Depends(get_db)):
        result=await db.execute(select(Resume).where(Resume.owner_id==current_user.id))
        return result.scalars().all()
@router.get("/{resume_id}",response_model=ResumeOut)
async def get_resume(
      resume_id:int,
      current_user:User=Depends(get_current_user),
      db:AsyncSession=Depends(get_db)):
        result=await db.execute(select(Resume).where(Resume.id==resume_id))
        resume=result.scalar_one_or_none()
        if not resume or resume.owner_id!=current_user.id:
                raise  HTTPException(status_code=404,detail="Resume not found")
        return resume
@router.patch("/{resume_id}",response_model=ResumeOut)
async def update_resume(resume_id:int,data:ResumeUpdate,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
      result=await db.execute(select(Resume).where(Resume.id==resume_id))
      resume=result.scalar_one_or_none()
      if not resume or resume.owner_id!=current_user.id:
            raise HTTPException(status_code=404,detail="Resume not found")
      for field,value in data.model_dump(exclude_unset=True).items():
            setattr(resume,field,value)
      await db.commit()
      await db.refresh(resume)
      return resume

@router.post("/{resume_id}/optimize-bullet",response_model=BulletOptimizeResponse)
async def optimize_bullet(resume_id:int,data:BulletOptimizeRequest,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
      result=await db.execute(select(Resume).where(Resume.id==resume_id))
      resume=result.scalar_one_or_none()
      if not resume or resume.owner_id!=current_user.id:
             raise HTTPException(status_code=404,detail="Resume not found")
      system_prompt,user_prompt=build_bullet_optimize_prompt(data.raw_bullet,data.job_description)
      try:
        raw_output = generate_json(system_prompt, user_prompt)
        parsed = json.loads(raw_output)
        validated = BulletOptimizeResponse(**parsed)
      except (json.JSONDecodeError, ValidationError) as e:
            raise HTTPException(status_code=502, detail=f"AI response was malformed: {e}")
      return validated
@router.get("/{resume_id}/export-pdf")
async def export_resume_pdf(resume_id:int,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
      result=await db.execute(select(Resume).where(Resume.id==resume_id))
      resume=result.scalar_one_or_none()
      if not resume or resume.owner_id!=current_user.id:
            raise HTTPException(status_code=404,detail="Resume not found")
      output_path = os.path.join(tempfile.gettempdir(), f"resume_{resume_id}.pdf")

      await run_in_threadpool(
         build_resume_pdf,
    output_path,
    resume.personal_info,
    resume.education,
    resume.experience,
    resume.projects,
    resume.skills,
    resume.extracurricular,
    )
      return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=f"{resume.title.replace(' ', '_')}.pdf",
    )
@router.post("/{resume_id}/generate-project-from-github",response_model=GeneratedProject)
async def generate_project_from_github(resume_id:int,data:GithubProjectRequest,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
      result=await db.execute(select(Resume).where(Resume.id==resume_id))
      resume=result.scalar_one_or_none()
      if not resume or resume.owner_id!=current_user.id:
            raise HTTPException(status_code=404,detail="resume not found")
      try:
            repo_data=fetch_github_repo_data(data.github_url)
      except ValueError as e:
            raise HTTPException(status_code=404,detail=str(e))
      system_prompt,user_prompt=build_project_from_github_prompt(repo_data)
      try:
            raw_output=generate_json(system_prompt,user_prompt)
            parsed=json.loads(raw_output)
            validated=GeneratedProject(**parsed)
      except(json.JSONDecodeError,ValidationError) as e:
            raise HTTPException(status_code=502, detail=f"AI response was malformed: {e}")
      return validated
@router.delete("/{resume_id}",status_code=204)
async def delete_resume(resume_id:int,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
      result=await db.execute(select(Resume).where(Resume.id==resume_id))
      resume=result.scalar_one_or_none()
      if not resume or resume.owner_id!=current_user.id:
            raise HTTPException(status_code=404,details="resume not found")
      await db.delete(resume)
      await db.commit()

@router.post("/{resume_id}/sync-skills-from-github-profile",response_model=SkillsSyncResponse)
async def sync_skills_from_github_profile(resume_id:int,data:GithubProfileRequest,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
      result=await db.execute(select(Resume).where(Resume.id==resume_id))
      resume=result.scalar_one_or_none()
      if not resume or resume.owner_id!=current_user.id:
            raise HTTPException(status_code=404,detail="Resume not found")
      try:
            languages=fetch_github_profile_languages(data.github_url)
      except ValueError as e:
            raise HTTPException(status_code=400,detail=str(e))
      if not languages:
            return SkillsSyncResponse(skills=[])
      system_prompt,user_prompt=build_skills_from_languages_prompt(languages)
      try:
            raw_output=generate_json(system_prompt,user_prompt)
            parsed=json.loads(raw_output)
            validated=SkillsSyncResponse(**parsed)
      except(json.JSONDecodeError,ValidationError) as e:
            raise HTTPException(status_code=502, detail=f"AI response was malformed: {e}")
      return validated