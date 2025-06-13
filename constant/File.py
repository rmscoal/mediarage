import os
from enum import Enum
from typing import Union


class File(Enum):

    @staticmethod
    def from_str(value: str) -> Union["Image", "Video", None]:
        if value.upper() in [image.value for image in Image]:
            return Image(value)
        elif value.upper() in [video.value for video in Video]:
            return Video(value)
        return None

    @staticmethod
    def from_path(file_path: str) -> Union["Image", "Video", None]:
        _, ext = os.path.splitext(file_path)
        ext = ext.upper().strip(".")
        if ext in [image.value for image in Image]:
            return Image(ext)
        elif ext in [video.value for video in Video]:
            return Video(ext)
        return None


class Image(File):
    GIF = "GIF"
    JPEG = "JPEG"
    JPG = "JPG"
    PNG = "PNG"


class Video(File):
    AVI = "AVI"
    MOV = "MOV"
    MP4 = "MP4"
    MPEG = "MPEG"
