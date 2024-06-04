# Garbage-Classification-Picking-Robot

Robby is a robot designed to identify, move towards, and pick up trash using a Raspberry Pi, ultrasonic sensor, camera, and servo motor. It uses a pre-trained garbage classification model from Hugging Face for image recognition.

## Table of Contents

- [Introduction](#introduction)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Future Improvements](#future-improvements)
- [Acknowledgements](#acknowledgements)

## Introduction

Robby is a robotic project aimed at automating the process of identifying and picking up trash. It uses a camera to capture images, an ultrasonic sensor to measure distance, and a pre-trained machine learning model to classify the captured images. If trash is detected, Robby moves towards it and picks it up.

## Hardware Requirements

- Raspberry Pi (with Raspbian OS)
- PiCamera
- Ultrasonic Sensor (HC-SR04)
- Servo Motor
- Motor Driver (L298N or equivalent)
- DC Motors for wheels
- Jumper wires
- Breadboard

## Software Requirements

- Python 3
- RPi.GPIO library
- requests library
- picamera library
- Pillow library

## Installation

1. **Set up the Raspberry Pi:**
   - Install Raspbian OS on your Raspberry Pi.
   - Ensure your Raspberry Pi is connected to the internet.

2. **Install required Python libraries:**
   ```sh
   pip install RPi.GPIO requests picamera pillow

## Usage
1. **Wiring:**

  -Connect the ultrasonic sensor to the GPIO pins as defined in the code (TRIG to pin 38, ECHO to pin 36).
  -Connect the servo motor to GPIO pin 12.
  -Connect the motor driver to the Raspberry Pi and DC motors.

2. **Run the script:**
  ```sh
  python robby.py
 ```
3. **Clone this repository:**
  ```sh
  git clone <repository-url>
  cd <repository-directory>
  ```

## Code Explanation

The robby.py script initializes the robot, sets up the GPIO pins, and defines the following functions:

-forward(sec): Moves the robot forward for a specified number of seconds.
-backward(sec): Moves the robot backward for a specified number of seconds.
-lturn(sec): Turns the robot left for a specified number of seconds.
-rturn(sec): Turns the robot right for a specified number of seconds.
-pick(): Controls the servo motor to pick up the trash.
-get_distance(): Measures the distance to an object using the ultrasonic sensor.
-query_image(image): Sends the captured image to the Hugging Face API for classification.
-capture_image(): Captures an image using the PiCamera.

The main loop captures an image, classifies it, checks the distance to the nearest object, and decides whether to move towards the trash or take a random turn.

## Future Improvements
-Implement better navigation algorithms to avoid obstacles more efficiently.
-Integrate a more sophisticated trash collection mechanism.
-Enhance the image classification model for higher accuracy.

## Acknowledgements
-The pre-trained garbage classification model is provided by Hugging Face.
-Inspired by various robotics and machine learning projects available online.

## License
-This project is licensed under the MIT License - see the LICENSE file for details.

