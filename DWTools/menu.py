import bpy
import time
import requests
import subprocess
import sys
import os
import random
from math import radians
from io import BytesIO

from . import bl_info

from .functions import *
from .operators import *

is_blender_2_79_or_older = bpy.app.version < (2, 80, 0)
is_blender_2_80_or_newer = bpy.app.version >= (2, 80, 0)
is_blender_2_92_or_newer = bpy.app.version >= (2, 92, 0)
is_blender_3_or_newer = bpy.app.version >= (3, 0, 0)


class RIGToolsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "RIG Tools"
    bl_idname = "OG_PT_RIG_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if is_blender_2_80_or_newer else 'TOOLS'
    bl_category = "DWTOOLS"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        col = self.layout.column()
        box = col.box()
        
        boxcol = box.column()
        boxcol.scale_y = 1.2
        row = boxcol.row()
        boxcol.label(text="Convert Mixamo Rig To VRM Rigged                 Convert VRM Rig to Mixamo Rig")
        row = boxcol.row()
        row.operator("mixamo.vrm")
        row.operator("vrm.mixamo")
        
        boxtwo = col.box()
        boxcol = boxtwo.column()
        boxcol.scale_y = 1.2
        row = boxcol.row()
        boxcol.label(text="Add Custom Properties to Armature")
        row = boxcol.row()
        row.operator("poser.arm")
        
class AIToolsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "AI Tools"
    bl_idname = "OG_PT_AI_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if is_blender_2_80_or_newer else 'TOOLS'
    bl_category = "DWTOOLS"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        col = self.layout.column()
        box = col.box()
        
        boxcol = box.column()
        boxcol.scale_y = 1.2
        row = boxcol.row()
        boxcol.label(text="Generate LoRA training data from Rigged Model")
        boxcol.label(text="Kohya Ready")
        row = boxcol.row()
        boxcol.prop(scene, "out_path")
        row = boxcol.row()
        row.prop(scene, "lora_name")
        row = boxcol.row()
        row.prop(scene, "lora_text")
        row = boxcol.row()
        boxcol.prop(scene, "pic_amount")
        row = boxcol.row()
        row.operator("lora.ren")

class OBJToolsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "OBJ Tools"
    bl_idname = "OG_PT_OBJ_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if is_blender_2_80_or_newer else 'TOOLS'
    bl_category = "DWTOOLS"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        col = self.layout.column()
        box = col.box()
        boxcol = box.column()
        boxcol.scale_y = 1.2
        row = boxcol.row()
        boxcol.label(text="Object Array")
        row = boxcol.row()
        row.prop(scene, "x_axis")
        row.prop(scene, "y_axis")
        row.prop(scene, "z_axis")
        boxcol.prop(scene, "array_count")
        row = boxcol.row()
        row.operator("array.obj")

class CONToolsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Conversion Tools"
    bl_idname = "OG_PT_Convert_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if is_blender_2_80_or_newer else 'TOOLS'
    bl_category = "DWTOOLS"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        col = self.layout.column()
        box = col.box()
        boxcol = box.column()
        boxcol.scale_y = 1.2
        row = boxcol.row()
        boxcol.label(text="Batch convert GLB To VRM")
        row = boxcol.row()
        boxcol.label(text="Searches folder of .blend for .glbs")
        row = boxcol.row()
        boxcol.label(text="*May be buggy*")
        boxcol.prop(scene, "batch_start")
        boxcol.prop(scene, "batch_end")
        boxcol.prop(scene, "tex_size")
        row = boxcol.row()
        row.operator("batch.vrm")

class CreditsMenu(bpy.types.Panel):
    bl_label = 'Credits'
    bl_idname = 'OG_PT_Credits_Menu'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' if is_blender_2_80_or_newer else 'TOOLS'
    bl_category = 'DWTOOLS'

    def draw(self, context):
        github = 'https://github.com/HowieDuhzit'
        discord = 'https://discord.gg/nJAh55ppJ6'
        patreon = 'https://www.patreon.com/HowieDuhzit'
        buymeacoffee = 'https://buymeacoffee.com/HowieDuhzit'
        
        m_col = self.layout.column()
        box = m_col.box()
        col = box.column()
        col.scale_y = 1.2
        col.operator('smc.browser', text='Contact me on Discord (@HowieDuhzit)').link = discord
        col.operator('smc.browser', text='Report a Bug on GitHub').link = github
        col.separator()
        col.operator('smc.browser', text='Support Howie Duhzit on Patreon').link = patreon
        col.operator('smc.browser', text='Buy Me An Energy Drink').link = buymeacoffee