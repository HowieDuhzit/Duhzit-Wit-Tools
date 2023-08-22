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
    if "enum_values" in locals():
        importlib.reload(enum_values)
    if "functions" in locals():
        importlib.reload(functions)
    if "operators" in locals():
        importlib.reload(operators)
    if "menues" in locals():
        importlib.reload(menu)
else:
    from .enum_values import *
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
from .type_annotations import SMCIcons

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

try:
    from web3 import Web3

    web3_exist = True
except ImportError:
    web3_exist = False
    
if web3_exist:
    print("WEB3 Already Installed")
else:
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'web3', '-t', target])

from PIL import Image
from web3 import Web3

def register():
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for klass in CLASSES:
        bpy.utils.register_class(klass)

def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

if __name__ == "__main__":
    register()