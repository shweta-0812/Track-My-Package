from typing import Any

from user.model import UserModel
from user.repos import user_repo
from user.schemas.request import CreateUser

get_latest_user = user_repo.get_latest_user


async def get_user_by_email(email: str):
    return await user_repo.get_user_by_email(email=email)


async def get_user(id: str):
    return await user_repo.get(id=id)


async def count_users(email: str = None):
    await user_repo.count(email=email)


async def create_user(create_user: CreateUser):
    new_user_data = dict()
    latest_user = await get_latest_user()
    last_id = 0
    print(latest_user)
    # if latest_user> 0:
    #     last_id = latest_user["hits"]["hits"][0]["_id"]

    # auto generate new id
    new_user_data["id"] = int(last_id) + 1

    new_user_data["email"] = create_user.email
    new_user_data["first_name"] = create_user.first_name
    new_user_data["last_name"] = create_user.last_name

    return await user_repo.create_user(user=UserModel(**new_user_data))


async def update_user(
    current_user: Any, first_name: str, last_name: str, email: str
):
    pass
