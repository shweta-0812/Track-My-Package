from common.base_model import PTBaseModel

USER_MODEL = "user"


class User(PTBaseModel):
    id: int
    email: str
    first_name: str
