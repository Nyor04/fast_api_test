from fastapi import APIRouter
from fastapi import Depends, HTTPException
from pydantic import BaseModel, field_validator
import re

from routers.auth import JWTBearer

users_router = APIRouter()

email_format = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
user_list = [
    {    
        "id": 1,
        "username": "burena",
        "email": "test@dev.com",
        "is_active": True,
        "address": [
            {
            "city": "si",
            "state": "alli",
            "country": "nunca jamas"
            }
        ],
        "roles": [
            "user"
        ]
    }
    
]

class Address(BaseModel):
    city:str
    state:str
    country:str

class UpdateRoleAtrribute(BaseModel):
    roles:list[str]

class User(BaseModel):
    id:int
    username:str
    email:str = 'test@dev.com'
    is_active:bool = True
    address:list[Address]
    roles:list

  

    @field_validator("email")
    def email_validator(cls, value): 
        if not isinstance(value, str):  
            raise ValueError("Email must be a string.")
        if not re.match(email_format, value):
            raise ValueError("Invalid email format.")
        return value
    
    @field_validator('roles')
    def roles_validator(cls,value):
        if not value:
            raise ValueError("User must have at least 1 rol assigned.")
        return value


@users_router.get("/users", tags=['Users'], dependencies=[Depends(JWTBearer())])
def get_users():
    return user_list

@users_router.get("/users/{id}", tags=['Users'])
def get_users(id:int):
    return user_list[id]

@users_router.post("/users", tags=['Users'])
def create_users(user:User):
    if any(product.id == user.id for product in user_list):
        return {'message':f"User id must be unique!, id {user.id} already in use"}
    user_list.append(user)
    return {'message':'User added', 'user_object':user_list}

@users_router.put("/users/{id}", tags=['Users'])
def update_users(id:int, user:User):
    user_index = next((index for index, value in enumerate(user_list) if value.id == id))
    if user_index == None:
        raise HTTPException(status_code=404, detail="User Does Not Exist")
    else:
        user_list[user_index] = user
        return {'message':'user updated', 'user_object':user_list[user_index]}

@users_router.patch("/users/{id}/roles", tags=['Users'],description="este endopoint acutaliza el atributo roles de los objetos usuarios.")
def update_users_role(id:int, roles:UpdateRoleAtrribute ):
    user_index = next((index for index, value in enumerate(user_list) if value['id'] == id))
    if user_index == None:
        raise HTTPException(status_code=404, detail="User Does Not Exist")
    else:
        user_list[user_index]['roles']=roles.roles
        return {'message':"Roles attribute updated", "updated_object":user_list[user_index]}
    
