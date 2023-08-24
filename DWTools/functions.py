import bpy
import time
import requests
import subprocess
import sys
import os
import random
import json
import base64
import math
import shutil
from math import radians
from io import BytesIO
from PIL import Image, ImageChops
import cv2

def generate_normal_map(input_image, strength=1):
    width, height = input_image.size
    normal_map = Image.new('RGB', (width, height), (128, 128, 255))
    
    for y in range(height):
        for x in range(width):
            # Get grayscale value of the input image
            center = input_image.getpixel((x, y))[0]
            
            # Calculate gradients using surrounding pixels
            left = input_image.getpixel((x - 1, y))[0] if x > 0 else center
            right = input_image.getpixel((x + 1, y))[0] if x < width - 1 else center
            up = input_image.getpixel((x, y - 1))[0] if y > 0 else center
            down = input_image.getpixel((x, y + 1))[0] if y < height - 1 else center
            
            # Calculate normal vectors from gradients
            dx = (right - left) / 255.0 * strength
            dy = (down - up) / 255.0 * strength
            dz = 1.0 / strength
            
            # Normalize the vector
            length = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
            dx /= length
            dy /= length
            dz /= length
            
            # Map the normal vector to RGB colors
            red = int((dx + 1) * 0.5 * 255)
            green = int((dy + 1) * 0.5 * 255)
            blue = int((dz + 1) * 0.5 * 255)
            
            normal_map.putpixel((x, y), (red, green, blue))
    
    return normal_map
def convert_to_displacement_map(diffuse_img):
    gray_img = cv2.cvtColor(diffuse_img, cv2.COLOR_BGR2GRAY)
    displacement_map = gray_img.astype(np.float32) / 255.0
    return displacement_map

