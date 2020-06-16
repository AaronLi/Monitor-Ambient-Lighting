import json
class LedConfiguration:
    def __init__(self, diagonal, led_count, monitor_number, led_order, led_density, bezels) -> None:
        super().__init__()

        self.monitor_diagonal = diagonal

        self.led_count = led_count

        self.monitor_number = monitor_number

        self.led_order = led_order

        self.led_density = led_density

        self.bezels = bezels

    def __repr__(self)-> str:
        return f'Monitor Number: {self.monitor_number} '\
               f'Diagonal: {self.monitor_diagonal} ' \
               f'LED Count: {self.led_count} ' \
               f'LED Order: {self.led_order} ' \
               f'LED Density: {self.led_density}'


class LightingSetup:

    def __init__(self, monitor_configurations):
        self.monitor_configurations = monitor_configurations

    @staticmethod
    def load(path):
        configurations = []
        with open(path) as f:
            data = json.load(f)
            monitor_data = data['monitor_configuration']

            for monitor in monitor_data:
                number = monitor['monitor']
                led_order = monitor.get('led_order')
                diagonal_size = monitor.get('diagonal_size')
                led_count = monitor.get('led_count')
                leds_per_inch = monitor.get('leds_per_inch')
                bezels = monitor.get('bezel_thickness')

                config_out = LedConfiguration(diagonal_size, led_count, number, led_order, leds_per_inch, bezels)

                configurations.append(config_out)

        return LightingSetup(configurations)

if __name__ == '__main__':
    configs = LightingSetup.load('../monitor_configuration.json')

    print(configs)