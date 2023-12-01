import logging
import uvicorn
from aiogram import types
from fastapi import FastAPI
from utils.config import config
from middlewares.spam_filter import on_pre_process

from bot import bot, dp


WEBHOOK_PATH = f"/bot/{config.tg.token}"
WEBHOOK_URL = config.server.url + WEBHOOK_PATH


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)

app = FastAPI()


dp.update.outer_middleware(on_pre_process)


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
    logger.info("App started")


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    try:
        await dp.feed_update(bot, telegram_update)
    except Exception as e:
        print(e)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    logger.info("App stopped")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.server.port)
