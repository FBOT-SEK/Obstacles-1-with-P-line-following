#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_A)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)


color = ColorSensor(INPUT_1)
US1 = UltrasonicSensor(INPUT_2)
US2 = UltrasonicSensor(INPUT_3)
US3 = UltrasonicSensor(INPUT_4)

US1.mode = 'US-DIST-CM'
color.mode = 'COL-COLOR'    

ODO = 15/5.6

# Here is where your code starts
def seguidor():
    while True:
        target = 50
        correction = 2
        cs = color.reflected_light_intensity
        error = cs - target
        steering_drive.on((error * correction), 30)

        if US1.distance_centimeters <= 10:
            print("a")
            break

def rotate(grau):
    graus = ODO*grau
    tank_drive.on_for_degrees(-20, 20, graus)
    
def dist_cm(cm):
    perimetro = math.pi*5.6
    andar =  perimetro*cm
    tank_drive.on_for_degrees(20, 20, andar)
    
def segue_parede():
    while US2.distance_centimeters <= 15:
        print(US2.distance_centimeters)
        time.sleep(0.1)
        tank_drive.on(20, 20)
        if color.color == 1:
            dist_cm(7.6)
            rotate()
            break
        
    else:
        dist_cm(10)
        rotate(90)
        dist_cm(20)
        segue_parede()
        
    

while True: #while main
    seguidor()
    time.sleep(0.1)
    rotate(-90)
    
    segue_parede()