import ast
from socketio_events.types import Config, News, Pose, Status
from utils.global_instances import sio

from libalfred import AlfredAPI

async def background_thread_arm_pose():
    arm = AlfredAPI()
    while True:
        p = arm.get_servo_angle()
        if len(p)>2:
            try:
                pos = ast.literal_eval(p)
                if pos[0]==0:
                    servo_angle = [round(a,2) for a in pos[1][:-1]]
                    #print(servo_angle[:3])
                    await sio.emit("arm_pose",data=servo_angle)
            except:
                continue

        await sio.sleep(0.1)

async def send_arm_pose():
    sio.emit("arm_pose", data=[2,3])


def send_return_configuration(config: Config):
    sio.emit("return-configuration", config.to_dict())


def send_task_news(news: News):
    sio.emit("task-news", news.to_dict())


def send_status_change(new_status: Status):
    sio.emit("status-change", repr(new_status))
