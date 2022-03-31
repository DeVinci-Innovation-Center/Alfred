import threading
import time
from pathlib import Path

import libalfred
import numpy as np
import torch
from libalfred.utils import camera_stream

from . import inference
from .grasping_utils.detection import CustomDetectMultiBackend, DetectFlag
from .grasping_utils.general import _preds_postprocessor

# from .yolov5 import detect
from .yolov5.utils.general import LOGGER

FILE = Path(__file__).resolve()
# WEIGHTS_PATH = (FILE / "../trained_weights/custom.pt").resolve()
WEIGHTS_PATH = (FILE / "../trained_weights/yolov5n.pt").resolve()

LOGGER.setLevel("ERROR")


def main():
    device_name = "cuda" if torch.cuda.is_available() else "cpu"

    api = libalfred.AlfredAPI()
    cam_stream = camera_stream.StreamCamThread(daemon=True)
    cam_stream.start()
    while not cam_stream.frame_ready:
        time.sleep(0.01)
    frame: np.ndarray = cam_stream.get_frame()
    # print(frame)

    # Load model
    model = CustomDetectMultiBackend(WEIGHTS_PATH, device=device_name)
    model.to(torch.device(device_name))
    stride, names, pt, jit, onnx = (
        model.stride,
        model.names,
        model.pt,
        model.jit,
        model.onnx,
    )

    print(f"recognizing classes: {', '.join(names)}")
    detect_flag = DetectFlag("cup")

    img_size = frame.shape
    preds_postprocessor = _preds_postprocessor(
        img_size, names, detect_flag, api
    )

    inference_thread = threading.Thread(
        target=inference.run,
        args=(model, cam_stream, img_size),
        kwargs={
            "pred_postprocessor": preds_postprocessor,
            "line_thickness": 2,
        },
        daemon=True,
    )
    inference_thread.start()

    inference_thread.join()


if __name__ == "__main__":
    main()
