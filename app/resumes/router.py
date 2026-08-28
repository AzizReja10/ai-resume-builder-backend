import os
import json
import tempfile
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool
from pydantic import ValidationError
from app.resumes.schemas import ResumeExportRequest
from app.core.database import get_db
from app.core.session import get_session_id
from app.resumes.models import Resume
from app.resumes.schemas import (
    ResumeCreate, ResumeOut, ResumeUpdate,
    BulletOptimizeRequest, BulletOptimizeResponse,
    GithubProjectRequest, GeneratedProject,
    GithubProfileRequest, SkillsSyncResponse,
)
from app.ai.client import generate_json
from app.ai.prompts import build_bullet_optimize_prompt, build_project_from_github_prompt, build_skills_from_languages_prompt
from app.ai.github import fetch_github_repo_data, fetch_github_profile_languages
from app.export.pdf import build_resume_pdf

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/", response_model=ResumeOut)
async def create_resume(
    data: ResumeCreate,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    resume = Resume(session_id=session_id, title=data.title)
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    return resume


@router.get("/", response_model=list[ResumeOut])
async def list_resumes(
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.session_id == session_id))
    return result.scalars().all()


@router.get("/{resume_id}", response_model=ResumeOut)
async def get_resume(
    resume_id: int,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume or resume.session_id != session_id:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.patch("/{resume_id}", response_model=ResumeOut)
async def update_resume(
    resume_id: int,
    data: ResumeUpdate,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume or resume.session_id != session_id:
        raise HTTPException(status_code=404, detail="Resume not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(resume, field, value)

    await db.commit()
    await db.refresh(resume)
    return resume


@router.delete("/{resume_id}", status_code=204)
async def delete_resume(
    resume_id: int,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume or resume.session_id != session_id:
        raise HTTPException(status_code=404, detail="Resume not found")

    await db.delete(resume)
    await db.commit()


@router.post("/{resume_id}/optimize-bullet", response_model=BulletOptimizeResponse)
async def optimize_bullet(
    resume_id: int,
    data: BulletOptimizeRequest,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume or resume.session_id != session_id:
        raise HTTPException(status_code=404, detail="Resume not found")

    system_prompt, user_prompt = build_bullet_optimize_prompt(data.raw_bullet, data.job_description)

    try:
        raw_output = generate_json(system_prompt, user_prompt)
        parsed = json.loads(raw_output)
        validated = BulletOptimizeResponse(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=502, detail=f"AI response was malformed: {e}")

    return validated


@router.post("/{resume_id}/generate-project-from-github", response_model=GeneratedProject)
async def generate_project_from_github(
    resume_id: int,
    data: GithubProjectRequest,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume or resume.session_id != session_id:
        raise HTTPException(status_code=404, detail="Resume not found")

    try:
        repo_data = fetch_github_repo_data(data.github_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    system_prompt, user_prompt = build_project_from_github_prompt(repo_data)

    try:
        raw_output = generate_json(system_prompt, user_prompt)
        parsed = json.loads(raw_output)
        validated = GeneratedProject(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=502, detail=f"AI response was malformed: {e}")

    return validated


@router.post("/{resume_id}/sync-skills-from-github-profile", response_model=SkillsSyncResponse)
async def sync_skills_from_github_profile(
    resume_id: int,
    data: GithubProfileRequest,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume or resume.session_id != session_id:
        raise HTTPException(status_code=404, detail="Resume not found")

    try:
        languages = fetch_github_profile_languages(data.github_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not languages:
        return SkillsSyncResponse(skills=[])

    system_prompt, user_prompt = build_skills_from_languages_prompt(languages)
    try:
        raw_output = generate_json(system_prompt, user_prompt)
        parsed = json.loads(raw_output)
        validated = SkillsSyncResponse(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=502, detail=f"AI response was malformed: {e}")

    return validated


@router.get("/{resume_id}/export-pdf")
async def export_resume_pdf(
    resume_id: int,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume or resume.session_id != session_id:
        raise HTTPException(status_code=404, detail="Resume not found")

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
@router.post("/export-pdf-preview")
async def export_pdf_preview(data: ResumeExportRequest):
    output_path = os.path.join(tempfile.gettempdir(), "resume_preview.pdf")

    await run_in_threadpool(
        build_resume_pdf,
        output_path,
        data.personal_info,
        data.education,
        data.experience,
        data.projects,
        data.skills,
        data.extracurricular,
    )

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=f"{data.title.replace(' ', '_')}.pdf",
    )