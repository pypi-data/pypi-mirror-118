
from typing import Optional, Union
from PIL import Image, ImageTk  # type: ignore

from ..utils import FLAG_ICON_PATH, MINE_ICON_PATH

_FLAG_ICON: Optional[Union[ImageTk.PhotoImage, str]] = None
_MINE_ICON: Optional[Union[ImageTk.PhotoImage, str]] = None
_NO_ICON: str = ""


THUMBNAIL_SIZE = (18, 18)


def get_flag_icon() -> Union[ImageTk.PhotoImage, str]:
    global _FLAG_ICON
    if not _FLAG_ICON:
        flag_image = Image.open(FLAG_ICON_PATH)
        flag_image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        _FLAG_ICON = ImageTk.PhotoImage(flag_image)
    return _FLAG_ICON


def get_mine_icon() -> Union[ImageTk.PhotoImage, str]:
    global _MINE_ICON
    if not _MINE_ICON:
        mine_image = Image.open(MINE_ICON_PATH)
        mine_image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        _MINE_ICON = ImageTk.PhotoImage(mine_image)
    return _MINE_ICON


def get_no_icon() -> Union[ImageTk.PhotoImage, str]:
    return _NO_ICON
