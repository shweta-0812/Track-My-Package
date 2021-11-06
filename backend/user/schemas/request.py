from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    first_name: str
    last_name: str


class UpdateUser(BaseModel):
    first_name: str = None
    last_name: str = None
