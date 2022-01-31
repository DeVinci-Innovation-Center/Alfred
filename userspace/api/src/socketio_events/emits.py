from socketio_events.types import Config, News, Pose, Status
from src.utils.global_instances import sio


def send_arm_pose(pose: Pose):
    sio.emit("arm_pose", data=pose.to_dict())


def send_return_configuration(config: Config):
    sio.emit("return-configuration", config.to_dict())


def send_task_news(news: News):
    sio.emit("task-news", news.to_dict())


def send_status_change(new_status: Status):
    sio.emit("status-change", repr(new_status))
