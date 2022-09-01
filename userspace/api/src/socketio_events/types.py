from dataclasses import dataclass
from typing import Optional

_possible_statuses: list = ["offline", "online"]


@dataclass
class Pose:
    """ALFRED pose data."""

    joint_pose: list
    head_data: Optional[dict] = None

    def __post_init__(self):
        if self.head_data is None:
            self.head_data = {"equipment": None}

    def to_dict(self):
        return {
            "joint_1": self.joint_pose[0],
            "joint_2": self.joint_pose[1],
            "joint_3": self.joint_pose[2],
            "joint_4": self.joint_pose[3],
            "joint_5": self.joint_pose[4],
            "joint_6": self.joint_pose[5],
            "head": self.head_data,
        }


@dataclass
class Config:
    """ALFRED global configuration object class."""

    def to_dict(self):
        return {}


@dataclass
class News:
    """ALFRED task news."""

    def to_dict(self):
        return {}


@dataclass
class Status:
    """ALFRED status to be shown on dashboard."""

    status: str
    current_application: Optional[str] = None

    def __post_init__(self):
        if self.status not in _possible_statuses:
            raise ValueError(
                f"status '{self.status}' not in possible statuses: "
                f"{_possible_statuses}",
            )

    def __str__(self):
        if self.status != "online" or self.current_application is None:
            return f"{self.status}"

        return f"{self.status}: {self.current_application}"
