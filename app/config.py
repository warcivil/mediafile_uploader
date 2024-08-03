import logging
from decouple import AutoConfig
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine

config = AutoConfig()
logging.basicConfig(level=logging.INFO)


def get_logger(name):
    logger = logging.getLogger(name)
    fh = logging.FileHandler(FILE_HANDLER_PATH)
    formatter = logging.Formatter('%(asctime)s - detail_api - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


class DBCredentials(BaseSettings):
    DB_USER: str = config('DB_USER')
    DB_PASSWORD: str = config('DB_PASSWORD')
    DB_NAME: str = config('DB_NAME')
    DB_PORT: str = config("DB_PORT", cast=str)

    def get_db_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@localhost:{self.DB_PORT}/{self.DB_NAME}"

    def get_async_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@localhost:{self.DB_PORT}/{self.DB_NAME}"


class Settings(BaseSettings):
    SERVER_HOST: str = config('SERVER_HOST')
    SERVER_PORT: int = config('SERVER_PORT', cast=int)
    DEBUG: bool = config("DEBUG", cast=bool)


db_credentials = DBCredentials()
async_engine = create_async_engine(db_credentials.get_async_db_url())

FILE_HANDLER_PATH = config('FILE_HANDLER_PATH')
PATH_TO_FILE = config('PATH_TO_FILE')
YANDEX_DISK_CLIENT_ID = config('YANDEX_DISK_CLIENT_ID')
YANDEX_DISK_CLIENT_SECRET = config('YANDEX_DISK_CLIENT_SECRET')
YANDEX_DISK_TOKEN=config('YANDEX_DISK_TOKEN')