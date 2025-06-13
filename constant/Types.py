from enum import Enum
from typing import Union


class File(Enum):

    @staticmethod
    def from_str(value: str) -> Union["Image", "Video", None]:
        if value in [image.value for image in Image]:
            return Image(value)
        elif value in [video.value for video in Video]:
            return Video(value)
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
