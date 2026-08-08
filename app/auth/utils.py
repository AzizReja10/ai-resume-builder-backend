from datetime import datetime,timedelta,timezone
import jwt
from app.core.config import settings
from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)
def verify_password(password:str,hashed_password:str)->bool:
    return pwd_context.verify(password,hashed_password)
def create_access_token(user_id:int)->str:
    expire =datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    to_encode={"sub":str(user_id),"exp":expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
def decode_access_token(token:str)->int|None:
    try:
        payload=jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        return int(payload.get("sub"))
    except jwt.PyJWTError:
        return None