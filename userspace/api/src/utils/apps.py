import multiprocessing
import traceback
from typing import Callable

import socketio


class App(multiprocessing.Process):
    """App to run as sub-process, which doesn't exit program when it encounters an exception."""

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

        multiprocessing.Process.__init__(self, *args, **kwargs)

        self._f_args = f_args if f_args is not None else []
        self._f_kwargs = f_kwargs if f_kwargs is not None else {}

        self.use_sockets = use_sockets
        self.socket = socket

        self.use_pipe = use_pipe

        self.parent_conn, self.child_conn = None, None
        if self.use_pipe:
            self.parent_conn, self.child_conn = multiprocessing.Pipe()

    def run(self):
        try:
            print(f"starting app with target: {self._target}")

            try:
                if self.use_pipe:
                    self._target(
                        self.child_conn, *self._f_args, **self._f_kwargs
                    )
                else:
                    self._target(*self._f_args, **self._f_kwargs)
            except Exception:
                print(traceback.format_exc())

            print(f"finished app with target: {self._target}")

            if self.use_sockets:
                self.socket.emit("app_watcher", "done")

        except Exception:  # pylint: disable = broad-except
            tb = traceback.format_exc()
            if self.use_sockets:
                self.socket.emit("app_watcher", {"exception": tb})
            # raise e  # You can still rise this exception if you need to


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
    """Manages running apps in backend, to only allow for one app to be running at once."""

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

        self.current_app.join(0)
        process_status = self.current_app.is_alive()
        return process_status

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
