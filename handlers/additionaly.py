from utils.db.users import get_user_db


async def get_user(state, user_id):
    data = await state.get_data()
    user = data.get('user')
    if user is None:
        user = get_user_db(user_id)
        await state.update_data(user=user)
    return user
