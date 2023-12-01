import asyncio
from datetime import datetime
from bot import bot
from handlers import SystemVariables
from utils.config import config

SPAM_LIST = SystemVariables.SPAM_LIST
USER_MSG = SystemVariables.USER_MSG
BLACK_LIST = SystemVariables.BLACK_LIST
BREAK = SystemVariables.BREAK

ADMIN_ID = config.tg.admin_id


async def on_pre_process(handler, event, data):
    user_id = data['event_from_user'].id

    if BREAK and user_id != ADMIN_ID:
        await bot.send_message(chat_id=user_id, text="Technical maintenance")
        return None
    if (user_id in SPAM_LIST or user_id in BLACK_LIST) and user_id != ADMIN_ID:
        await bot.send_message(chat_id=user_id, text="You're blocked")
        return None

    current_time = datetime.now()
    if user_id in USER_MSG:
        last_time = USER_MSG[user_id][1]
        time_difference = current_time - last_time
        USER_MSG[user_id][1] = current_time
        if time_difference.total_seconds() < 5:
            USER_MSG[user_id][0] += 1
            if USER_MSG[user_id][0] == 5:
                SPAM_LIST.append(user_id)
                await asyncio.sleep(120)
                SPAM_LIST.remove(user_id)
                USER_MSG[user_id][0] = 0
        else:
            USER_MSG[user_id][0] = 0
    else:
        USER_MSG[user_id] = [0, current_time]

    return await handler(event, data)