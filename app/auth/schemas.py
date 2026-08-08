from pydantic import BaseModel,EmailStr
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    full_name:str
class UserOut(BaseModel):
    email:EmailStr
    full_name:str
    class Config:
        from_attributes=True
class Token(BaseModel):
    access_token:str
    token_type:str="bearer"
class TokenData(BaseModel):
    user_id:int|None=None
class UserLogin(BaseModel):
    email:EmailStr
    password:str