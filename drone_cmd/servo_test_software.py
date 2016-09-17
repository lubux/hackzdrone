import RPi.GPIO as GPIO
import time

PIN = 7
BASE_FREQ = 50

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN ,GPIO.OUT)

p = GPIO.PMW(PIN, BASE_FREQ)

p.start(7.5)

while True:
    p.changeDutyCycle(7.5)
    time.sleep(1)
    p.changeDutyCycle(2)
    time.sleep(1)