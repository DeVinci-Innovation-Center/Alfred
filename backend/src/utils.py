import multiprocessing
from typing import Callable


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
    current_process: multiprocessing.Process
    current_app: Callable
    current_app_args: tuple
    current_app_kwargs: dict

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.is_app_running = False
        self.current_process = None

    def __bool__(self):
        """Returns True if a process is running, else False."""

        if self.current_process is None:
            return False

        self.current_process.join(0)
        thread_status = self.current_process.is_alive()
        return thread_status

    def run_app(self, app: Callable, *args, **kwargs):
        """Spawn a thread running provided app."""

        if self.__bool__():
            raise AppRunningException()

        self.current_app = app  # type: ignore
        self.current_app_args = args
        self.current_app_kwargs = kwargs

        self.current_process = multiprocessing.Process(
            target=app, args=args, kwargs=kwargs
        )

        self.current_process.start()
        self.is_app_running = True

    def stop_app(self):
        """Stop current running app."""

        if self.__bool__():
            raise NoAppRunningException()

        self.current_process.terminate()
        self.current_process = None
        self.is_app_running = False


ctx_manager = ContextManager()
