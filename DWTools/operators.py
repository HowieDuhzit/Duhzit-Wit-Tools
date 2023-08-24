import bpy
import time
import requests
import subprocess
import sys
import os
import random
from math import radians
from io import BytesIO
from PIL import Image

from .properties import *
from .functions import *

class Imagine(bpy.types.Operator):
    """Imagine a material"""
    bl_idname = "imagine.mat"
    bl_label = "Imagine A New Material"

    def execute(self, context):
        imagine(context)
        return {'FINISHED'}

class M2V(bpy.types.Operator):

    bl_idname = "mixamo.vrm"
    bl_label = "Convert"

    def execute(self, context):
        mix2vrm(context)
        return {'FINISHED'}

class V2M(bpy.types.Operator):

    bl_idname = "vrm.mixamo"
    bl_label = "Convert"

    def execute(self, context):
        vrm2mix(context)
        return {'FINISHED'}

class BATCHVRM(bpy.types.Operator):

    bl_idname = "batch.vrm"
    bl_label = "Convert GLB"

    def execute(self, context):
        batchVRM(context)
        return {'FINISHED'}
        
class ARRAY(bpy.types.Operator):

    bl_idname = "array.obj"
    bl_label = "Array Objects"

    def execute(self, context):
        array(context)
        return {'FINISHED'}

class LORA(bpy.types.Operator):

    bl_idname = "lora.ren"
    bl_label = "Render LoRA"

    def execute(self, context):
        lora(context)
        return {'FINISHED'}

class TSCAN(bpy.types.Operator):

    bl_idname = "lora.tscan"
    bl_label = "Render LoRA Tscan"

    def execute(self, context):
        tscan(context)
        return {'FINISHED'}

class POSER(bpy.types.Operator):

    bl_idname = "poser.arm"
    bl_label = "Generate Custom Bone Properties"

    def execute(self, context):
        create_custom_properties_with_drivers()
        return {'FINISHED'}