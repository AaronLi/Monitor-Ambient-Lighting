import threading

import mss
import numpy as np

sct = mss.mss()

class ThreadedImageGrabber:

    def __init__(self) -> None:
        self.image_grabber = threading.Thread(target=self._grab_and_store_screenshot, name="Screenshot grabber")
        self.screenshot = None
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
        return self.screenshot

    def _grab_and_store_screenshot(self):
        while self.__running.is_set():
            self.screenshot = np.array(sct.grab(sct.monitors[0]))[:, :, :3]
            self.ready_next_frame.clear()
            self.ready_next_frame.wait(0.5)


