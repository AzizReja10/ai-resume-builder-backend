from fastapi import Header,HTTPException

async def get_session_id(x_session_id:str|None=Header(default=None,alias="X-Session-Id"))->str:
    if not x_session_id or not x_session_id.strip():
        raise HTTPException(status_code=404,detail="error")
    return x_session_id.strip()