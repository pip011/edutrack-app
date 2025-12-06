from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.user_schema import UserCreate, UserResponse
from backend.schemas.authorization_schema import LoginRequest, LoginResponse, UserInfo
from backend.services.users_service import UserService
from backend.services.authorization_service import AuthorizationService
from ...database.db import get_session


router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        new_user = await UserService.register_user(session, user)
        await session.commit()
        return UserResponse.model_validate(new_user)
    except ValueError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail='Пользователь с таким именем уже зарегистрирован')
    except Exception:
        await session.rollback()
        raise
    

@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, response: Response, session: AsyncSession = Depends(get_session)):
    access_token = await AuthorizationService.login(login_request.username, login_request.password, session)
    
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный юзернейм или пароль"
        )
        
    response.set_cookie(
        key='access_token',
        value=access_token, 
        httponly=False,
        max_age=60*60*24,
        domain="127.0.0.1",
        samesite='lax',
        secure=False
    )
    
        
    return LoginResponse(
        access_token=access_token, 
        username=login_request.username, 
        role=AuthorizationService.get_current_user_role(access_token=access_token)
    )
    

@router.get("/me", response_model=UserInfo)
async def verify_auth(user: dict = Depends(AuthorizationService.get_current_user)):
    return UserInfo(**user)


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",    
        httponly=False,
        domain="127.0.0.1",
        samesite="lax",
        secure=False
    )
    return {'ok': True}