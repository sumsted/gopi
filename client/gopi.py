from Queue import Empty
import multiprocessing
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

def check_motors():
    set_speed(200)
    fwd()
    l0 = enc_read(0)
    r0 = enc_read(1)
    print l0, r0
    delay(20)
    stop()
    l1 = enc_read(0)
    r1 = enc_read(1)
    print l1, r1
    l2 = l1 - l0
    r2 = r1 - r0
    print l2, r2, (l2-r2)


def delay(t=2):
    time.sleep(t)


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


def navigate():
    servo(90)
    set_speed(200)
    fwd()
    while True:
        dist = us_dist(0)
        print("dist: %d" % dist)
        checks = 0
        while dist < 15:
            print("Stopping to think about this for a second, dist: %d" % dist)
            stop()
            if checks > 4:
                print("I'm stuck")
                stop()
                exit()
            delay(.2)
            left_rot()
            delay(1)
            stop()
            dist = us_dist(0)
            print("checks: %d, dist: %d" % (checks, dist))
            checks += 1
        if checks > 0:
            print("I'm back on the road, dist: %d" % dist)
            fwd()


def straight_line(speed, enc_dist):
    # servo(90)
    set_speed(speed)
    base_l = latest_l = enc_read(0)
    base_r = latest_r = enc_read(1)
    delta_l = latest_l - base_l
    delta_r = latest_r - base_r
    delta_speed = 0
    print("start - bl: %d, br: %d, dl: %d, dr: %d, ls: %d, rs:%d" % (base_l, base_r, delta_l, delta_r, speed, speed + delta_speed))
    fwd()
    while delta_l < enc_dist:
    # while True:
        delta = delta_l - delta_r
        if delta > 0:
            delta_speed += 20
            set_right_speed(speed + delta_speed)
            print("right slow")
        elif delta < 0:
            delta_speed -= 20
            set_right_speed(speed + delta_speed)
            print("left slow")
        else:
            delta_speed = 0
            set_right_speed(speed)
            print("just right")
        print("dl: %d, dr: %d, d: %d, ls: %d, rs:%d" % (delta_l, delta_r, delta, speed, speed + delta_speed))
        latest_l = enc_read(0)
        latest_r = enc_read(1)
        delta_l = latest_l - base_l
        delta_r = latest_r - base_r

    stop()
    print("stop - bl: %d, br: %d, dl: %d, dr: %d, ls: %d, rs:%d" % (base_l, base_r, delta_l, delta_r, speed, speed + delta_speed))


