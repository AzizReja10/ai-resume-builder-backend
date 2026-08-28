from sqlalchemy import Integer,String,JSON
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base

class Resume(Base):
    __tablename__="resumes"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    title:Mapped[str]=mapped_column(String,default="Untitiled Resume")
    personal_info:Mapped[dict]=mapped_column(JSON,default=dict)
    education:Mapped[dict]=mapped_column(JSON,default=list)
    experience:Mapped[list]=mapped_column(JSON,default=list)
    projects:Mapped[list]=mapped_column(JSON,default=list)
    skills:Mapped[list]=mapped_column(JSON,default=list)
    extracurricular:Mapped[list]=mapped_column(JSON,default=list)
    session_id: Mapped[str] = mapped_column(String, index=True)