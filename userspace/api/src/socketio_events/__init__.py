import logging

logger = logging.getLogger("uvicorn.error")


def register_routes():
    import src.socketio_events.routes

    logger.info("Registered socketio routes.")
