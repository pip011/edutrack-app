from pydantic import BaseModel

from ..enums import UserRole

class LoginRequest(BaseModel):
    username: str
    password: str
    
class LoginResponse(BaseModel):
    access_token: str
    username: str
    role: UserRole
    token_type: str = "bearer"
    message: str = "Авторизация прошла успешно."
    
class UserInfo(BaseModel):
    user_id: str
    username: str
    role: str