import maya.cmds as cmds
import os
import re

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
            pattern_r = re.compile(f'{key}_{orig_r}', re.IGNORECASE)
            pattern_l = re.compile(f'{key}_{orig_l}', re.IGNORECASE)
            pattern_m = re.compile(f'{key}_{orig_m}', re.IGNORECASE) if orig_m else None

            replacement = tgt_map.get(key, key)

            if tgt_before:
                rep_r = f'{tgt_r}_' + replacement if tgt_us else f'{tgt_r}{replacement}'
                rep_l = f'{tgt_l}_' + replacement if tgt_us else f'{tgt_l}{replacement}'
                rep_m = f'{tgt_m}_' + replacement if tgt_us else f'{tgt_m}{replacement}' if orig_m else None
            else:
                rep_r = replacement + f'_{tgt_r}' if tgt_us else f'{replacement}{tgt_r}'
                rep_l = replacement + f'_{tgt_l}' if tgt_us else f'{replacement}{tgt_l}'
                rep_m = replacement + f'_{tgt_m}' if tgt_us else f'{replacement}{tgt_m}' if orig_m else None

            new_name = pattern_r.sub(rep_r, new_name)
            new_name = pattern_l.sub(rep_l, new_name)
            if pattern_m:
                new_name = pattern_m.sub(rep_m, new_name)

        if new_name != joint:
            print(f'Renaming {joint} -> {new_name}')
            cmds.rename(joint, new_name)

# The rest of the UI functions remain unchanged...
# show_ui(), browse_folder(), refresh_systems(), apply_rename()

# Automatically show the UI when the script is executed
show_ui()
