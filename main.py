import time
import RPi.GPIO as GPIO
import requests
import io
import picamera
from PIL import Image, ImageDraw, ImageFont
import random
#from gpiozero import AngularServo
from time import sleep
from picamera import PiCamera


GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Ultrasonic sensor pins
TRIG = 38
ECHO = 36

# Motor pins
#servo=AngularServo(18,min_pulse_width=0.0006,max_pulse_width=0.0023)
GPIO.setup(12,GPIO.OUT)
servo1 = GPIO.PWM(12,50)
servo1.start(0)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

#dc = 20
#hz = 10
#pwm = GPIO.PWM(29, hz)

class Robot:
    def __init__(self, name, rwheel, lwheel):
        self.name = name
        self.rwheel = tuple(rwheel)
        self.lwheel = tuple(lwheel)

        self.rwheel_f = int(rwheel[0])
        self.rwheel_b = int(rwheel[1])

        self.lwheel_f = int(lwheel[0])
        self.lwheel_b = int(lwheel[1])

    def forward(self, sec):
        print("Moving Forward")
        GPIO.output(self.rwheel_f, True)
        GPIO.output(self.lwheel_f, True)

        time.sleep(sec)
        GPIO.output(self.rwheel_f, False)
        GPIO.output(self.lwheel_f, False)

    def backward(self, sec):
        print("Moving Backward")
        GPIO.output(self.rwheel_b, True)
        GPIO.output(self.lwheel_b, True)

        time.sleep(sec)
        GPIO.output(self.rwheel_b, False)
        GPIO.output(self.lwheel_b, False)

    def lturn(self, sec):
        print("Moving Left")
        GPIO.output(self.rwheel_f, True)

        time.sleep(sec)
        GPIO.output(self.rwheel_f, False)

    def rturn(self, sec):
        print("Moving Right")
        GPIO.output(self.lwheel_f, True)

        time.sleep(sec)
        GPIO.output(self.lwheel_f, False)


robby = Robot("robby", (29, 32), (33, 31))

# Initialize ultrasonic sensor
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def pick():
    print("Picking up")
    #servo.angle=0
    #sleep(1)
    #servo.angle=90
    #sleep(1)
    #print("picking now")
    #robby.forward(0.25)
    #sleep(2)
    #servo.angle = 0
    #sleep(1)
    servo1.ChangeDutyCycle(2)
    sleep(1)
    servo1.ChangeDutyCycle(7)
    sleep(1)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in cm/s
    distance = round(distance, 2)
    return distance

API_URL = "https://api-inference.huggingface.co/models/yangy50/garbage-classification"
headers = {"Authorization": "Bearer <Your token id>"}


def query_image(image):
    response = requests.post(API_URL, headers=headers, data=image)
    return response.json()


# Capture image from the PiCamera
def capture_image():
    with picamera.PiCamera() as camera:
        # Wait for the camera to warm up
        time.sleep(2)
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        # Rewind the stream ready to read its content
        stream.seek(0)
        return stream.read()

while True:
    servo1.ChangeDutyCycle(2)
    sleep(1)
    image_data = capture_image()
    output = query_image(image_data)
    #camera.capture("/home/monarch/Documents/Soham/capture.jpg")
    #output = query("/home/monarch/Documents/Soham/capture.jpg")
   
    print(output)
    print(output[0]['label'])
    distance = get_distance()
    print("Distance:", distance, "cm")

    # Check if the first label is "trash" with the highest score
    if output[0]['label'] in ['plastic', 'trash', 'paper'] and output[0]['score'] > 0.8:  # Adjust the threshold score as needed
        # Move the robot forward
        print("Trash found")
       
            #print("Distance:", distance, "cm")
        if distance > 5:  # If distance is greater than 5 cm, move towards the trash
            robby.forward(0.25)
        else:  # If distance is less than or equal to 5 cm, stop and wait
            pick()
            print("Too close to move towards the trash")
            time.sleep(2)  # Wait for a moment before taking further action
    else:
        # Check distance to the nearest object
        pick()
        if distance < 5:  # If distance is less than 5 cm, take a random turn
            # Take a random turn
            print("Taking a random turn")
            turn_duration = random.uniform(0.5, 1.5)  # Random duration for turn
            if random.choice([True, False]):
                robby.lturn(turn_duration)
            else:
                robby.rturn(turn_duration)
        else:
            # If no trash is detected and distance is greater than 5 cm, continue moving forward
            print("Continuing forward")
            robby.forward(0.25  )

    # Wait for a moment before capturing the next image
    time.sleep(2)
GPIO.cleanup()
