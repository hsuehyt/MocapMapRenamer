# MocapMapRenamer

A simple Python-based tool for Autodesk Maya to batch rename mocap skeleton joints from one bone naming system to another.  
Ideal for converting naming conventions (e.g., from **AdvancedSkeleton** to **Plask** or any custom system) using customizable mapping files.

---

## 📸 Snapshot  
![UI Screenshot](https://github.com/hsuehyt/MocapMapRenamer/blob/main/images/Screenshot%202025-03-21%20225603.png)

---

## ✨ Features
- UI integrated directly in Maya's Script Editor
- Browse and select your `moCapMatchers` folder
- Load available bone systems from `.txt` files
- Select target system for renaming  
- Apply batch renaming easily to all joint nodes in the scene  

---

## 📂 Folder Structure
```
MocapMapRenamer/
│
├─ moCapMatchers/         # Contains .txt files for different skeleton systems
├─ images/                # Screenshots and documentation images
├─ Mocap Map Renamer.py   # Main Python script for Maya
├─ LICENSE
└─ README.md
```

---

## ⚙️ How to Use
1. Place the `Mocap Map Renamer.py` and `moCapMatchers` folder in your Maya scripts directory or source them from any location.
2. Run the script in Maya's Script Editor (Python tab).
3. The UI will pop up, allowing you to:
   - Set the `moCapMatchers` directory  
   - Select the **Target Bone System**  
   - Click `Apply Rename` to convert bone names in your scene.

---

## 📝 Creating Custom Mapping Files
- Each `.txt` file inside `moCapMatchers` should contain key-value pairs like:
```
sideRight = R
sideLeft = L
Hips = Pelvis
Spine1 = SpineMid
```
- These determine how each bone will be renamed.

---

## 📜 License
This project is licensed under the MIT License.