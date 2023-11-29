import io
import os
from PIL import Image


class ImageSaver:
    is_saved: bool = False

    def __init__(self, raw_bytes: bytes, format: str = "jpg") -> None:
        self.raw_bytes = raw_bytes
        self.format = format

    def save(self, output_file_name: str = "output", folder: str = ".") -> None:
        os.makedirs(folder, exist_ok=True)
        image = Image.open(io.BytesIO(self.raw_bytes))
        output_path = os.path.join(
            folder, output_file_name + "." + self.format or "jpg"
        )
        image.save(output_path)
