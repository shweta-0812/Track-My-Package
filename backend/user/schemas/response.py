from pydantic import BaseModel

from common.base_model import PTBaseModelStatusEnum


class UserInDB(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    status: PTBaseModelStatusEnum
    created_at: int
    updated_at: int
    date: int