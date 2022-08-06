from gltflib import GLTF
import shutil
import os
import sys

args = sys.argv
vrm_filename = args[1]

# Prepare Filenames
glb_filename = vrm_filename[:-4] + '_temp.glb'
glb_new_filename = vrm_filename[:-4] + '_temp_mod.glb'
vrm_new_filename = vrm_filename[:-4] + '_mod.vrm'

# Copy and Change File Extension to GLB file
shutil.copy(vrm_filename, glb_filename)

# Load
gltf = GLTF.load_glb(glb_filename)

# Find Node IDs
id_upper_chest = next(filter(lambda b: b['bone']=='upperChest', gltf.model.extensions['VRM']['humanoid']['humanBones']), None)['node']
id_chest = next(filter(lambda b: b['bone']=='chest', gltf.model.extensions['VRM']['humanoid']['humanBones']), None)['node']
id_neck = next(filter(lambda b: b['bone']=='neck', gltf.model.extensions['VRM']['humanoid']['humanBones']), None)['node']
id_left_shoulder = next(filter(lambda b: b['bone']=='leftShoulder', gltf.model.extensions['VRM']['humanoid']['humanBones']), None)['node']
id_right_shoulder = next(filter(lambda b: b['bone']=='rightShoulder', gltf.model.extensions['VRM']['humanoid']['humanBones']), None)['node']

# Move Childlen of UpperChest to Chest
upper_chest_node = gltf.model.nodes[id_upper_chest]
upper_chest_node.children.remove(id_neck)
upper_chest_node.children.remove(id_left_shoulder)
upper_chest_node.children.remove(id_right_shoulder)

chest_node = gltf.model.nodes[id_chest]
chest_node.children.append(id_neck)
chest_node.children.append(id_left_shoulder)
chest_node.children.append(id_right_shoulder)

# Add Translation of UpperChest to Every Former Children of UpperChest
neck_node = gltf.model.nodes[id_neck]
neck_node.translation[0] += upper_chest_node.translation[0]
neck_node.translation[1] += upper_chest_node.translation[1]
neck_node.translation[2] += upper_chest_node.translation[2]

left_shoulder_node = gltf.model.nodes[id_left_shoulder]
left_shoulder_node.translation[0] += upper_chest_node.translation[0]
left_shoulder_node.translation[1] += upper_chest_node.translation[1]
left_shoulder_node.translation[2] += upper_chest_node.translation[2]

right_shoulder_node = gltf.model.nodes[id_right_shoulder]
right_shoulder_node.translation[0] += upper_chest_node.translation[0]
right_shoulder_node.translation[1] += upper_chest_node.translation[1]
right_shoulder_node.translation[2] += upper_chest_node.translation[2]

# Remove Chest Node From Humanoid
upper_chest = next(filter(lambda b: b['bone']=='upperChest', gltf.model.extensions['VRM']['humanoid']['humanBones']), None)
gltf.model.extensions['VRM']['humanoid']['humanBones'].remove(upper_chest)

# Export GLB
gltf.export_glb(glb_new_filename)

# Copy and Change File Extension to GLB file
shutil.copy(glb_new_filename, vrm_new_filename)

# Remove Temporary Files
os.remove(glb_filename)
os.remove(glb_new_filename)

