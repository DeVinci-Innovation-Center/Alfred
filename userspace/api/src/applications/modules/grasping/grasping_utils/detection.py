from dataclasses import dataclass, field
from functools import singledispatchmethod
from typing import List

from ..yolov5.models.common import DetectMultiBackend


class CustomDetectMultiBackend(DetectMultiBackend):
    """DetectMultiBackend with weights path reference."""

    def __init__(self, weights="yolov5s.pt", device="cuda", dnn=True):
        super().__init__(weights, device, dnn)

        self.weights = weights


@dataclass
class DetectFlag:
    """Detection target and associated flag. Works if either target name
    or id is provided."""

    names: List[str]
    target_name: str = ""
    target_id: int = -1
    flag: bool = False

    def __post_init__(self):
        if self.target_name == "" and self.target_id == -1:
            return

        if self.target_name == "":
            self.change_target(self.target_id)

        if self.target_id == -1:
            self.change_target(self.target_name)

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
        """Set flag to False."""

        self.flag = False

    def toggle(self, validate=True):
        """Toggle flag. target_name or target_id must be set before calling
        this fuction if validate is True (default)."""

        if self:
            self.unset()
        else:
            self.set(validate)

    def reset_target(self):
        """Set flag to follow no target."""

        self.target_id = -1
        self.target_name = ""

    @singledispatchmethod
    def change_target(self, new_target: int):
        """Change flag target by id (position in self.names list).
        Automatically sets target_name."""

        if new_target == -1:
            self.target_id = -1
            self.target_name = ""

        self.target_id = new_target
        self.target_name = self.names[self.target_id]

        self.unset()

    @change_target.register
    def _(self, new_target: str):
        """Change flag target by name.
        Automatically sets target_id. (position in self.names list)."""

        if new_target == "":
            self.target_id = -1
            self.target_name = ""

        self.target_name = new_target
        self.target_id = self.names.index(self.target_name)

        self.unset()
