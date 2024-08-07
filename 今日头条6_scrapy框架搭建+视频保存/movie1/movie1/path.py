# 导入YOLO代码的路径，保证begin.py可以import
import os
import sys

# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)

# 计算要导入文件的绝对路径
current_script_dir = os.path.dirname(current_script_path)
target_module_path = os.path.join(current_script_dir, r'../../../目标识别/YOLOV8/ultralytics-main/ultralytics-main/ultralytics/__init__.py')
target_module_dir = os.path.dirname(target_module_path)

# 将目标模块的目录添加到sys.path中
if target_module_dir not in sys.path:
    sys.path.insert(0, target_module_dir)