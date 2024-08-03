import os
import uvicorn

from app.config import Settings

settings = Settings()

num_cores = os.cpu_count()

uvicorn.run(
    'app.app:app',
    host=settings.SERVER_HOST,
    port=settings.SERVER_PORT,
    reload=True if settings.DEBUG else False,
    workers=1 if settings.DEBUG else num_cores + 1,
)
