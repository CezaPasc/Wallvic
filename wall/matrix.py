import logging
from rpi_ws281x import PixelStrip, Color

LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0     # set to '1' for GPIOs 13, 19, 41, 45 or 53


def generate_matrix(rows=38, length=11):
    matrix = []

    current = 0
    for row in range(0, rows):
        single_row = range(current, current+length)
        single_row = [i for i in single_row]
        if len(single_row) != length:
            diff = length - len(single_row)
            to_add = range(max(single_row)+1, max(single_row) + diff + 1)
            single_row.extend(to_add)

        even = (len(matrix) % 2 == 0)
        single_row = single_row if even else reversed(single_row)
        single_row = list(single_row)
        matrix.append(single_row)

        current = max(single_row) + 1

    return list(reversed(matrix))


class Matrix():

    def __init__(self, led_count, rows, length, pin, dead_pixels=[], freq=LED_FREQ_HZ, led_dma=LED_DMA, led_invert=LED_INVERT, led_brightness=LED_BRIGHTNESS, led_channel=LED_CHANNEL, inverted=True):
        self.inverted = inverted
        self.strip = PixelStrip(led_count, pin, freq, led_dma, led_invert, led_brightness, led_channel)
        self.strip.begin()

        self.led_count = led_count
        self.rows = rows
        self.length = length
        self.dead_pixels = dead_pixels

        self.matrix = self.generate_matrix()
        self.clear()

    def clear(self):
        [self.strip.setPixelColor(i, Color(0,0,0)) for i in range(0, self.led_count)]
        self.strip.show()
        

    def generate_matrix(self):
        matrix = []

        current = 0
        for row in range(0, self.rows):
            single_row = range(current, current+self.length)
            single_row = [i for i in single_row if i not in self.dead_pixels]
            if len(single_row) != self.length:
                diff = self.length - len(single_row)
                to_add = range(max(single_row)+1, max(single_row) + diff + 1)
                single_row.extend(to_add)

            even = (len(matrix) % 2 == 0)
            single_row = single_row if even else reversed(single_row)
            single_row = list(single_row)
            matrix.append(single_row)

            current = max(single_row) + 1

        return list(reversed(matrix))

    def set_pixel(self, x, y, color):
        if not self.inverted:
            x, y = y, x
        pixel_number = self.matrix[x][y]
        # Red and green are switched on the strip
        r, g, b  = color
        logging.debug("Set led %d to %s" % (pixel_number, Color(g,r,b)))
        self.strip.setPixelColor(pixel_number, Color(*color))
        self.strip.show()



if __name__ == "__main__":
    leds = Matrix(400, 38, 11, 18, dead_pixels=[61])
    for row in leds.matrix:
        print(row)