from sqlalchemy import String,Integer
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.core.database import Base
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String)  

    resumes = relationship("Resume", back_populates="owner")