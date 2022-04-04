import threading
import time
from pathlib import Path

import libalfred
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


def main(to_grab: str = ""):
    device_name = "cuda" if torch.cuda.is_available() else "cpu"

    api = libalfred.AlfredAPI()
    cam_stream = camera_stream.StreamCamThread(daemon=True)

    cam_stream.start()
    while cam_stream.frame_size == (0, 0):
        time.sleep(0.01)
    frame_size = cam_stream.frame_size
    # print(frame)

    # Load model
    model = CustomDetectMultiBackend(WEIGHTS_PATH, device=device_name)
    model.to(torch.device(device_name))

    names = model.names
    print(f"recognizing classes: {', '.join(names)}")

    detect_flag = DetectFlag(names, target_name=to_grab)
    print(detect_flag)

    preds_postprocessor = _preds_postprocessor(
        frame_size, names, detect_flag, api
    )

    inference_thread = threading.Thread(
        target=inference.run,
        args=(model, cam_stream, frame_size),
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
