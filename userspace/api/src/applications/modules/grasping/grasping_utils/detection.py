from dataclasses import dataclass
from functools import singledispatchmethod
from pathlib import Path

import torch

from ..yolov5.models.common import DetectMultiBackend
from ..yolov5.utils.general import check_suffix


class CustomDetectMultiBackend(DetectMultiBackend):
    """DetectMultiBackend with weights path reference."""

    def __init__(self, weights="yolov5s.pt", device="cuda", dnn=True):
        super().__init__(weights, device, dnn)

        self.weights = weights


@dataclass
class DetectFlag:
    """Detection target and associated flag. Works if either target name
    or id is provided."""

    target_name: str = ""
    target_id: int = -1
    flag: bool = False

    def __bool__(self):
        return self.flag

    def set(self, validate=True):
        """Sets flag. target_name or target_id must be set before calling
        this fuction if validate is True (default)."""

        if validate and (self.target_name == "" and self.target_id == -1):
            raise ValueError(
                "target_name or target_id must be set before setting flag."
            )

        self.flag = True

    def unset(self):
        self.flag = False

    def toggle(self):
        self.flag = not self.flag

    @singledispatchmethod
    def change_target(self, new_target: int):
        self.target_id = new_target
        self.target_name = ""

        self.unset()

    @change_target.register
    def _(self, new_target: str):
        self.target_name = new_target
        self.target_id = -1

        self.unset()
