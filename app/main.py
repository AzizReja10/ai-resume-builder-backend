from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.auth.router import router as auth_router
from app.auth import models as auth_models
from app.resumes import models as resume_models
from app.resumes.router import router as resumes_router


app = FastAPI(title="AI Resume Builder")


# CORS
origins = [
    "http://localhost:5173",
    "https://ai-resume-builder-frontend-sigma.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(resumes_router)
app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    return {"status": "ok"}