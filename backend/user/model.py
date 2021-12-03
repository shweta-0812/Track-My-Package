from common.base_model import PTBaseModel

USER_MODEL = "user"

USER_ES_INDEX_DOC_MAPPINGS = {
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "text"},
        "first_name": {"type": "text"},
        "last_name": {"type": "text"},
        "status": {"type": "integer"},
        "date": {"type": "integer"},
        "created_at": {"type": "integer"},
        "updated_at": {"type": "integer"},
    }
}

class UserModel(PTBaseModel):
    id: int
    email: str
    first_name: str
