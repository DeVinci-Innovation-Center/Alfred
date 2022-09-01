"""Main file for the grasping application."""

import threading
import time
from multiprocessing.connection import Connection
from pathlib import Path

import cv2
import torch

import libalfred
from libalfred.utils import camera_stream
from src.utils.global_instances import logger

from . import inference
from .grasping_utils.detection import CustomDetectMultiBackend, DetectFlag
from .grasping_utils.general import _preds_postprocessor

# from .yolov5 import detect
from .yolov5.utils.general import LOGGER

FILE = Path(__file__).resolve()
# WEIGHTS_PATH = (FILE / "../trained_weights/custom.pt").resolve()
WEIGHTS_PATH = (FILE / "../trained_weights/yolov5l.pt").resolve()
# WEIGHTS_PATH = (FILE / "../trained_weights/yolov5n.pt").resolve()

LOGGER.setLevel("ERROR")


def watch_conn(conn: Connection, flag: DetectFlag):
    """Watch the connection from multiprocessing and change behavior
    accordingly."""

    while True:
        msg = conn.recv()
        logger.debug("grasping received message: %s", msg)

        if msg[0] == "flag:update":
            flag.change_target(msg[1])


def main(conn: Connection = None, to_grab: str = ""):
    grasping_logger = logger.getChild("grasping")

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
    grasping_logger.debug("recognizing classes: %s", {", ".join(names)})

    detect_flag = DetectFlag(names, target_name=to_grab)
    grasping_logger.debug("detect flag: %s", detect_flag)

    preds_postprocessor = _preds_postprocessor(frame_size, names, detect_flag, api)

    output_generator = inference.run(model, cam_stream, frame_size, line_thickness=2)

    if conn is not None:
        flag_changer_thread = threading.Thread(
            target=watch_conn,
            args=(
                conn,
                detect_flag,
            ),
            daemon=True,
        )
        flag_changer_thread.start()

    grasping_logger.info("Starting processing loop.")
    for pred, im in output_generator:
        preds_postprocessor(pred)

        cv2.imshow("image", im)
        key = cv2.waitKey(1)
        if key in [ord("q"), 27]:  # q or escape to quit
            cv2.destroyAllWindows()
            return

if __name__ == "__main__":
    main()
