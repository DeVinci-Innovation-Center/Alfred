import threading
import time
from pathlib import Path

_lock = threading.Lock()

import torch
import libalfred

from . import inference
from .grasping_utils.detection import CustomDetectMultiBackend, DetectFlag
from .grasping_utils.general import _preds_postprocessor
from .yolov5 import detect
from .yolov5.utils.general import LOGGER

FILE = Path(__file__).resolve()
# WEIGHTS_PATH = (FILE / "../trained_weights/custom.pt").resolve()
WEIGHTS_PATH = (FILE / "../trained_weights/yolov5l-runtime.pt").resolve()
# WEIGHTS_PATH = (FILE / "../trained_weights/yolov5l.onnx").resolve()
VIDEO_SOURCE = 4

LOGGER.setLevel("ERROR")


def main(device_name: str = "cuda"):
    api = libalfred.AlfredAPI()

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

    print(names)
    detect_flag = DetectFlag(target_name="cup")

    img_size = inference.get_img_size(VIDEO_SOURCE)
    preds_postprocessor = _preds_postprocessor(img_size, names, detect_flag, api)

    inference_thread = threading.Thread(
        target=inference.run,
        args=(model, VIDEO_SOURCE),
        kwargs={"pred_postprocessor": preds_postprocessor, "line_thickness": 2},
        daemon=True,
    )
    inference_thread.start()

    # while inference_thread.is_alive():
    #     time.sleep(4)
    #     with _lock:
    #         detect_flag.change_target("cube")

    #     time.sleep(4)
    #     with _lock:
    #         detect_flag.change_target("boule")

    inference_thread.join()

    # custom inference function
    # inference.run(
    #     model, VIDEO_SOURCE, pred_postprocessor=preds_postprocessor, half=False
    # )

    # yolov5 base inference function
    # detect.run(
    #     weights=WEIGHTS_PATH,  # model.pt path(s)
    #     source=VIDEO_SOURCE,  # file/dir/URL/glob, 0 for webcam
    #     imgsz=[480, 640],  # inference size (pixels)
    #     conf_thres=0.50,  # confidence threshold
    #     iou_thres=0.45,  # NMS IOU threshold
    #     max_det=1000,  # maximum detections per image
    #     device="0",  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    #     view_img=True,  # show results
    #     save_txt=False,  # save results to *.txt
    #     save_conf=False,  # save confidences in --save-txt labels
    #     save_crop=False,  # save cropped prediction boxes
    #     nosave=False,  # do not save images/videos
    #     classes=None,  # filter by class: --class 0, or --class 0 2 3
    #     agnostic_nms=False,  # class-agnostic NMS
    #     augment=False,  # augmented inference
    #     visualize=False,  # visualize features
    #     update=False,  # update all models
    #     exist_ok=False,  # existing project/name ok, do not increment
    #     line_thickness=3,  # bounding box thickness (pixels)
    #     hide_labels=False,  # hide labels
    #     hide_conf=False,  # hide confidences
    #     half=False,  # use FP16 half-precision inference
    #     dnn=False,  # use OpenCV DNN for ONNX inference
    # )


if __name__ == "__main__":
    main()
