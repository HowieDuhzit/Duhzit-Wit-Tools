import os
from typing import cast
from typing import DefaultDict
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import bpy
import bpy.utils.previews

Icons = Union[bpy.utils.previews.ImagePreviewCollection, Dict[str, bpy.types.ImagePreview], None]
DW_icons = cast(Icons, None)
icons_directory = os.path.dirname(__file__)


def get_icon_id(identifier: str) -> int:
    return get_icon(identifier).icon_id


def get_icon(identifier: str) -> bpy.types.ImagePreview:
    if identifier in DW_icons:
        return DW_icons[identifier]
    return DW_icons.load(identifier, os.path.join(icons_directory, '{0}.png'.format(identifier)), 'IMAGE')


def get_img_icon_id(identifier: str, path: str) -> int:
    return get_img_icon(identifier, path).icon_id


def get_img_icon(identifier: str, path: str) -> bpy.types.ImagePreview:
    if identifier in DW_icons:
        return DW_icons[identifier]
    return DW_icons.load(identifier, path, 'IMAGE')


def initialize_DW_icons() -> None:
    global DW_icons
    DW_icons = bpy.utils.previews.new()


def unload_DW_icons() -> None:
    bpy.utils.previews.remove(DW_icons)
