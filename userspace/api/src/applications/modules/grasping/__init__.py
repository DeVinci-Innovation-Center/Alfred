import sys
from pathlib import Path

FILE = Path(__file__).resolve()
YOLOV5_ROOT = FILE.parents[0] / "yolov5"  # YOLOv5 root directory
if str(YOLOV5_ROOT) not in sys.path:
    sys.path.append(str(YOLOV5_ROOT))  # add ROOT to PATH
