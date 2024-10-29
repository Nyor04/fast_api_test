from fastapi import APIRouter

from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from middlewares.jwt_manager import jwt_generator, jwt_validator
from pydantic import BaseModel, field_validator
import re #regular expresions gods.

auth_router = APIRouter()

email_format = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class LoginData(BaseModel):
    email:str
    password:str

    @field_validator("email")
    def email_validator(cls, value): 
        if not isinstance(value, str):  
            raise ValueError("Email must be a string.")
        if not re.match(email_format, value):
            raise ValueError("Invalid email format.")
        return value

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) :
        auth = await super().__call__(request)
        data = jwt_validator(auth.credentials)
        if data['email'] != "mock@email.com" or data["password"] != "mockpassword":
            raise HTTPException(status_code=401,detail="Credenciales invalidas")

@auth_router.post("/login", tags=['Auth'])
def login(user:LoginData):
    if user.email == "mock@email.com" and user.password == "mockpassword":
        token:str = jwt_generator(user.model_dump())
        return JSONResponse(content=token, status_code=200)
    else:
        message = {"message":"Auth failed, check your credentials"}
        return JSONResponse(content=message)