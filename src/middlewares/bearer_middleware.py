from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.repository.user import User

class BearerTokenAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=404, detail="Invalid or missing token")

        token = credentials.credentials
        if not User.is_user(token):
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return token