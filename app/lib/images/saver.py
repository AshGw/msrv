import io
import os
from typing import Optional

from PIL import Image


class ImageSaver:
    is_saved: bool = False

    def __init__(self, raw_bytes: bytes, format: Optional[str] = "jpg"):
        self.raw_bytes = raw_bytes
        self.format = format

    def save(self, output_file_name: str, folder: Optional[str] = "."):
        os.makedirs(folder, exist_ok=True)
        image = Image.open(io.BytesIO(self.raw_bytes))
        output_path = os.path.join(folder, output_file_name + "." + self.format)
        image.save(output_path)
