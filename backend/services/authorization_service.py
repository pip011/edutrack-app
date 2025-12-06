import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

import bcrypt
import jwt
from fastapi import Cookie, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from ..repositories.user_repository import UserRepository
from ..database.models.user_model import User
from ..enums import UserRole


blacklisted_tokens: dict[str, datetime] = {}

security = HTTPBearer()


class AuthorizationService:
    @staticmethod
    def _get_jwt_secret_key() -> str:
        return settings.JWT_SECRET_KEY
    
    @staticmethod
    def _verify_password(password, password_hash):
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash)
        
    @staticmethod
    def _validate_credentials(username: str, password: str, session: AsyncSession):
        user: User = UserRepository.find_user_by_username(username, session)
        
        if not user:
            return False
        
        return AuthorizationService._verify_password(password, user.password_hash)
    
    @staticmethod
    def _create_jwt_token(user_id: str, role: str, username: str, expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=360)

        payload = {
            "sub": user_id,
            "role": role,
            "username": username,
            "exp": int(expire.timestamp()),    
            "iat": int(datetime.now(timezone.utc).timestamp()),  
            "jti": secrets.token_urlsafe(16)    
        }

        return jwt.encode(payload, AuthorizationService._get_jwt_secret_key(), algorithm="HS256")
    
    @staticmethod
    def _decode_jwt_token(token: str) -> dict:
        try:
            if token in blacklisted_tokens:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Токен был отозван"
                )
                
            payload = jwt.decode(token, AuthorizationService._get_jwt_secret_key(), algorithms=["HS256"])
            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Срок токена истек"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный токен"
            )
            
    @staticmethod
    def get_current_user_id(access_token: str = Cookie(None)) -> int:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided"
            )
        
        payload = AuthorizationService._decode_jwt_token(access_token)
        user_id = payload.get('sub')
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return int(user_id)
    
    @staticmethod
    def get_current_user_role(access_token: str = Cookie(None)) -> str:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided"
            )
        
        payload = AuthorizationService._decode_jwt_token(access_token)
        user_role = payload.get('role')
        
        if user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return user_role
    
    @staticmethod
    def get_current_user(access_token: str = Cookie(None)) -> dict:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided"
            )
        
        payload = AuthorizationService._decode_jwt_token(access_token)
        user_role = payload.get('role')
        username = payload.get('username')
        user_id = payload.get('sub')
        
        if user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return {'user_id': user_id, 'username': username, 'role': user_role}
    
    @staticmethod
    def _blacklist_token(token: str) -> None:
        try:
            payload = jwt.decode(token, AuthorizationService._get_jwt_secret_key(), algorithms=["HS256"])
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                blacklisted_tokens[token] = exp_datetime

                AuthorizationService._cleanup_expired_blacklisted_tokens()
        except jwt.InvalidTokenError:
            pass
        
    @staticmethod
    def _cleanup_expired_blacklisted_tokens() -> None:
        current_time = datetime.now(timezone.utc)
        expired_tokens = [
            token for token, exp_time in blacklisted_tokens.items()
            if exp_time < current_time
        ]

        for token in expired_tokens:
            del blacklisted_tokens[token]
    
    @staticmethod 
    def require_role(*allowed_roles: UserRole) -> function:
        def role_checker(user = Depends(AuthorizationService.get_current_user)) -> dict:
            if user["role"] not in [role.value for role in allowed_roles]:
                raise HTTPException(
                    status_code=403,
                    detail=f"Access denied for role '{user['role']}'"
                )
            return user
        return role_checker
    
    @staticmethod
    async def login(username: str, password: str, session: AsyncSession) -> str | None:
        user: User = await UserRepository.find_user_by_username(username, session)
        if not user: 
            return None
        if not AuthorizationService._verify_password(password, user.password_hash):
            return None
        
        return AuthorizationService._create_jwt_token(user_id=str(user.id), role=user.role, username=username)