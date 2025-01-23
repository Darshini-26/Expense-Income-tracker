from pydantic import BaseModel
 
class User_auth_create(BaseModel):
    username: str
    password: str
 
class User_auth_out(BaseModel):
    id: int
    username: str
 
    class Config:
        from_attributes = True
 