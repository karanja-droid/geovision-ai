from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer(auto_error=False)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
    if credentials is None:
        return "demo-user"
    if credentials.credentials != "demo-token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid demo token")
    return "demo-user"