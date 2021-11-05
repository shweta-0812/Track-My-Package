from pydantic.main import BaseModel


class Success(BaseModel):
    success: bool = True
    msg: str