def empty_and_remove_folder(folder_path):
    try:
        # Delete all files and subfolders within the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        # Remove the empty folder
        os.rmdir(folder_path)
        print(f"Folder '{folder_path}' has been emptied and removed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def mix2vrm(context):
    bpy.ops.object.editmode_toggle()
    for bone in bpy.context.view_layer.objects.active.data.edit_bones:
        if "Hips" in bone.name:
            bone.name = "hips"
        elif "Spine1" in bone.name:
            bone.name = "chest"
        elif "Spine2" in bone.name:
            bone.name = "upper_chest"
        elif "Neck" in bone.name:
            bone.name = "neck"
        elif "Head" in bone.name:
            bone.name = "head"
        elif "LeftEye" in bone.name:
            bone.name = "eye.L"
        elif "RightEye" in bone.name:
            bone.name = "eye.R"
        elif "LeftShoulder" in bone.name:
            bone.name = "shoulder.L"
        elif "LeftArm" in bone.name:
            bone.name = "upper_arm.L"
        elif "LeftForeArm" in bone.name:
            bone.name = "lower_arm.L"
        elif "LeftHandThumb1" in bone.name:
            bone.name = "thumb_proximal.L"
        elif "LeftHandThumb2" in bone.name:
            bone.name = "thumb_intermediate.L"
        elif "LeftHandThumb3" in bone.name:
            bone.name = "thumb_distal.L"
        elif "LeftHandIndex1" in bone.name:
            bone.name = "index_proximal.L"
        elif "LeftHandIndex2" in bone.name:
            bone.name = "index_intermediate.L"
        elif "LeftHandIndex3" in bone.name:
            bone.name = "index_distal.L"
        elif "LeftHandMiddle1" in bone.name:
            bone.name = "middle_proximal.L"
        elif "LeftHandMiddle2" in bone.name:
            bone.name = "middle_intermediate.L"
        elif "LeftHandMiddle3" in bone.name:
            bone.name = "middle_distal.L"
        elif "LeftHandRing1" in bone.name:
            bone.name = "ring_proximal.L"
        elif "LeftHandRing2" in bone.name:
            bone.name = "ring_intermediate.L"
        elif "LeftHandRing3" in bone.name:
            bone.name = "ring_distal.L"
        elif "LeftHandPinky1" in bone.name:
            bone.name = "little_proximal.L"
        elif "LeftHandPinky2" in bone.name:
            bone.name = "little_intermediate.L"
        elif "LeftHandPinky3" in bone.name:
            bone.name = "little_distal.L"
        elif "RightShoulder" in bone.name:
            bone.name = "shoulder.R"
        elif "RightArm" in bone.name:
            bone.name = "upper_arm.R"
        elif "RightForeArm" in bone.name:
            bone.name = "lower_arm.R"
        elif "RightHandThumb1" in bone.name:
            bone.name = "thumb_proximal.R"
        elif "RightHandThumb2" in bone.name:
            bone.name = "thumb_intermediate.R"
        elif "RightHandThumb3" in bone.name:
            bone.name = "thumb_distal.R"
        elif "RightHandIndex1" in bone.name:
            bone.name = "index_proximal.R"
        elif "RightHandIndex2" in bone.name:
            bone.name = "index_intermediate.R"
        elif "RightHandIndex3" in bone.name:
            bone.name = "index_distal.R"
        elif "RightHandMiddle1" in bone.name:
            bone.name = "middle_proximal.R"
        elif "RightHandMiddle2" in bone.name:
            bone.name = "middle_intermediate.R"
        elif "RightHandMiddle3" in bone.name:
            bone.name = "middle_distal.R"
        elif "RightHandRing1" in bone.name:
            bone.name = "ring_proximal.R"
        elif "RightHandRing2" in bone.name:
            bone.name = "ring_intermediate.R"
        elif "RightHandRing3" in bone.name:
            bone.name = "ring_distal.R"
        elif "RightHandPinky1" in bone.name:
            bone.name = "little_proximal.R"
        elif "RightHandPinky2" in bone.name:
            bone.name = "little_intermediate.R"
        elif "RightHandPinky3" in bone.name:
            bone.name = "little_distal.R"
        elif "LeftUpLeg" in bone.name:
            bone.name = "upper_leg.L"
        elif "LeftLeg" in bone.name:
            bone.name = "lower_leg.L"
        elif "LeftFoot" in bone.name:
            bone.name = "foot.L"
        elif "LeftToeBase" in bone.name:
            bone.name = "toes.L"
        elif "RightUpLeg" in bone.name:
            bone.name = "upper_leg.R"
        elif "RightLeg" in bone.name:
            bone.name = "lower_leg.R"
        elif "RightFoot" in bone.name:
            bone.name = "foot.R"
        elif "RightToeBase" in bone.name:
            bone.name = "toes.R"
        elif "LeftHand" in bone.name:
            bone.name = "hand.L"
        elif "RightHand" in bone.name:
            bone.name = "hand.R"
        elif "Spine" in bone.name:
            bone.name = "spine"                
    bpy.ops.object.editmode_toggle()
    bpy.context.view_layer.objects.active.name = "VRM RIG"
 
def vrm2mix(context):
    bpy.ops.object.editmode_toggle()
    for bone in bpy.context.view_layer.objects.active.data.edit_bones:
        if "hips" in bone.name:
            bone.name = "mixamorig:Hips"
        elif "chest" in bone.name:
            bone.name = "mixamorig:Spine1"
        elif "upper_chest" in bone.name:
            bone.name = "mixamorig:Spine2"
        elif "neck" in bone.name:
            bone.name = "mixamorig:Neck"
        elif "head" in bone.name:
            bone.name = "mixamorig:Head"
        elif "eye.L" in bone.name:
            bone.name = "mixamorig:LeftEye"
        elif "eye.R" in bone.name:
            bone.name = "mixamorig:RightEye"
        elif "shoulder.L" in bone.name:
            bone.name = "mixamorig:LeftShoulder"
        elif "upper_arm.L" in bone.name:
            bone.name = "mixamorig:LeftArm"
        elif "lower_arm.L" in bone.name:
            bone.name = "mixamorig:LeftForeArm"
        elif "thumb_proximal.L" in bone.name:
            bone.name = "mixamorig:LeftHandThumb1"
        elif "thumb_intermediate.L" in bone.name:
            bone.name = "mixamorig:LeftHandThumb2"
        elif "thumb_distal.L" in bone.name:
            bone.name = "mixamorig:LeftHandThumb3"
        elif "index_proximal.L" in bone.name:
            bone.name = "mixamorig:LeftHandIndex1"
        elif "index_intermediate.L" in bone.name:
            bone.name = "mixamorig:LeftHandIndex2"
        elif "index_distal.L" in bone.name:
            bone.name = "mixamorig:LeftHandIndex3"
        elif "middle_proximal.L" in bone.name:
            bone.name = "mixamorig:LeftHandMiddle1"
        elif "middle_intermediate.L" in bone.name:
            bone.name = "mixamorig:LeftHandMiddle2"
        elif "middle_distal.L" in bone.name:
            bone.name = "mixamorig:LeftHandMiddle3"
        elif "ring_proximal.L" in bone.name:
            bone.name = "mixamorig:LeftHandRing1"
        elif "ring_intermediate.L" in bone.name:
            bone.name = "mixamorig:LeftHandRing2"
        elif "ring_distal.L" in bone.name:
            bone.name = "mixamorig:LeftHandRing3"
        elif "little_proximal.L" in bone.name:
            bone.name = "mixamorig:LeftHandPinky1"
        elif "little_intermediate.L" in bone.name:
            bone.name = "mixamorig:LeftHandPinky2"
        elif "little_distal.L" in bone.name:
            bone.name = "mixamorig:LeftHandPinky3"
        elif "shoulder.R" in bone.name:
            bone.name = "mixamorig:RightShoulder"
        elif "upper_arm.R" in bone.name:
            bone.name = "mixamorig:RightArm"
        elif "lower_arm.R" in bone.name:
            bone.name = "mixamorig:RightForeArm"
        elif "thumb_proximal.R" in bone.name:
            bone.name = "mixamorig:RightHandThumb1"
        elif "thumb_intermediate.R" in bone.name:
            bone.name = "mixamorig:RightHandThumb2"
        elif "thumb_distal.R" in bone.name:
            bone.name = "mixamorig:RightHandThumb3"
        elif "index_proximal.R" in bone.name:
            bone.name = "mixamorig:RightHandIndex1"
        elif "index_intermediate.R" in bone.name:
            bone.name = "mixamorig:RightHandIndex2"
        elif "index_distal.R" in bone.name:
            bone.name = "mixamorig:RightHandIndex3"
        elif "middle_proximal.R" in bone.name:
            bone.name = "mixamorig:RightHandMiddle1"
        elif "middle_intermediate.R" in bone.name:
            bone.name = "mixamorig:RightHandMiddle2"
        elif "middle_distal.R" in bone.name:
            bone.name = "mixamorig:RightHandMiddle3"
        elif "ring_proximal.R" in bone.name:
            bone.name = "mixamorig:RightHandRing1"
        elif "ring_intermediate.R" in bone.name:
            bone.name = "mixamorig:RightHandRing2"
        elif "ring_distal.R" in bone.name:
            bone.name = "mixamorig:RightHandRing3"
        elif "little_proximal.R" in bone.name:
            bone.name = "mixamorig:RightHandPinky1"
        elif "little_intermediate.R" in bone.name:
            bone.name = "mixamorig:RightHandPinky2"
        elif "little_distal.R" in bone.name:
            bone.name = "mixamorig:RightHandPinky3"
        elif "upper_leg.L" in bone.name:
            bone.name = "mixamorig:LeftUpLeg"
        elif "lower_leg.L" in bone.name:
            bone.name = "mixamorig:LeftLeg"
        elif "foot.L" in bone.name:
            bone.name = "mixamorig:LeftFoot"
        elif "toes.L" in bone.name:
            bone.name = "mixamorig:LeftToeBase"
        elif "upper_leg.R" in bone.name:
            bone.name = "mixamorig:RightUpLeg"
        elif "lower_leg.R" in bone.name:
            bone.name = "mixamorig:RightLeg"
        elif "foot.R" in bone.name:
            bone.name = "mixamorig:RightFoot"
        elif "toes.R" in bone.name:
            bone.name = "mixamorig:RightToeBase"
        elif "hand.L" in bone.name:
            bone.name = "mixamorig:LeftHand"
        elif "hand.R" in bone.name:
            bone.name = "mixamorig:RightHand"
        elif "spine" in bone.name:
            bone.name = "mixamorig:Spine"             
    bpy.ops.object.editmode_toggle()
    bpy.context.view_layer.objects.active.name = "Mixamo RIG"

def batchVRM(context):
    i = context.scene.batch_start
    while i <= context.scene.batch_end:
        path_to_file = bpy.path.abspath('//') + str(i) +".glb"
        print("*****Importing " + path_to_file +"*****")
        bpy.ops.import_scene.gltf(filepath=path_to_file)
                
        print("*****Resizing Textures*****")
        for img in bpy.data.images:
            if img.name != "Render Result":
                img.scale(context.scene.tex_size,context.scene.tex_size)
                
        print("*****Applying Bones*****")
        mix2vrm(context)
        bpy.ops.vrm.assign_vrm0_humanoid_human_bones_automatically(armature_name="VRM RIG")

        print("*****Exporting " + path_to_file+"*****")  
        output_file = bpy.path.abspath('//') + str(i) + ".vrm"
        bpy.ops.export_scene.vrm(filepath=output_file,armature_object_name="VRM RIG")
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=True)
        i += 1
    print("*****FINISHED*****")

