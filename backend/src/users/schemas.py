from pydantic import BaseModel

class UserAuthSchema(BaseModel):
    username: str
    password: str

class UserSchema(BaseModel):
    username: str