from sqlalchemy import Integer,String,ForeignKey,JSON
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.core.database import Base

class Resume(Base):
    __tablename__="resumes"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    owner_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    title:Mapped[str]=mapped_column(String,default="Untitiled Resume")
    personal_info:Mapped[dict]=mapped_column(JSON,default=dict)
    education:Mapped[dict]=mapped_column(JSON,default=list)
    experience:Mapped[list]=mapped_column(JSON,default=list)
    projects:Mapped[list]=mapped_column(JSON,default=list)
    skills:Mapped[list]=mapped_column(JSON,default=list)
    owner=relationship("User",back_populates="resumes")
    extracurricular:Mapped[list]=mapped_column(JSON,default=list)