def array(context):
    objDims = bpy.context.active_object.dimensions
    for i in range(context.scene.array_count):
        bpy.ops.object.duplicate()
        if context.scene.x_axis:
            bpy.ops.transform.translate(value=(objDims.x,0,0))
        elif context.scene.y_axis:
            bpy.ops.transform.translate(value=(0,objDims.y,0))
        elif context.scene.z_axis:
            bpy.ops.transform.translate(value=(0,0,objDims.z))

def lora(context):
    arm = bpy.data.objects["Armature"]
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')

    max_rotation_x = 30
    max_rotation_y = 30
    max_rotation_z = 30
    os.makedirs(str(context.scene.out_path)+"/image")
    os.makedirs(str(context.scene.out_path)+"/log")
    os.makedirs(str(context.scene.out_path)+"/model")
    os.makedirs(str(context.scene.out_path)+"/image/100_"+str(context.scene.lora_name))
    for index, _ in enumerate(range(0,context.scene.pic_amount*2,2)):
        if _ % 2 == 1:
            continue
        formatted_num = f"{_:04}"
        for bone in bpy.data.objects['Armature'].pose.bones.values():
            bone.rotation_mode = 'XYZ'
            random_rotation_x = random.uniform(-max_rotation_x, max_rotation_x)
            random_rotation_y = random.uniform(-max_rotation_y, max_rotation_y)
            random_rotation_z = random.uniform(-max_rotation_z, max_rotation_z)
            
            bone.rotation_euler.x = radians(random_rotation_x)
            bone.rotation_euler.y = radians(random_rotation_y)
            bone.rotation_euler.z = radians(random_rotation_z)
 
        renderOut(context,formatted_num,index)