class MotionChild(multiprocessing.Process):

    def __init__(self, action_queue, results_queue):
        super(MotionChild, self).__init__()
        self.action_queue = action_queue
        self.queue = results_queue

    def run(self):
        current_action = {'direction': 'stop', 'speed': 0, 'right_padding': 0}
        set_speed(current_action['speed'])
        base_l = latest_l = enc_read(0)
        base_r = latest_r = enc_read(1)
        delta_l = latest_l - base_l
        delta_r = latest_r - base_r
        delta_speed = 0

        while True:
            latest_l = enc_read(0)
            latest_r = enc_read(1)
            delta_l = latest_l - base_l
            delta_r = latest_r - base_r

            # capture next action
            try:
                action = self.action_queue.get(True, 3)
                # action = self.action_queue.get(False)
                print("action received %(direction)s, %(speed)d, %(right_padding)d" % action)
                current_action = action
                # Only do this stuff if a new action is received

                # reset the base
                base_l = latest_l = enc_read(0)
                base_r = latest_r = enc_read(1)
                delta_l = latest_l - base_l
                delta_r = latest_r - base_r
                delta_speed = 0

                # set speed
                set_speed(current_action['speed'])

                # start direction
                if current_action['direction'] == 'stop':
                    stop()
                elif current_action['direction'] == 'fwd':
                    fwd()
                elif current_action['direction'] == 'bwd':
                    bwd()
                elif current_action['direction'] == 'end':
                    stop()
                    break
                else:
                    print("wtf")
                    break

            except Empty, e:
                pass
                # print("no action yet")
            # print("current_action: direction: %(direction)s, speed %(speed)d, right_padding: %(right_padding)d" %
            #       current_action)

            # continuously correct, curve determined by padding, positive=right turn, negative=left
            if us_dist(0) < 30:
                print "AAAAHHHHH! EMERGENCY STOP!!!"
                stop()
                return
            diff = 25
            delta = delta_l - (delta_r + current_action['right_padding'])
            if delta > 0:
                # delta_speed = diff if current_action['right_padding'] == 0 else delta_speed + diff
                set_right_speed(current_action['speed'] + delta_speed)
                # print("turning a little left")
            elif delta < 0:
                # delta_speed = -diff
                # delta_speed = diff if current_action['right_padding'] == 0 else delta_speed + diff
                set_right_speed(current_action['speed'] + delta_speed)
                # print("turning a little right")
            else:
                delta_speed = 0
                # set_right_speed(current_action['speed'])
                # print("just right")
            print("dl: %d, dr: %d, d: %d, ls: %d, rs: %d, rp: %d" %
                  (delta_l, delta_r, delta, current_action['speed'], current_action['speed'] + delta_speed,
                  current_action['right_padding']))
        return


    def run2(self):
        current_action = {'direction': 'stop', 'speed': 0, 'right_padding': 0}
        set_speed(current_action['speed'])
        base_l = latest_l = enc_read(0)
        base_r = latest_r = enc_read(1)
        delta_l = latest_l - base_l
        delta_r = latest_r - base_r
        delta_speed = 0

        while True:
            latest_l = enc_read(0)
            latest_r = enc_read(1)
            delta_l = latest_l - base_l
            delta_r = latest_r - base_r

            # capture next action
            try:
                # action = self.action_queue.get(True, 3)
                action = self.action_queue.get(False)
                print("action received %(direction)s, %(speed)d, %(right_padding)d" % action)
                current_action = action
                # Only do this stuff if a new action is received

                # reset the base
                base_l = latest_l = enc_read(0)
                base_r = latest_r = enc_read(1)
                delta_l = latest_l - base_l
                delta_r = latest_r - base_r
                delta_speed = 0

                # set speed
                set_speed(current_action['speed'])

                # start direction
                if current_action['direction'] == 'stop':
                    stop()
                elif current_action['direction'] == 'fwd':
                    fwd()
                elif current_action['direction'] == 'bwd':
                    bwd()
                elif current_action['direction'] == 'end':
                    stop()
                    break
                else:
                    print("wtf")
                    break

            except Empty, e:
                pass
                # print("no action yet")
            # print("current_action: direction: %(direction)s, speed %(speed)d, right_padding: %(right_padding)d" %
            #       current_action)

            # continuously correct, curve determined by padding, positive=right turn, negative=left
            if us_dist(0) < 30:
                print "AAAAHHHHH! EMERGENCY STOP!!!"
                stop()
                return
            diff = 25
            delta = delta_l - (delta_r + current_action['right_padding'])
            if delta > 0:
                # delta_speed = diff if current_action['right_padding'] == 0 else delta_speed + diff
                set_right_speed(current_action['speed'] + delta_speed)
                # print("turning a little left")
            elif delta < 0:
                # delta_speed = -diff
                # delta_speed = diff if current_action['right_padding'] == 0 else delta_speed + diff
                set_right_speed(current_action['speed'] + delta_speed)
                # print("turning a little right")
            else:
                delta_speed = 0
                # set_right_speed(current_action['speed'])
                # print("just right")
            print("dl: %d, dr: %d, d: %d, ls: %d, rs: %d, rp: %d" %
                  (delta_l, delta_r, delta, current_action['speed'], current_action['speed'] + delta_speed,
                  current_action['right_padding']))
        return



def start_motion():
    action_queue = multiprocessing.JoinableQueue()
    results_queue = multiprocessing.Queue()
    motion_child = MotionChild(action_queue, results_queue)
    motion_child.start()

    # print "****** straight"
    # action = {'direction': 'fwd', 'speed': 150, 'right_padding': 0}
    # action_queue.put(action)
    # delay(10)
    # action = {'direction': 'end', 'speed': 0, 'right_padding': 0}
    # action_queue.put(action)
    #
    #
    print "****** straight"
    action = {'direction': 'fwd', 'speed': 150, 'right_padding': 0}
    action_queue.put(action)
    delay(3)
    print "****** right"
    action = {'direction': 'fwd', 'speed': 150, 'right_padding': 10}
    action_queue.put(action)
    delay(3)
    # print "****** straight"
    # action = {'direction': 'fwd', 'speed': 150, 'right_padding': 0}
    # action_queue.put(action)
    # delay(10)
    # print "****** left"
    # action = {'direction': 'fwd', 'speed': 150, 'right_padding': -5}
    # action_queue.put(action)
    # delay(10)
    # print "****** stop"
    # action = {'direction': 'fwd', 'speed': 150, 'right_padding': 0}
    # action_queue.put(action)
    # delay(10)
    action = {'direction': 'end', 'speed': 0, 'right_padding': 0}
    action_queue.put(action)


def main():
    check_motors()

if __name__ == '__main__':
    main()
