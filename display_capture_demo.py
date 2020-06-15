import cv2
from pygame import *

from threaded_image_grabber import sct, ThreadedImageGrabber
print(sct.monitors)
screen = display.set_mode((sct.monitors[0]['width'] // 2, sct.monitors[0]['height'] // 2))

image_grabber = ThreadedImageGrabber().start()

clockity = time.Clock()
while image_grabber.is_running:
    for e in event.get():
        if e.type == QUIT:
            image_grabber.stop()

    captured_screenshots = image_grabber.pull_frame_and_request_next()
    if not captured_screenshots:
        continue
    captured_screenshots = [cv2.cvtColor(
        cv2.resize(captured_screenshot, (captured_screenshot.shape[1] // 64, captured_screenshot.shape[0] // 64)),
        cv2.COLOR_BGR2RGB) for captured_screenshot in captured_screenshots]

    out_image = [transform.flip(transform.rotate(surfarray.make_surface(captured_screenshot), -90), True, False) for captured_screenshot in captured_screenshots]

    for i, screenshot in enumerate(out_image):
        blit_location = ((sct.monitors[i+1]['left'] - sct.monitors[0]['left'])//2, (sct.monitors[i+1]['top'] - sct.monitors[0]['top'])//2)
        print(blit_location)
        screen.blit(transform.scale(screenshot, (sct.monitors[i+1]['width']//2, sct.monitors[i+1]['height']//2)), blit_location)
    clockity.tick(30)
    display.flip()

    display.set_caption(f'FPS: {clockity.get_fps():.2f}')

quit()
