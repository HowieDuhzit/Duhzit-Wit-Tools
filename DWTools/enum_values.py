import bpy

from .functions import *
from .operators import *
from .menu import *

PROPS = [
    ('x_axis', bpy.props.BoolProperty(name='X', default=False)),
    ('y_axis', bpy.props.BoolProperty(name='Y', default=False)),
    ('z_axis', bpy.props.BoolProperty(name='Z', default=False)),
    ('array_count', bpy.props.IntProperty(name='Array Count', default=1, min=1)),
    ('batch_start', bpy.props.IntProperty(name='Batch Start', default=1, min=1)),
    ('batch_end', bpy.props.IntProperty(name='Batch End', default=5555, min=1)),
    ('tex_size', bpy.props.IntProperty(name='Texture Size', default=1024, step=128)),
    ('pic_amount', bpy.props.IntProperty(name='Picture Amount', default=15, min=15, step=5)),
    ('out_path', bpy.props.StringProperty(name='Output Path', default="C:/tmp/LoRA/")),
    ('lora_text', bpy.props.StringProperty(name='LoRA Description', default="a character in a random pose, on white background.")),
    ('lora_name', bpy.props.StringProperty(name='LoRA Name', default="Name")),
]

#-----------------------------------------------------------------------------------------------------------------------------

CLASSES = [
    RIGToolsPanel,
    AIToolsPanel,
    OBJToolsPanel,
    CONToolsPanel,
    CreditsMenu,
    M2V,
    V2M,
    BATCHVRM,
    ARRAY,
    LORA,
    POSER,
]
