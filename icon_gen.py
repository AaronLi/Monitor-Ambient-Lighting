from pygame import *
import math
display.init()
monitor = image.load('monitor.png')
icon = Surface((128, 128), SRCALPHA)

for x in range(icon.get_width()):
    for y in range(icon.get_height()):
        distance = math.hypot(icon.get_width()//2 - x, icon.get_height()//2 - y)
        if distance < icon.get_width()//2:
            angle = math.degrees(math.atan2(icon.get_height()//2 - y, icon.get_width()//2 - x))
            r = int(255 * ((math.sin(math.radians(angle)) + 1) / 2))
            g = int(255 * ((math.sin(math.radians(angle + 120)) + 1) / 2))
            b = int(255 * ((math.sin(math.radians(angle + 240)) + 1) / 2))

            dist_float = min(max(((1 - distance/(icon.get_width()//2))**0.3), 0), 1)

            a = dist_float * 255

            icon.set_at((x, y), (r, g, b, a))

scaled_monitor = transform.scale(monitor, (int(icon.get_width() * 0.8), int(icon.get_height() * 0.8)))

icon.blit(scaled_monitor, ((icon.get_width() - scaled_monitor.get_width())//2, (icon.get_height() - scaled_monitor.get_height())//2))


image.save(icon, "icon.png")