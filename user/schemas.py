from pydantic import BaseModel, field_validator
from typing import Optional
from settings import settings
import re
class RegisterSerializer(BaseModel):
    username: str
    password: str
    email: str
    superkey: Optional[str] = False

    @field_validator('superkey')
    @classmethod
    def validate_superkey(cls, value):
        if value == '':
            return False
        if value != settings.superkey:
            raise ValueError('Invalid superkey')
        return True
    
    @field_validator('password')
    @classmethod
    def validate_password(cls,value):
        password_pattern="[A-Za-z0-9@#$%^&+=]{8,}"
        if re.match(password_pattern,value):
            return value
        raise ValueError("password must contain one uppercase, one special character, one Number ")