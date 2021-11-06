from user.repos import user_repo


async def get_user_by_email(email: str):
    return await user_repo._filter(email=email)


async def get_user(id: str):
    return await user_repo.get(id=id)


async def count_users(email: str = None):
    await user_repo.count(email=email)


async def create_user(first_name: str, last_name: str, email: str, is_active: bool):
    pass


async def update_user(
    first_name: str, last_name: str, email: str, client_id: int, is_active: bool
):
    pass
