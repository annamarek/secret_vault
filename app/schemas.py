from pydantic import BaseModel, EmailStr


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class SecretCreate(BaseModel):
    title: str
    content: str


class SecretUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class SecretResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str