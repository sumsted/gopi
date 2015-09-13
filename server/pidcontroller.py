from Queue import Empty
import multiprocessing
import time
# from gopigo import *
from client.gopigo_client import *


class PidController(multiprocessing.Process):
    def __init__(self, action_queue, results_queue):
        super(PidController, self).__init__()
        print("time_elapsed, kp, ki, kd, delta_l,delta_r, error_p, error_i, error_d, correction, speed, right_speed")

        self.action_queue = action_queue
        self.results_queue = results_queue

        self.safe_distance = None
        self.current_speed = None
        self.kp = None
        self.ki = None
        self.kd = None
        self.calibration = None
        self.error_i = None
        self.base_l = None
        self.latest_l = None
        self.base_r = None
        self.latest_r = None
        self.start_time = None
        self.last_time = None
        self.last_error_p = None
        self.direction = None
        self._reset()

    def _reset(self):
        # enable_encoders()
        # time.sleep(1)
        self.safe_distance = 15
        self.current_speed = 0
        self.kp = 10
        self.ki = 0
        self.kd = 0
        self.calibration = 0
        self.error_i = 0
        self.base_l = self.latest_l = enc_read(0)
        self.base_r = self.latest_r = enc_read(1)
        self.start_time = self.last_time = self._get_current_milliseconds()
        self.last_error_p = 0
        self.direction = 0


    @staticmethod
    def _get_current_milliseconds():
        return int(round(time.time() * 1000))

    def _tune(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def _set_start_speed(self, speed):
        set_left_speed(speed - 25)
        set_right_speed(speed + 25)
        self.current_speed = speed

    def _set_speed(self, speed):
        set_speed(speed)
        self.current_speed = speed

    def _correction(self):
        latest_l = enc_read(0)
        latest_r = enc_read(1)

        current_time = self._get_current_milliseconds()
        time_elapsed = current_time - self.last_time

        delta_l = (latest_l - self.base_l)
        delta_r = (latest_r - self.base_r)
        error_p = delta_l - delta_r
        self.error_i += int(error_p * time_elapsed / 1000)
        error_d = 0 if time_elapsed == 0 else (error_p - self.last_error_p) / time_elapsed

        correction = self.kp * error_p + self.ki * self.error_i + self.kd * error_d + self.calibration

        print("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d" %
              (time_elapsed, self.kp, self.ki, self.kd, delta_l, delta_r, error_p,
               self.error_i, error_d, correction,
               self.current_speed - int(correction / 2), self.current_speed + int(correction / 2)))

        self.last_error_p = error_p
        self.last_time = current_time

        return correction

    def run(self):
        self._reset()
        action = {'command': 'pass', 'speed': 0}
        while True:
            try:
                action = self.action_queue.get(True, 1)
                # action = self.action_queue.get(False)
                if action['command'] == 'stop':
                    stop()
                    self._reset()
                elif action['command'] == 'fwd':
                    # todo: gradual speed increase
                    self._set_start_speed(action['speed'])
                    fwd()
                    time.sleep(.05)
                    self._reset()
                    self._set_speed(action['speed'])
                elif action['command'] == 'bwd':
                    self._set_speed(action['speed'])
                    bwd()
                elif action['command'] == 'tune':
                    self.calibration = action['calibration']
                    self.kp = action['kp']
                    self.kp = action['ki']
                    self.kp = action['kd']
                elif action['command'] == 'speed':
                    self._set_speed(action['speed'])
                elif action['command'] == 'direction':
                    self.direction = action['direction']
                elif action['command'] == 'calibration':
                    self.calibration = action['calibration']
                elif action['command'] == 'kp':
                    self.kp = action['kp']
                elif action['command'] == 'ki':
                    self.kp = action['ki']
                elif action['command'] == 'kd':
                    self.kp = action['kd']
                elif action['command'] == 'end':
                    stop()
                    break
                elif action['command'] == 'pass':
                    pass
                elif action['command'] == 'left_rot':
                    set_speed(150)
                    left_rot()
                    time.sleep(action['duration'])
                    stop()
                    set_speed(0)
                elif action['command'] == 'right_rot':
                    set_speed(150)
                    right_rot()
                    time.sleep(action['duration'])
                    stop()
                    set_speed(0)
                else:
                    print('wtf is %s' % action['command'])
                    stop()
                    break
            except Empty:
                # print(".")
                pass

            if us_dist(0) < self.safe_distance:
                print("EMERGENCY STOP")
                stop()
                set_speed(0)
                servo(130)
                time.sleep(1)
                servo(50)
                time.sleep(1)
                led_off(0)
                led_off(1)
                led_on(0)
                led_on(1)
                led_off(0)
                led_off(1)
                led_on(0)
                led_on(1)
                servo(100)
                time.sleep(1)
                servo(80)
                time.sleep(1)
                servo(100)
                time.sleep(1)
                servo(80)
                time.sleep(1)
                servo(90)
                led_off(0)
                led_off(1)
                led_on(0)
                led_on(1)
                led_off(0)
                led_off(1)
                return

            correction = self._correction()
            correction_l = correction_r = int(correction / 2)
            set_right_speed(self.current_speed + correction_r)
            set_left_speed(self.current_speed - correction_l)

        return


if __name__ == '__main__':
    action_queue = multiprocessing.JoinableQueue()
    results_queue = multiprocessing.Queue()
    motion_child = PidController(action_queue, results_queue)
    motion_child.start()

    # print("**** straight")
    action = {'command': 'fwd', 'speed': 150}
    action_queue.put(action)
    # time.sleep(10)
    # action = {'end'}
    # action_queue.put(action)
    motion_child.join()