import enum
import math
import cv2

from lib import led_configuration


class EdgeLighting:
    """
    EdgeLighting. Will take image data from screenshots and their respective monitor's information and give the list of
    colours that need to be outputted to the LED's
    """
    _direction_change = {
            "U": (0, -1),
            "L": (-1, 0),
            "D": (0, 1),
            "R": (1, 0)
        }

    _extended_name = {
        "U" : "up",
        "L" : "left",
        "D" : "down",
        "R" : "right",
        "T" : "top",
        "B" : "bottom"
    }

    class SIDE(enum.Enum):
        TOP = "T"
        LEFT = "L"
        BOTTOM = "B"
        RIGHT = "R"

        @property
        def extended_name(self):
            return EdgeLighting._extended_name[self.value]

    class DIRECTION(enum.Enum):
        UP = "U"
        LEFT = "L"
        DOWN = "D"
        RIGHT = "R"

        @property
        def pixel_change(self):
            return EdgeLighting._direction_change[self.value]

    def __init__(self, lighting_configurations: led_configuration.LightingSetup, monitor_info) -> None:
        """

        :param lighting_configurations: A LightingSetup object containing all of the information about how the lights
            should be configured
        :param monitor_info: A list of dictionaries with the dimensions of the monitors stored
            with the keys 'width' and 'height'
        """
        self.lighting_configurations = lighting_configurations

        self.led_positions = []

        for configuration, monitor_resolution in zip(lighting_configurations.monitor_configurations, monitor_info):
            bezel_diagonal = math.hypot(configuration.bezels['top'] + configuration.bezels['bottom'],
                                        configuration.bezels['left'] + configuration.bezels['right'])

            diagonal_length = configuration.monitor_diagonal + bezel_diagonal

            pixel_diagonal = math.hypot(monitor_resolution['width'], monitor_resolution['height'])

            monitor_pixel_ratio = diagonal_length / pixel_diagonal # inches per pixel

            pixels_per_led = (1/monitor_pixel_ratio) * configuration.led_density

            monitor_width = monitor_pixel_ratio * monitor_resolution['width']
            monitor_height = monitor_pixel_ratio * monitor_resolution['height']

            for strip_segment_index in range(len(configuration.led_order)//2):
                strip_side = EdgeLighting.SIDE(configuration.led_order[strip_segment_index*2])
                strip_direction = EdgeLighting.DIRECTION(configuration.led_order[strip_segment_index * 2 + 1])

                pX, pY = EdgeLighting.get_starting_position(strip_side, strip_direction, monitor_resolution)

                dX, dY = strip_direction.pixel_change

                dX *= pixels_per_led
                dY *= pixels_per_led

                for pixel_index in range(configuration.led_count[strip_side.extended_name]):
                    pixel_x = int(pX + dX * pixel_index)
                    pixel_y = int(pY + dY * pixel_index)
                    if pixel_x not in range(monitor_resolution['width']) or pixel_y not in range(monitor_resolution['height']):
                        print(strip_side, strip_direction, pixel_x, pixel_y)
                    self.led_positions.append((pixel_x, pixel_y))


    @staticmethod
    def get_starting_position(side: SIDE, direction: DIRECTION, monitor_resolution: dict):
        x_start = 0
        y_start = 0
        if direction == EdgeLighting.DIRECTION.UP:
            y_start = monitor_resolution['height']-1

        elif direction == EdgeLighting.DIRECTION.DOWN:
            y_start = 0

        elif direction == EdgeLighting.DIRECTION.RIGHT:
            x_start = 0

        elif direction == EdgeLighting.DIRECTION.LEFT:
            x_start = monitor_resolution['width'] - 1

        if side == EdgeLighting.SIDE.LEFT:
            x_start = 0
        elif side == EdgeLighting.SIDE.RIGHT:
            x_start = monitor_resolution['width'] - 1
        elif side == EdgeLighting.SIDE.TOP:
            y_start = 0
        elif side == EdgeLighting.SIDE.BOTTOM:
            y_start = monitor_resolution['height'] - 1

        return x_start, y_start


    def update(self, screenshots):
        colours_out = []
        for screenshot in screenshots:
            scaled_screenshot = cv2.resize(screenshot, (screenshot.shape[1]//4, screenshot.shape[0]//4))
            for position_x, position_y in self.led_positions:
                r, g, b = scaled_screenshot[position_y//4, position_x//4]
                colours_out += [b, g, r]


        return colours_out