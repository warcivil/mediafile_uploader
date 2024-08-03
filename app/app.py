import traceback

from fastapi import FastAPI, UploadFile, File, HTTPException
from http_constants import status
from starlette.responses import FileResponse

from app.config import get_logger
from app.voice_async_api.save_on_local import SaveOnLocal
from app.voice_async_api.save_to_db import FileSaver
from app.voice_async_api.upload_on_cloud import UploadOnYandexCloud

app = FastAPI()
logger = get_logger(__name__)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    async_db = FileSaver()
    save_on_local = SaveOnLocal()
    save_on_ya_cloud = UploadOnYandexCloud()
    try:
        path_to_file = await save_on_local.save(file)
        link = await save_on_ya_cloud.upload_to_ya_cloud(path_to_file)
        await async_db.save_file(file, path_to_file, link)
    except Exception as exc:
        logger.error(f'error: {traceback.print_exc()}')
        raise HTTPException(status_code=status.INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return {"status": status.OK}


@app.post("/uploadfile_streaming/")
async def create_upload_file_streaming(file: UploadFile = File(...)):
    async_db = FileSaver()
    save_on_local = SaveOnLocal()
    save_on_ya_cloud = UploadOnYandexCloud()
    try:
        path_to_file = await save_on_local.streaming_save(file)
        link = await save_on_ya_cloud.upload_to_ya_cloud(path_to_file)
        await async_db.save_file(file, path_to_file, link)
    except:
        logger.error(f'error: {traceback.print_exc()}')
        raise HTTPException(status_code=status.INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return {'status': status.OK}


@app.get("/files/{file_uid}")
async def download_file(file_uid: str):
    async_db = FileSaver()
    file_path = await async_db.get_file(file_uid)
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_uid)