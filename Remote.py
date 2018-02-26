import RPi.GPIO as GPIO
from time import sleep
import hashlib
import json
import os
import requests

url = "https://developer-api.nest.com/devices/thermostats/FSbxP07P7AcQcibDFZtYzrTCvDOd8X7F"

geturl = "https://developer-api.nest.com/devices/thermostats/FSbxP07P7AcQcibDFZtYzrTCvDOd8X7F/target_temperature_f"

token = "c.KDMKhB3e28RftnNKrPqLSfdtsDqUq1ev0CmWz8G3548Ye0JYdK12XX6fsT4qdwawtjDqmRuFfyUcRgLqyYOqklxpMHS1TSEmNdEIUTuRo75RxuNbQk9Se5XRd9yXe6BNsPADCawX1DeyGtnI" # Update with your token

headers = {'Authorization': 'Bearer {0}'.format(token), 'Content-Type': 'application/json'}

GPIO.setmode(GPIO.BCM)

sleepTime = .1

#GPIO Pin of the component
lightPinGreen = 4
buttonUp = 17
lightPinRed = 18
buttonDown = 27

GPIO.setup(lightPinGreen, GPIO.OUT)
GPIO.setup(buttonUp, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lightPinRed, GPIO.OUT)
GPIO.setup(buttonDown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(lightPinGreen, False)
GPIO.output(lightPinRed, False)

def getTemp():
    initial_response = requests.get(geturl, headers=headers, allow_redirects=False)
    if initial_response.status_code == 307:
        initial_response = requests.get(initial_response.headers['Location'], headers=headers, allow_redirects=False)
    return int(initial_response.text)

def sendReq(str):
    curtemp = getTemp()
    
    print(curtemp)
    
    if str=='Up':
        curtemp += 1
    else:
        curtemp -= 1
    
    payload = {"target_temperature_f": curtemp}
    
    initial_response = requests.put(url, headers=headers, data=json.dumps(payload), allow_redirects=False)
    if initial_response.status_code == 307:
        initial_response = requests.put(initial_response.headers['Location'], headers=headers, data=json.dumps(payload), allow_redirects=False)
    print(initial_response.text)

try:
    while True:
        GPIO.output(lightPinGreen, not GPIO.input(buttonUp))
        GPIO.output(lightPinRed, not GPIO.input(buttonDown))
        if(not GPIO.input(buttonUp)):
            sendReq("Up")
            print("pressed up")
            sleep(1)
        if(not GPIO.input(buttonDown)):
            sendReq("Down")
            print("pressed down")
            sleep(1)
        sleep(0.1)
finally:
    GPIO.output(lightPinGreen, False)
    GPIO.output(lightPinRed, False)
    GPIO.cleanup()    
