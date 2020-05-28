import RPi.GPIO as GPIO
import time
from time import sleep
#set mode board and BCM
GPIO.setmode(GPIO.BCM)

GPIO.setwarning(False)

#set pins
trigger = 14
echo = 15
led = 18
#setup input output
GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(led,GPIO.OUT)

def distance():
    GPIO.output(trigger,False)
    time.sleep(1)
    #check system work
    GPIO.output(trigger, True)

    time.sleep(0.00001)
    GPIO.output(trigger, False)

    while GPIO.input(echo)==0:
        Start = time.time()
    while GPIO.input(echo)==1:
        Stop = time.time()
    #sonic speed * time = the distance, and divide by 2 to calculate the one way trip
    distance = round(((Stop - Start)*34300)/2,2)
    return distance


light = GPIO.PWM(led,50)
light.Start(0)
if __name__ == '__main__':
    try:
        while True:
            echo_distance = distance()*10
            print("Distance is : %.lf cm" % echo_distance)
            if echo_distance < 10:
                for dc in range(60,101,5):
                    light.ChangeDutyCycle(dc)
                    sleep(0.1)
            elif 10 < echo_distance <50:
                for dc in range(40,5,-5):
                    light.ChangeDutyCycle(dc)
                    sleep(0.1)
            else:
                for dc in range(0,1):
                    light.ChangeDutyCycle(dc)
                    sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupt by user")
        light.stop()
        GPIO.cleanup()