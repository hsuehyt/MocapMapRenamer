import maya.cmds as cmds
import os

def load_name_mapping(file_path):
    mapping = {}
    side_right = 'R'
    side_left = 'L'
    side_middle = ''
    side_before_name = True
    side_underscore = False

    with open(file_path, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if '=' in line:
                key, value = line.split('=')
                key, value = key.strip(), value.strip()
                if key == 'sideRight':
                    side_right = value
                elif key == 'sideLeft':
                    side_left = value
                elif key == 'sideMiddle':
                    side_middle = value
                elif key == 'sideBeforeName':
                    side_before_name = bool(int(value))
                elif key == 'sideUnderScore':
                    side_underscore = bool(int(value))
                else:
                    mapping[key] = value

    return mapping, side_right, side_left, side_middle, side_before_name, side_underscore

def rename_bones(name_matchers_folder, original_system='AdvancedSkeleton', target_system='Plask'):
    original_file = os.path.join(name_matchers_folder, f'{original_system}.txt')
    target_file = os.path.join(name_matchers_folder, f'{target_system}.txt')

    if not os.path.exists(original_file) or not os.path.exists(target_file):
        cmds.error('Original or Target system file not found!')
        return

    orig_map, orig_r, orig_l, orig_m, orig_before, orig_us = load_name_mapping(original_file)
    tgt_map, tgt_r, tgt_l, tgt_m, tgt_before, tgt_us = load_name_mapping(target_file)

    all_joints = cmds.ls(type='joint')

    for joint in all_joints:
        new_name = joint
        for key, value in orig_map.items():
            if key in joint:
                replacement = tgt_map.get(key, key)
                if orig_before:
                    new_name = new_name.replace(f'{orig_r}_{key}', f'{tgt_r}_' + replacement if tgt_us else f'{tgt_r}{replacement}')
                    new_name = new_name.replace(f'{orig_l}_{key}', f'{tgt_l}_' + replacement if tgt_us else f'{tgt_l}{replacement}')
                    if orig_m:
                        new_name = new_name.replace(f'{orig_m}_{key}', f'{tgt_m}_' + replacement if tgt_us else f'{tgt_m}{replacement}')
                else:
                    new_name = new_name.replace(f'{key}_{orig_r}', replacement + f'_{tgt_r}' if tgt_us else f'{replacement}{tgt_r}')
                    new_name = new_name.replace(f'{key}_{orig_l}', replacement + f'_{tgt_l}' if tgt_us else f'{replacement}{tgt_l}')
                    if orig_m:
                        new_name = new_name.replace(f'{key}_{orig_m}', replacement + f'_{tgt_m}' if tgt_us else f'{replacement}{tgt_m}')

        if new_name != joint:
            cmds.rename(joint, new_name)

def show_ui():
    default_dir = r'C:/Users/hsueh/Documents/maya/scripts/AdvancedSkeleton/AdvancedSkeletonFiles/moCapMatchers'

    if cmds.window('renameBonesUI', exists=True):
        cmds.deleteUI('renameBonesUI')

    window = cmds.window('renameBonesUI', title='Mocap Map Renamer', width=300, height=200)
    
    # Main form layout
    form = cmds.formLayout(numberOfDivisions=100)
    
    # Create UI elements
    title_text = cmds.text(label='Mocap Map:', align='center')
    folder_path = cmds.textField(text=default_dir, width=200)
    browse_btn = cmds.button(label='Browse', command=lambda x: browse_folder(folder_path))
    
    orig_text = cmds.text(label='Original Bone System:', align='center')
    orig_menu = cmds.optionMenu('origMenu', width=200)
    
    target_text = cmds.text(label='Target Bone System:', align='center')
    target_menu = cmds.optionMenu('targetMenu', width=200)
    
    refresh_btn = cmds.button(label='Refresh Systems', command=lambda x: refresh_systems(folder_path))
    apply_btn = cmds.button(label='Apply Rename', command=lambda x: apply_rename(folder_path), height=100)
    
    # Position elements in the form
    cmds.formLayout(form, edit=True, attachForm=[
        (title_text, 'top', 5), (title_text, 'left', 0), (title_text, 'right', 0),
        (folder_path, 'left', 10), (folder_path, 'right', 10),
        (browse_btn, 'left', 0), (browse_btn, 'right', 0),
        (orig_text, 'left', 0), (orig_text, 'right', 0),
        (orig_menu, 'left', 10), (orig_menu, 'right', 10),
        (target_text, 'left', 0), (target_text, 'right', 0),
        (target_menu, 'left', 10), (target_menu, 'right', 10),
        (refresh_btn, 'left', 0), (refresh_btn, 'right', 0),
        (apply_btn, 'left', 0), (apply_btn, 'right', 0), (apply_btn, 'bottom', 5)
    ])
    
    cmds.formLayout(form, edit=True, attachControl=[
        (folder_path, 'top', 5, title_text),
        (browse_btn, 'top', 5, folder_path),
        (orig_text, 'top', 10, browse_btn),
        (orig_menu, 'top', 5, orig_text),
        (target_text, 'top', 10, orig_menu),
        (target_menu, 'top', 5, target_text),
        (refresh_btn, 'top', 10, target_menu),
        (apply_btn, 'top', 5, refresh_btn)
    ])
    
    # Load the systems
    refresh_systems(folder_path)

    # Set default target to 'Plask' if available
    target_items = cmds.optionMenu('targetMenu', q=True, itemListLong=True) or []
    target_labels = [cmds.menuItem(item, q=True, label=True) for item in target_items]
    if 'Plask' in target_labels:
        cmds.optionMenu('targetMenu', e=True, v='Plask')

    cmds.showWindow(window)
    cmds.window(window, edit=True, width=300, height=200)

def browse_folder(folder_path_field):
    folder = cmds.fileDialog2(fileMode=3, caption='Select nameMatchers folder')
    if folder:
        cmds.textField(folder_path_field, e=True, text=folder[0])
        refresh_systems(folder_path_field)

def refresh_systems(folder_path_field):
    folder_path = cmds.textField(folder_path_field, q=True, text=True)
    if not os.path.exists(folder_path):
        cmds.warning('Folder does not exist')
        return

    systems = [f[:-4] for f in os.listdir(folder_path) if f.endswith('.txt')]

    for menu_name in ['origMenu', 'targetMenu']:
        if cmds.optionMenu(menu_name, exists=True):
            items = cmds.optionMenu(menu_name, q=True, itemListLong=True) or []
            for item in items:
                cmds.deleteUI(item)
            for sys in systems:
                cmds.menuItem(label=sys, parent=menu_name)

    # Set default target to 'Plask' if available after refresh
    target_items = cmds.optionMenu('targetMenu', q=True, itemListLong=True) or []
    target_labels = [cmds.menuItem(item, q=True, label=True) for item in target_items]
    if 'Plask' in target_labels:
        cmds.optionMenu('targetMenu', e=True, v='Plask')

def apply_rename(folder_path_field):
    folder_path = cmds.textField(folder_path_field, q=True, text=True)
    orig_system = cmds.optionMenu('origMenu', q=True, v=True)
    target_system = cmds.optionMenu('targetMenu', q=True, v=True)
    rename_bones(folder_path, orig_system, target_system)

# Automatically show the UI when the script is executed
show_ui()