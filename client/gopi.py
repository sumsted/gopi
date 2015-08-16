import time

from client.gopigo_client import *


def scan():
    servo(30)
    for i in range(24):
        angle = 30+(i*5)
        print angle
        servo(angle)
        print us_dist(0)
    servo(90)


def fb():
    fwd()
    time.sleep(5)
    bwd()
    time.sleep(5)
    stop()


def delay():
    time.sleep(2)


def dance():
    fwd()
    delay()
    left_rot()
    delay()
    bwd()
    delay()
    right_rot()
    delay()
    right()
    delay()
    fwd()
    delay()
    left()
    delay()
    fwd()
    delay()
    stop()


def main():
    dance()

if __name__ == '__main__':
    main()
