"""Handle Applications in the context of ALFRED. Contains the Application
class, Exceptions and the ContextManager for managing applications in the
system."""

from ctypes import c_bool
import multiprocessing
import os
import threading
import time
import traceback
from typing import Callable

import socketio

from src.utils.global_instances import logger


class App(multiprocessing.Process):
    """App to run as sub-process, which doesn't exit program when it encounters
    an exception."""

    def __init__(
        self,
        *args,
        use_sockets: bool = False,
        socket: socketio.Server = None,
        use_pipe: bool = False,
        f_args: tuple = None,
        f_kwargs: dict = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._f_args = f_args if f_args is not None else []
        self._f_kwargs = f_kwargs if f_kwargs is not None else {}

        self.use_sockets = use_sockets
        self.socket = socket

        self.use_pipe = use_pipe

        self.parent_conn, self.child_conn = None, None
        if self.use_pipe:
            self.parent_conn, self.child_conn = multiprocessing.Pipe()

        self._running = multiprocessing.Value(c_bool, False)

    @property
    def running(self) -> bool:
        with self._running.get_lock():
            ret = self._running.value

        return ret

    def run(self):
        try:
            logger.info("starting app with target: %s", repr(self._target))
            with self._running.get_lock():
                self._running.value = True

            try:
                if self.use_pipe:
                    self._target(self.child_conn, *self._f_args, **self._f_kwargs)
                else:
                    self._target(*self._f_args, **self._f_kwargs)

            except Exception:  # pylint: disable=broad-except
                logger.exception("Exception occured within App:", exc_info=1)

            if self.use_sockets:
                self.socket.emit("app_watcher", "done")

        except Exception:  # pylint: disable = broad-except
            tb = traceback.format_exc()
            logger.exception("Exception occured outside the App:", exc_info=1)

            if self.use_sockets:
                self.socket.emit("app_watcher", {"exception": tb})

        finally:
            logger.info("finished app with target: %s", repr(self._target))
            with self._running.get_lock():
                self._running.value = False

            # kill self to avoid orphaned threads
            os.kill(self.pid, 9)


class AppRunningException(Exception):
    """Exception raised when user tries to run an app when another one is running."""

    message: str

    def __init__(
        self,
        message=(
            "One app is already running. "
            "Backend can't run 2 apps on the same arm at once."
        ),
        app: Callable = None,
    ):

        self.message = message

        if app is not None:
            self.message += " " + f"Running app is: {repr(app)}"

        super().__init__(self.message)


class NoAppRunningException(Exception):
    """Raised when user tries to stop the current app but none is running."""

    message: str

    def __init__(self, message="No app is running."):
        self.message = message

        super().__init__(self.message)


class ContextManager:
    """Manages running apps in backend, to only allow for one app to be
    running at once."""

    _instance = None

    is_app_running: bool
    current_app: App

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.is_app_running = False
        self.current_app = None

    def __bool__(self):
        """Returns True if a process is running, else False."""

        if self.current_app is None:
            return False

        return self.current_app.running

    def run_app(self, app: App):
        """Spawn a thread running provided app."""

        if self.__bool__():
            raise AppRunningException()

        self.current_app = app  # type: ignore

        self.current_app.start()
        self.is_app_running = True

    def stop_app(self):
        """Stop current running app."""

        if not self.__bool__():
            raise NoAppRunningException()

        self.current_app.terminate()
        self.current_app = None
        self.is_app_running = False


ctx_manager = ContextManager()
