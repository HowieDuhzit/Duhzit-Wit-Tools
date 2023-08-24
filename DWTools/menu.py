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
from .icons import get_icon_id

class RIGToolsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "RIG Tools"
    bl_idname = "OG_PT_RIG_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
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
    bl_region_type = 'UI'
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
        boxcol.prop(scene, "out_path", icon_value=get_icon_id('download'))
        row = boxcol.row()
        row.prop(scene, "lora_name")
        row = boxcol.row()
        row.prop(scene, "lora_text")
        row = boxcol.row()
        boxcol.prop(scene, "pic_amount")
        row = boxcol.row()
        row.operator("lora.ren", icon_value=get_icon_id('image_search'))
        row = boxcol.row()
        row.operator("lora.tscan", icon_value=get_icon_id('image_search'))

class OBJToolsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "OBJ Tools"
    bl_idname = "OG_PT_OBJ_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
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
    bl_region_type = 'UI'
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
    bl_region_type = 'UI'
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
        col.operator('smc.browser', text='Discord', icon_value=get_icon_id('discord')).link = discord
        col.operator('smc.browser', text='GitHub', icon_value=get_icon_id('github')).link = github
        col.separator()
        col.operator('smc.browser', text='Support Howie Duhzit on Patreon', icon_value=get_icon_id('patreon')).link = patreon
        col.operator('smc.browser', text='Buy Me An Energy Drink', icon_value=get_icon_id('bmc')).link = buymeacoffee
        
class IMAGINEPANEL(bpy.types.Panel):
    bl_label = "Imagine"
    bl_idname = "IMAGINE_PT_material"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = 'material'
        
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        col = self.layout.column()
        box = col.box()
        boxcol = box.column()
        boxcol.scale_y = 1.2
        row = boxcol.row()
        col = self.layout.column(align = True)
        row = boxcol.row()
        row.prop(scene, "tex_width")
        row.prop(scene, "tex_height")
        row = layout.row()
        boxcol.prop(scene, "steps")
        row = layout.row()        
        
        box = col.box()
        boxcol = box.column()
        boxcol.scale_y = 1.2
        row = boxcol.row()
        col = self.layout.column(align = True)
        row = boxcol.row()
        row.prop(scene, "api_path")
        row = layout.row()
        box = col.box()
        boxcol = box.column()
        boxcol.scale_y = 1.2
        row = boxcol.row()
        col = self.layout.column(align = True)
        row = boxcol.row()
        row.prop(scene, "img_name")
        row.prop(scene, "tile")
        row = boxcol.row()
        row.prop(scene, "prompt")
        row = boxcol.row()
        row.prop(scene, "negprompt")
        row = boxcol.row()
        row.prop(scene, "seed")
        row = boxcol.row()
        row.operator("imagine.mat")