def renderOut(context,num,index,angle):
    bpy.ops.render.render(use_viewport=True)    
    bpy.data.images['Render Result'].save_render(str(context.scene.out_path)+"/image/100_"+str(context.scene.lora_name)+"/"+f"{num}-0-" + str(index) + ".png")
    filename = str(str(context.scene.out_path)+"/image/100_"+str(context.scene.lora_name)+"/"+f"{num}-0-" + str(index) + ".txt")
    with open(filename, 'w') as file:
        file.write(context.scene.lora_name+" is "+context.scene.lora_text+ " at a "+str(angle)+" degree angle")

def tscan(context):
    arm = bpy.data.objects.get("Armature")
    if arm is None:
        print("Armature not found")
        return
    
    bpy.context.view_layer.objects.active = arm
    obj = bpy.context.active_object
    
    out_path = context.scene.out_path
    pic_amount = context.scene.pic_amount
    lora_name = context.scene.lora_name
    
    empty_and_remove_folder(out_path)
    os.makedirs(os.path.join(out_path, "image"))
    os.makedirs(os.path.join(out_path, "log"))
    os.makedirs(os.path.join(out_path, "model"))
    os.makedirs(os.path.join(out_path, f"image/100_{lora_name}"))
    
    for index in range(pic_amount):
        angle_degrees = (index / pic_amount) * 360  # Calculate angle in degrees
        rounded_angle_degrees = round(angle_degrees)
        formatted_num = f"{index:04}"
        
        print(f"Making Scene angle: {rounded_angle_degrees} degrees")
        obj.rotation_mode = 'XYZ'
        obj.rotation_euler.z = math.radians(rounded_angle_degrees)  # Convert to radians
        
        renderOut(context, formatted_num, index, rounded_angle_degrees)

