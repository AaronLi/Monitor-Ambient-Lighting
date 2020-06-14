import threading

import cv2
import mss
import numpy as np
from pygame import *

sct = mss.mss()

running = True

screen = display.set_mode((sct.monitors[0]['width']//2, sct.monitors[0]['height']//2))

screenshot = None

ready_next_frame = threading.Event()


def grab_and_store_screenshot():
    global screenshot, sct, running
    while running:
        screenshot = np.array(sct.grab(sct.monitors[0]))[:, :, :3]
        ready_next_frame.clear()
        ready_next_frame.wait()


image_grabber = threading.Thread(target=grab_and_store_screenshot)
image_grabber.start()
clockity = time.Clock()
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    if screenshot is None:
        continue
    captured_screenshot = screenshot
    ready_next_frame.set()
    captured_screenshot = cv2.cvtColor(cv2.resize(captured_screenshot, (captured_screenshot.shape[1] // 64, captured_screenshot.shape[0] // 64)),
                              cv2.COLOR_BGR2RGB)

    out = captured_screenshot


    out_image = transform.flip(transform.rotate(surfarray.make_surface(out), -90), True, False)

    screen.blit(transform.scale(out_image, screen.get_size()), (0, 0))
    clockity.tick(15)
    display.flip()

    display.set_caption(f'FPS: {clockity.get_fps():.2f}')

quit()