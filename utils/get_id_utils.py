from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from config.settings import app_config
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user_id(token: str = Depends(security)) -> str:
    try:
        payload = jwt.decode(token.credentials, app_config["SECRET_KEY"], algorithms=app_config["ALGORITHM"])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: user_id not found")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