def imagine(context):
    url = "http://"+context.scene.api_path+"/sdapi/v1/txt2img"
    prompt = context.scene.prompt
    headers = {
    "Content-Type": "application/json"
    }
    data = {
    "prompt": context.scene.prompt,
    "steps": context.scene.steps,
    "sampler_index": "DPM++ 2M SDE Karras",
    "tiling": context.scene.tile,
    "negative_prompt": context.scene.negprompt,
    "seed": context.scene.seed,
    "width": context.scene.tex_width,
    "height": context.scene.tex_height,
    }
    for i in bpy.data.images:
        if i.name == str(context.scene.img_name) +"_diffuse.png":
            bpy.data.images.remove(i, do_unlink=True)
        elif i.name == str(context.scene.img_name) +"_normal.png":
            bpy.data.images.remove(i, do_unlink=True)
    
    response = requests.post(url, json=data, headers=headers)
    r = response.json()
    
    for i in r['images']:
        diffuse_image = Image.open(BytesIO(base64.b64decode(i.split(",",1)[0])))
        diffuse_image.save("C:/tmp/" + context.scene.img_name + "_diffuse.png", "PNG")
        input_image = bpy.data.images.load("C:/tmp/" + context.scene.img_name + "_diffuse.png")
        
        #normal_map = generate_normal_map(input_image, strength=1)
        #normal_image = Image.fromarray(normal_map)
        #normal_map.save("C:/tmp/" + prompt + "_normal.png", "PNG")
        
        #displacement_map = convert_to_displacement_map(diffuse_image)
        #displacement_image = Image.fromarray(displacement_map)
        #displacement_image.save("C:/tmp/" + prompt + "_displace.png", "PNG")
        
    mat = bpy.data.materials.new(name=context.scene.img_name+"_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.new('ShaderNodeTexCoord').name = "coord"
    nodes.new('ShaderNodeMapping').name = "map"
    nodes.new('ShaderNodeTexImage').name = "diffuse"
    nodes.new('ShaderNodeTexImage').name = "normal"
    nodes.new('ShaderNodeNormalMap').name = "normMap"
    nodes['diffuse'].image = bpy.data.images[context.scene.img_name+"_diffuse.png"]
    #nodes['normal'].image = bpy.data.images[prompt+"_normal.png"]
    links.new(nodes["coord"].outputs[2],nodes["map"].inputs[0])
    links.new(nodes["map"].outputs[0],nodes["diffuse"].inputs[0])
    links.new(nodes["map"].outputs[0],nodes["normal"].inputs[0])
    links.new(nodes["diffuse"].outputs[0],nodes["Principled BSDF"].inputs[0])
    links.new(nodes["normal"].outputs[0],nodes["normMap"].inputs[1])
    links.new(nodes["normMap"].outputs[0],nodes["Principled BSDF"].inputs[22])
    nodes["Principled BSDF"].inputs['Specular'].default_value = 0.2
    nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.8
    nodes["Principled BSDF"].inputs['Metallic'].default_value = 0
   
    obj = bpy.context.active_object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return {'FINISHED'}

def create_custom_properties_with_drivers():
    selected_armature = bpy.context.active_object

    if selected_armature and selected_armature.type == 'ARMATURE':
        bpy.ops.object.mode_set(mode='OBJECT')  # Switch to object mode if in edit mode

        for bone in selected_armature.data.bones:
            property_name_x = bone.name + "_X"
            property_name_y = bone.name + "_Y"
            property_name_z = bone.name + "_Z"

            if property_name_x in selected_armature:
                del selected_armature[property_name_x]
            if property_name_y in selected_armature:
                del selected_armature[property_name_y]
            if property_name_z in selected_armature:
                del selected_armature[property_name_z]

            selected_armature[property_name_x] = 0.0
            selected_armature.id_properties_ui(property_name_x).update(subtype='ANGLE')
            selected_armature[property_name_y] = 0.0
            selected_armature.id_properties_ui(property_name_y).update(subtype='ANGLE')
            selected_armature[property_name_z] = 0.0
            selected_armature.id_properties_ui(property_name_z).update(subtype='ANGLE')


        bpy.ops.object.mode_set(mode='POSE')  # Switch to pose mode

        for bone in selected_armature.pose.bones:
            bone.rotation_mode = 'XYZ'
            driver = bone.driver_add('rotation_euler', 0)  # 0 corresponds to X Euler rotation
            driver.driver.type = 'SCRIPTED'
            driver.driver.expression = 'var'
            driver_var = driver.driver.variables.new()
            driver_var.type = 'SINGLE_PROP'
            driver_var.name = 'var'
            driver_var.targets[0].id_type = 'OBJECT'
            driver_var.targets[0].id = selected_armature
            driver_var.targets[0].data_path = f'["{bone.name}_X"]'
            
            driver = bone.driver_add('rotation_euler', 1)  # 0 corresponds to X Euler rotation
            driver.driver.type = 'SCRIPTED'
            driver_var = driver.driver.variables.new()
            driver_var.type = 'SINGLE_PROP'
            driver_var.name = 'var'
            driver_var.targets[0].id_type = 'OBJECT'
            driver_var.targets[0].id = selected_armature
            driver_var.targets[0].data_path = f'["{bone.name}_Y"]'
            driver.driver.expression = 'var'
            
            driver = bone.driver_add('rotation_euler', 2)  # 0 corresponds to X Euler rotation
            driver.driver.type = 'SCRIPTED'
            driver_var = driver.driver.variables.new()
            driver_var.type = 'SINGLE_PROP'
            driver_var.name = 'var'
            driver_var.targets[0].id_type = 'OBJECT'
            driver_var.targets[0].id = selected_armature
            driver_var.targets[0].data_path = f'["{bone.name}_Z"]'
            driver.driver.expression = 'var'

        print("Custom properties and drivers created successfully!")
    else:
        print("Please select an armature object.")
    bpy.ops.object.mode_set(mode='OBJECT')
    