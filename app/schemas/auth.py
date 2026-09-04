from pydantic import (BaseModel, EmailStr, Field)

class SignupRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    
class SignupResponse(BaseModel):
    id: int
    name: str
    email: str

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)

class LoginResponse(BaseModel):
    id: int
    name: str
    email: str
    access_token: str
    refresh_token: str
    token_type: str

