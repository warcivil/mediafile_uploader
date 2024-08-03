import os
import uuid

import aiofiles
from fastapi import UploadFile

from app.config import PATH_TO_FILE
from app.constants import CHUNK_SIZE


class SaveOnLocal():
    async def save(self, file: UploadFile):
        file_name = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        async with aiofiles.open(PATH_TO_FILE+file_name, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return PATH_TO_FILE+file_name

    async def streaming_save(self, file: UploadFile):
        file_name = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        async with aiofiles.open(PATH_TO_FILE + file_name, 'wb') as out_file:
            while contents := await file.read(CHUNK_SIZE):
                await out_file.write(contents)
        return PATH_TO_FILE + file_name