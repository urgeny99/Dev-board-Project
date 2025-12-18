import machine
import time
from neopixel import NeoPixel

i2c = machine.I2C(0, scl=machine.Pin(26), sda=machine.Pin(27))
tmp112_address = 0x48

led_pin = machine.Pin(18, machine.Pin.OUT)
num_leds = 1
led_strip = NeoPixel(led_pin, num_leds)

def read_temperature():
    temp_raw = i2c.readfrom_mem(tmp112_address, 0x00, 2)
    temp = (temp_raw[0] << 8 | temp_raw[1]) >> 4
    if temp & 0x800:
        temp -= 4096
    return temp * 0.0625

def set_led_color(temperature):
    if temperature < 15:
        color = (0, 0, 255)
    elif 15 <= temperature <= 25:
        color = (0, 255, 0)
    elif 25 < temperature <= 35:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)
    led_strip[0] = color
    led_strip.write()

while True:
    temperature = read_temperature()
    print(f"Temperature: {temperature:.2f} °C")
    set_led_color(temperature)
    time.sleep(1)