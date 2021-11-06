from typing import Optional

from pydantic import BaseModel

from common.int_choice import IntChoice


class PTBaseModelStatusEnum(IntChoice):
    ACTIVE= 1
    IN_ACTIVE= 2


class PTBaseModel(BaseModel):
    created_at: int
    updated_at: Optional[int]
    status: PTBaseModelStatusEnum
