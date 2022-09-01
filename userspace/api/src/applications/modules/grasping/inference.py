from pathlib import Path

import cv2
import numpy as np
import torch
from torch.backends import cudnn

from libalfred.utils.camera_stream import StreamCamThread

from .yolov5.models.common import DetectMultiBackend
from .yolov5.utils.augmentations import letterbox

# from .yolov5.utils.datasets import LoadStreams
from .yolov5.utils.general import (
    LOGGER,
    check_img_size,
    check_imshow,
    increment_path,
    non_max_suppression,
    scale_coords,
    strip_optimizer,
    xyxy2xywh,
)
from .yolov5.utils.plots import Annotator, colors, save_one_box
from .yolov5.utils.torch_utils import select_device, time_sync


# pylint: disable=too-many-branches,too-many-statements
def run(
    model: DetectMultiBackend,
    cam_stream: StreamCamThread,  # libalfred cam stream instance
    img_size,  # image shape
    pred_postprocessor=lambda x: x,
    conf_thres=0.25,  # confidence threshold
    iou_thres=0.45,  # NMS IOU threshold
    max_det=1000,  # maximum detections per image
    device="",  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    view_img=True,  # show results
    save_txt=False,  # save results to *.txt
    save_conf=False,  # save confidences in --save-txt labels
    save_crop=False,  # save cropped prediction boxes
    classes=None,  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms=False,  # class-agnostic NMS
    augment=False,  # augmented inference
    visualize=False,  # visualize features
    update=False,  # update all models
    project="/tmp",  # save results to project/name
    name="exp",  # save results to project/name
    exist_ok=True,  # existing project/name ok, do not increment
    line_thickness=3,  # bounding box thickness (pixels)
    hide_labels=False,  # hide labels
    hide_conf=False,  # hide confidences
    half=False,  # use FP16 half-precision inference
):
    """Run inference on cam stream, yield pred results and annotated image.
    Code taken from yolov5 detect.py."""

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / "labels" if save_txt else save_dir).mkdir(
        parents=True, exist_ok=True
    )  # make dir

    # Load model
    device = select_device(device)
    stride, names, pt = (model.stride, model.names, model.pt)

    imgsz = check_img_size(img_size, s=stride)  # check image size

    # Half
    half &= (
        pt and device.type != "cpu"
    )  # half precision only supported by PyTorch on CUDA
    if pt:
        # pylint: disable=expression-not-assigned
        model.model.half() if half else model.model.float()

    # Dataloader
    view_img = check_imshow()
    cudnn.benchmark = True  # set True to speed up constant image size inference

    # Run inference
    if pt and device.type != "cpu":
        model(
            torch.zeros(1, 3, *imgsz[:2]).to(device).type_as(next(model.model.parameters()))
        )  # warmup
    dt, seen = [0.0, 0.0, 0.0], 0
    for path, im0 in cam_stream:
        im0s = [im0]
        # Convert
        ims = [letterbox(im0, img_size, stride=stride, auto=True)[0]]

        # Stack
        im = np.stack(ims, 0)

        # Convert
        im = im[..., ::-1].transpose((0, 3, 1, 2))  # BGR to RGB, BHWC to BCHW
        im = np.ascontiguousarray(im)

        s = ""  # reset text to print per preditction
        t1 = time_sync()
        im_tensor = torch.from_numpy(im).to(device)
        # uint8 to fp16/32
        im_tensor = im_tensor.half() if half else im_tensor.float()
        im_tensor /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im_tensor.shape) == 3:
            im_tensor = im_tensor[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        visualize = (
            increment_path(save_dir / Path(path).stem, mkdir=True)
            if visualize
            else False
        )
        pred = model(im_tensor, augment=augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(
            pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det
        )
        dt[2] += time_sync() - t3

        # Second-stage classifier (optional)
        # pred = \
        # utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1

            p, im0, frame = path[i], im0s[i].copy(), cam_stream.count
            s += f"{i}: "

            p = Path(p)  # to Path
            txt_path = str(save_dir / "labels" / p.stem) + f"_{frame}"
            s += f"{im.shape[2]}x{im.shape[3]}"
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    # add to string
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (
                            (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn)
                            .view(-1)
                            .tolist()
                        )  # normalized xywh
                        line = (
                            (cls, *xywh, conf) if save_conf else (cls, *xywh)
                        )  # label format
                        with open(txt_path + ".txt", "a", encoding="utf-8") as f:
                            f.write(("%g " * len(line)).rstrip() % line + "\n")

                    if save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = (
                            None
                            if hide_labels
                            else (names[c] if hide_conf else f"{names[c]} {conf:.2f}")
                        )
                        annotator.box_label(xyxy, label, color=colors(c, True))
                        if save_crop:
                            save_one_box(
                                xyxy,
                                imc,
                                file=save_dir / "crops" / names[c] / f"{p.stem}.jpg",
                                BGR=True,
                            )

            # Print time (inference-only)
            LOGGER.info("%sDone. (%.3fs)", s, t3 - t2)

            # Stream results
            im0 = annotator.result()
            # if view_img:
            #     cv2.imshow(str(p), im0)
            #     key = cv2.waitKey(1)
            #     if key in [ord("q"), 27]:  # q or escape to quit
            #         cv2.destroyAllWindows()
            #         return

            # Send preds to pred_processor
            yield pred, im0

    # Print results
    t = tuple(x / seen * 1e3 for x in dt)  # speeds per image
    LOGGER.info(
        """Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS"""
        """per image at shape %s""",
        *t,
        (1, 3, *imgsz),
    )

    if update:
        strip_optimizer(model.weights)  # update model (to fix SourceChangeWarning)
