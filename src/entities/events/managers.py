import uuid
from datetime import datetime
from pathlib import Path
from typing import Protocol

from fastapi import UploadFile

type StorageFileName = str
type RelativePath = str
type ContentLength = int


class IDetectionImageManager(Protocol):
    async def save_image(
        self,
        image_data: bytes,
        original_filename: str | None = None,
    ) -> str: ...

    async def save_upload_file(
        self,
        file: UploadFile,
    ) -> tuple[StorageFileName, ContentLength]: ...

    def delete_image(
        self,
        relative_path: str,
    ) -> bool: ...


class DetectionImageManager(IDetectionImageManager):
    def __init__(
        self,
    ):
        self.static_dir = Path(
            # ! Move to settings via .env
            "static/images",
        )

        self.static_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def save_image(
        self,
        image_data: bytes,
        original_filename: str | None = None,
    ) -> str:
        extension = Path(original_filename).suffix if original_filename else ".jpg"
        storage_filename = f"{uuid.uuid4().hex}{extension}"

        date_subdir = datetime.now().strftime("%Y_%m_%d")
        save_dir = self.static_dir / date_subdir
        save_dir.mkdir(parents=True, exist_ok=True)

        file_path = save_dir / storage_filename

        with file_path.open(mode="wb") as f:
            f.write(image_data)

        return storage_filename

    async def save_upload_file(
        self,
        file: UploadFile,
    ) -> tuple[StorageFileName, ContentLength]:
        content = await file.read()
        storage_filename = await self.save_image(
            image_data=content,
            original_filename=file.filename,
        )

        return storage_filename, len(content)

    def delete_image(
        self,
        relative_path: str,
    ) -> bool:
        try:
            full_path = self.static_dir.parent / relative_path.lstrip("/")

            if full_path.exists():
                full_path.unlink()

                return True
        except Exception as e:
            print(f"Error deleting image: {e}")

        return False
