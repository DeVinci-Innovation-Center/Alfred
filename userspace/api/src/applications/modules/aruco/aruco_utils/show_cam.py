import cv2
import cv2.aruco as aruco
import numpy as np
import threading

from typing import Any

_lock = threading.Lock()


class ShowThread(threading.Thread):
    """Thread to show the camera stream"""
    def __init__(self, is_aruco: bool = False, mtx: Any = None, dist: Any = None, rvec: Any = None, tvec: Any = None, cornes: np.array = None, ids: np.array = None) -> None:
        super().__init__()
        self.frame = None
        self._stop = threading.Event()
        if is_aruco:
            self.is_aruco = is_aruco
            self.mtx = mtx
            self.dist = dist
            self.rvec = rvec
            self.tvec = tvec
            self.corners = cornes
            self.ids = ids

    def run(self):
        """Show the camera stream on a window. If the window is closed, the thread is stopped."""
        while True:
            if self._stop.is_set():
                break
            if self.is_aruco & (np.all(self.ids is not None)):
                aruco.drawDetectedMarkers(self.frame, self.corners, self.ids)
                aruco.drawAxis(self.frame, self.mtx, self.dist,
                               self.rvec, self.tvec, length=0.01)
            if self.frame is not None:
                cv2.imshow("FRAME", self.frame)

                cv2.waitKey(1)
                if (cv2.getWindowProperty("FRAME", cv2.WND_PROP_VISIBLE) < 1):  # if window is closed
                    self._stop.set()
                    cv2.destroyAllWindows()

    def update(self, new_frame: np.array, new_rvec: Any = None, new_tvec: Any = None, new_cornes: np.array = None, new_ids: np.array = None)->None:
        """Update the frame to show"""
        with _lock: # block the running thread during the update
            self.frame = new_frame
            if self.is_aruco:
                self.rvec = new_rvec
                self.tvec = new_tvec
                self.corners = new_cornes
                self.ids = new_ids

    def stop(self)->None:
        """Stop the thread"""
        self._stop.set()
