from common.int_choice import IntChoice
from parcel.models import PTBaseModel


class UserStatusEnum(IntChoice):
    ACTIVE= 1
    IN_ACTIVE= 2


class User(PTBaseModel):
    id: int
    email: str
    first_name: str
    status: UserStatusEnum
