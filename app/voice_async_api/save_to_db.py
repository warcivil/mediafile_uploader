import os
import uuid

from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from http_constants import status

from app.config import async_engine
from app.models.db_models import MetadataMediaFile, MediaFile
from app.config import get_logger

logger = get_logger(__name__)

class FileSaver():
    def __init__(self):
        self.async_engine = async_engine

    async def save_file(self, file: UploadFile, path_to_file: str, link: str):
        contents = await file.read()

        # Извлечение информации о файле
        file_name = file.filename
        file_size = len(contents)
        file_format = file.content_type
        original_name, file_extension = os.path.splitext(file_name)

        uid=uuid.uuid4()
        # Сохранение в базу данных
        async with AsyncSession(self.async_engine) as session:
            # Создание объекта MetadataMediaFile
            metadata = MetadataMediaFile(
                file_size=file_size,
                file_format=file_format,
                original_name=original_name,
                file_extension=file_extension
            )
            session.add(metadata)
            await session.commit()

            # Создание объекта MediaFile
            media_file = MediaFile(
                uid=uid,
                file_path=path_to_file,
                link_on_cloud=link,
                metadata_media_file=metadata
            )
            session.add(media_file)
            await session.commit()

        logger.info(f'file {original_name} has been saved with uid = {uid}')
    async def get_file(self, uid) -> str:
        async with AsyncSession(self.async_engine) as session:
            stmt = select(MediaFile).where(MediaFile.uid == uid)
            result = await session.execute(stmt)
            media_file = result.scalar_one_or_none()
            if not media_file:
                raise HTTPException(status_code=status.NOT_FOUND, detail="File not found")
            return media_file.file_path