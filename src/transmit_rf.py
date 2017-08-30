import time
import sys
import RPi.GPIO as GPIO

a_on = '1110111110101010110011001'
a_off = '1110111110101010110000111'
b_on = '1110111110101010001111001'
b_off = '1110111110101010001100111'
c_on = '1110111110101000111111001'
c_off = '1110111110101000111100111'
d_on = '1110111110100010111111001'
d_off = '1110111110100010111100111'
e_on = '1110111110001010111111001'
e_off = '1110111110001010111100111'
short_delay = 0.000202
long_delay = 0.000576
extended_delay = 0.00568

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 23

def transmit_code(code):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(long_delay)
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(short_delay)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(extended_delay)
    GPIO.cleanup()