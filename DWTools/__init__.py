bl_info = {
    "name": "Duhzit Wit Tools",
    "author": "Howie Duhzit",
    "version": (0, 1, 5),
    "blender": (3, 40, 0),
    "location": "Viewport and Properties",
    "description": "Misc tools for Misc things",
    "warning": "",
    "wiki_url": "",
    "category": "User",
}
if "bpy" in locals():
    import importlib
    if "properties" in locals():
        importlib.reload(properties)
    if "functions" in locals():
        importlib.reload(functions)
    if "operators" in locals():
        importlib.reload(operators)
    if "menues" in locals():
        importlib.reload(menu)
else:
    from .properties import *
    from .functions import *
    from .operators import *
    from .menu import *

import bpy
import time
import requests
import subprocess
import sys
import os
import random
from math import radians
from io import BytesIO
from bpy.props import (
    PointerProperty,
    )
from bpy.types import (
    AddonPreferences,
    PropertyGroup,
    )
from .icons import initialize_DW_icons
from .icons import unload_DW_icons

python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
target = os.path.join(sys.prefix, 'lib', 'site-packages')

try:
    from PIL import Image
    from PIL import ImageChops

    pil_exist = True
except ImportError:
    pil_exist = False    
if pil_exist:
    print("PIL Already Installed")
else:
    subprocess.call([python_exe, '-m', 'ensurepip'])
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pillow', '-t', target])
from PIL import Image

def register():
    initialize_DW_icons()
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for klass in CLASSES:
        bpy.utils.register_class(klass)

def unregister():
    unload_DW_icons()
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

if __name__ == "__main__":
    register()