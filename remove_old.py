import asyncio
from datetime import datetime, timedelta

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import async_engine
from app.constants import OLD_FILES
from app.models.db_models import MediaFile


class RemoveOld():
    def __init__(self):
        self.async_engine = async_engine

    async def remove_old_files(self):
        async with AsyncSession(self.async_engine) as session:
            # Вычисляем дату 14 дней назад
            fourteen_days_ago = datetime.utcnow() - timedelta(days=OLD_FILES)

            # Удаляем файлы, созданные ранее 14 дней назад
            stmt = delete(MediaFile).where(MediaFile.created_at < fourteen_days_ago)
            await session.execute(stmt)
            await session.commit()


async def main():
    remove_old = RemoveOld()
    await remove_old.remove_old_files()


asyncio.run(main()) # ну и запустить этот скрипт в кроне 0 12 * * * например.