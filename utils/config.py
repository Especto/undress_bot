from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class Server:
    url: str
    port: int


@dataclass
class Config:
    tg: TgBot
    server: Server
    undress: str


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID')
        ),
        server=Server(
            url=env.str('URL'),
            port=env.int('PORT')
        ),
        undress=env.str('UNDRESS_TOKEN')
    )


config = load_config('.env')
