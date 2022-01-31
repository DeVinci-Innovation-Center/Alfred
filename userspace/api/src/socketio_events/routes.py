from src.utils.global_instances import sio

from fastapi.logger import logger


@sio.event
def disconnect(sid):
    logger.info("%s disconnected.", sid)


@sio.event
def connect(sid, environ, auth):
    logger.info("%s connected.", sid)


@sio.on("connect_error")
def print_err(*args):
    print(args)


@sio.on("app_watcher")
def get_app_event(*args):
    print(args)


@sio.on("start-watching-arm-pose")
def start_watching_arm_pose(*_):
    """Toggle on sending arm pose data."""


@sio.on("stop-watching-arm-pose")
def stop_watching_arm_pose(*_):
    """Toggle off sending arm pose data."""


@sio.on("emergence-stop")
def emergency_stop(*_):
    """Emergency stop ALFRED."""


@sio.on("fetch-configuration")
def fetch_configuration(*_):
    """Fetch ALFRED configuration."""


@sio.on("start-task")
def start_task(*_):
    """Start designed task."""


@sio.on("request-equipment-change")
def request_equipment_change(*_):
    """Process equipment change request."""
