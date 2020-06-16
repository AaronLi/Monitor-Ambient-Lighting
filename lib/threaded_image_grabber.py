import threading

import mss
import numpy as np

sct = mss.mss()

def monitor_resolutions():
    return sct.monitors

class ThreadedImageGrabber:

    def __init__(self) -> None:
        self.image_grabber = threading.Thread(target=self._grab_and_store_screenshot, name="Screenshot grabber")
        self.monitors = []
        self.ready_next_frame = threading.Event()
        self.__running = threading.Event()

    def start(self):
        self.__running.set()
        self.image_grabber.start()
        return self

    @property
    def is_running(self):
        return self.__running.is_set()

    def stop(self):
        self.__running.clear()

    def pull_frame_and_request_next(self):
        self.ready_next_frame.set()
        return self.monitors

    def _grab_and_store_screenshot(self):
        while self.__running.is_set():
            self.monitors = [np.array(sct.grab(monitor))[:, :, :3] for monitor in sct.monitors[1:]]
            self.ready_next_frame.clear()
            self.ready_next_frame.wait(timeout=0.5)


