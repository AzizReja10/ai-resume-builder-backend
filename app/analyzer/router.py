import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import ValidationError
from pypdf import PdfReader
import io

from app.ai.client import generate_json
from app.ai.prompts import build_resume_analysis_prompt
from app.resumes.schemas import ResumeAnalysisResponse

router = APIRouter(prefix="/analyzer", tags=["analyzer"])


@router.post("/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    contents = await file.read()

    try:
        reader = PdfReader(io.BytesIO(contents))
        text_parts = [page.extract_text() or "" for page in reader.pages]
        resume_text = "\n".join(text_parts).strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read this PDF — it may be corrupted or scanned as an image")

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text found in this PDF — if it's a scanned image, text extraction won't work",
        )

    # Cap length to keep prompt size reasonable
    resume_text = resume_text[:8000]

    system_prompt, user_prompt = build_resume_analysis_prompt(resume_text)

    try:
        raw_output = generate_json(system_prompt, user_prompt)
        parsed = json.loads(raw_output)
        validated = ResumeAnalysisResponse(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=502, detail=f"AI response was malformed: {e}")

    return validated