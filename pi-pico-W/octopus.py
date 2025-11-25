# pyright: ignore[reportMissingImports]
# pylance: ignore[reportMissingImports]

import time
time.sleep(0.1) # Wait for USB to become ready

version_number = 0.0

from machine import Pin, PWM
import utime
import math

# Helper function to create a PWM object for an LED on a specified pin
def create_led(pin):
    led = PWM(Pin(pin))
    led.freq(1000)  # Set a common frequency for PWM
    return led

# Define LEDs by colors
leds = {
    'led1_red': create_led(16),
    'led1_green': create_led(17),
    'led1_blue': create_led(18),
    'led2_red': create_led(15),
    'led2_green': create_led(14),
    'led2_blue': create_led(13)
}

# Pre-calculate the duty values for a full sine wave cycle
sine_duties = [int((1 - (math.sin(math.radians(i)) + 1) / 2) * 65535) for i in range(360)]

# Initialize current positions for all LEDs
current_positions = {led: 0 for led in leds}

# Define the rate table
rate_table = [
    {key: 1 if 'red' in key else 2 if 'green' in key else 4 for key in leds},
    {key: 2 if 'red' in key else 4 if 'green' in key else 1 for key in leds},
    {key: 4 if 'red' in key else 1 if 'green' in key else 2 for key in leds}
]

# Function to apply fading based on sine wave duties
def apply_fade(led, tick_count):
    if tick_count % rate_table[rate_index][led] == 0:
        leds[led].duty_u16(sine_duties[current_positions[led]])
        current_positions[led] = (current_positions[led] + 1) % len(sine_duties)

# globals 
tick_count = 0
rate_index = 0

def next_fade(): 
    global tick_count
    global rate_index  
    for led in leds:
        apply_fade(led, tick_count)
    
    tick_count += 1
    if tick_count % 1000 == 0:  # Change rate configuration periodically
        rate_index = (rate_index + 1) % len(rate_table)
    utime.sleep(0.01)

def main():
    print("Octopus V",version_number)
    while True :
        next_fade()

if __name__ == '__main__':
    main()
