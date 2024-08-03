
import yadisk

from app.config import YANDEX_DISK_TOKEN
from app.config import get_logger

logger = get_logger(__name__)

class UploadOnYandexCloud:
    def __init__(self):
        self.token = YANDEX_DISK_TOKEN
        self.client = yadisk.YaDisk(token=self.token)

    async def upload_to_ya_cloud(self, path_to_file):
        try:
            self.client.upload(path_to_file, '/')
            logger.info(f"File '{path_to_file}' uploaded successfully to Yandex.Disk")

            # Получаем ссылку на файл
            file_path_on_disk = '/' + path_to_file.split('/')[-1] # Предполагаем загрузку в корень
            link = self.client.get_download_link(file_path_on_disk)
            logger.info(f"Link for file '{file_path_on_disk}': {link}")
            return link

        except yadisk.exceptions.YaDiskError as e:
            logger.error(f"Error uploading file '{path_to_file}' to Yandex.Disk: {e}")
            return None
