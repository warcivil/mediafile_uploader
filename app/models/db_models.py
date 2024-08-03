from datetime import datetime

from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.orm import relationship

Base = declarative_base()

class MediaFile(Base):
    __tablename__ = 'media_file'
    id = Column(BigInteger, primary_key=True)
    uid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    file_path = Column(String)
    link_on_cloud = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    metadata_id = Column(BigInteger, ForeignKey('metadata_media_file.id'))
    metadata_media_file = relationship("MetadataMediaFile")


class MetadataMediaFile(Base):
    __tablename__ = 'metadata_media_file'
    id = Column(BigInteger, primary_key=True)
    file_size = Column(BigInteger)  # Размер файла в байтах
    file_format = Column(String)  # Формат файла (например, "mp3", "wav")
    original_name = Column(String)  # Оригинальное название файла
    file_extension = Column(String)  # Расширение файла (например, ".mp3", ".wav")