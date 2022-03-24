from dataclasses import dataclass

import numpy as np


@dataclass
class DetectFlag:
    target_id: int = -1
    flag: bool = False
    corner: np.array=False

    def __bool__(self):
        return self.flag

    def set(self, validate=True):
        """Sets flag. target_id must be set before calling this fuction if validate is True (default)."""

        if validate and self.target_id == -1:
            raise ValueError("target_id must be set before setting flag.")

        self.flag = True

    def unset(self):
        self.flag = False

    def toggle(self):
        self.flag = not self.flag
    
    def update(self,new_corner):
        self.corner=new_corner

    def change_target(self, new_target: int):
        """Change the target_id"""
        self.target_id = new_target
        self.unset()
