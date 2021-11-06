from typing import Optional

from pydantic import BaseModel

from common.int_choice import IntChoice
from common.utils import get_current_timestamp


class PTBaseModelStatusEnum(IntChoice):
    ACTIVE= 1
    IN_ACTIVE= 2


class PTBaseModel(BaseModel):
    created_at: int = get_current_timestamp()
    updated_at: Optional[int] = get_current_timestamp()
    status: PTBaseModelStatusEnum = PTBaseModelStatusEnum.ACTIVE
