# pylint: disable=invalid-name
import os
import sys
from dataclasses import dataclass
from typing import Optional


def check_config_values(config: dict):
    for conf in config:
        if conf == "ARM_IP" and config["MOVE_ARM"] is False:
            continue
        if config[conf] == "":
            sys.exit(f"Value {conf} was not set but is necessary.")


@dataclass
class Config:
    """Class for global config object."""

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", ""))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", "")
    REDIS_CHANNEL: str = os.getenv("REDIS_CHANNEL", "")

    MOVE_ARM: bool = os.getenv("MOVE_ARM", "") == "True"
    ARM_IP: str = os.getenv("ARM_IP", "")

    ROBOT_DOFS: int = 6
    END_EFFECTOR_INDEX: int = 6
    MAX_SPEED: int = 1000

    def __post_init__(self):
        if self.REDIS_PASSWORD == "":
            self.REDIS_PASSWORD = None


cfg = Config()

check_config_values(cfg.__dict__)
