from Queue import Empty
import multiprocessing
import time
from gopigo_client import *


class PidController(multiprocessing.Process):
    def __init__(self, action_queue, results_queue):
        super(PidController, self).__init__()
        print("time_elapsed, kp, ki, kd, delta_l,delta_r, error_p, error_i, error_d, correction, speed, right_speed")
        self.action_queue = action_queue
        self.results_queue = results_queue
        self.kp = self.ki = self.kd = self.calibration = 0
        self.error_i = 0
        self.last_error_p = 0
        self.time_elapsed = 0
        self.base_l = self.latest_l = 0
        self.base_r = self.latest_r = 0
        self.start_time = self.last_time = 0
        self.safe_distance = 30
        self.current_speed = 0
        self.direction = 0

    @staticmethod
    def _get_current_milliseconds():
        # return time.time()
        return int(round(time.time() * 1000))

    def _reset(self):
        # enable_encoders()
        # time.sleep(1)
        self.kp = 10
        self.ki = 0
        self.kd = 0
        self.calibration = 0
        self.error_i = 0
        self.time_elapsed = 0
        self.base_l = enc_read(0)
        self.base_r = enc_read(1)
        self.start_time = self.last_time = self._get_current_milliseconds()
        self.last_error_p = 0
        self.direction = 0

    def _tune(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def _set_start_speed(self, speed):
        set_left_speed(speed - 15)
        set_right_speed(speed + 15)
        self.current_speed = speed

    def _set_speed(self, speed):
        set_speed(speed)
        self.current_speed = speed

    def _correction(self):
        latest_l = enc_read(0)
        latest_r = enc_read(1)

        current_time = self._get_current_milliseconds()
        time_elapsed = current_time - self.last_time

        # print self.base_l, self.base_r
        # print latest_l, latest_r

        delta_l = (latest_l - self.base_l)
        delta_r = (latest_r - self.base_r)
        error_p = delta_l - delta_r
        self.error_i += int(error_p * time_elapsed / 1000)
        error_d = (error_p - self.last_error_p) / time_elapsed

        correction = self.kp * error_p + self.ki * self.error_i + self.kd * error_d + self.calibration

        # print("dl: %d, dr: %d, te: %d, ep: %d, ei: %d, ed: %d, s: %d, c: %d, rs: %d" %
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
                # action = self.action_queue.get(True, .2)
                action = self.action_queue.get(False)
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
                    self._tune(action['kp'], action['ki'], action['d'])
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