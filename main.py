import RPi.GPIO as GPIO
import serial
import time
import requests

GPIO.setmode(GPIO.BCM);
MAGNET_GPIO = 0
GPIO.setup(MAGNET_GPIO, GPIO.IN);
GPIO.setup(2, GPIO.OUT)
p = GPIO.PWM(2, 200)
p.start(70)

firstnoteKey = requests.get('http://192.168.49.15:8000/api/note')
firstnoteData = firstnoteKey.json()
note = firstnoteData['name']


def playNote():
    p.stop()
    GPIO.output(7, True)
    GPIO.output(2, True)
    time.sleep(0.001)
    p.start(100)
    p.ChangeDutyCycle(90)
    p.ChangeFrequency(freq)
    time.sleep(1)
    print("Done")

def setValue(val):
    global note
    valueChanged = note != val
    #     if valueChanged:
    #         preFunction()
    note = val
    if valueChanged:
        playNote()


while 1:
    key = requests.get('http://192.168.49.15:8000/api/note')

    if GPIO.input(MAGNET_GPIO) == 1:
        if (key):
            data = key.json()
            setValue(data['name'])
            freq = data['frequency']
            print(note, freq)
        else:
            print('data fail')
        print(GPIO.input(MAGNET_GPIO));

    elif GPIO.input(MAGNET_GPIO) == 0:
        print(GPIO.input(MAGNET_GPIO));
        p.ChangeFrequency(0.1)

