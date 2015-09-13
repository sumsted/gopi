import multiprocessing
from bottle import get, debug, run, view
import requests
from gopiimage import GopiImage
from tools import handle_padded
import common_views
from gopiimage import GopiImage
from pidcontroller import PidController

debug_mode = True
port = 8083
camera_host = 'http://192.168.42.1:8082'
# pid_host = 'http://192.168.42.1:8081'

# @get("/")
# @view("autonomous.html")
# def landing():
#     return {}


class GoPiAutonomous():

    def __init__(self):
        # self.gpi = GopiImage()
        self.action_queue = multiprocessing.JoinableQueue()
        self.results_queue = multiprocessing.Queue()
        self.motion_child = PidController(self.action_queue, self.results_queue)
        self.motion_child.start()


    def start(self, color):
        # seek
        found = False
        bad_tries = 0
        while not found and bad_tries < 10:
            # self.gpi.load_file('static/images/test3.png')
            # degrees, spots = self.gpi.find_color(color)
            result = requests.get(camera_host+'/cam/find/'+color).json()
            degrees = result['degrees']
            if degrees is not None:
                if degrees == -15:
                    self.action_queue.put({'command': 'left_rot', 'duration': .05})
                elif degrees == -10:
                    self.action_queue.put({'command': 'left_rot', 'duration': .05})
                elif degrees == -5:
                    self.action_queue.put({'command': 'left_rot', 'duration': .05})
                elif degrees == 0:
                    found = True
                if degrees == 5:
                    self.action_queue.put({'command': 'right_rot', 'duration': .05})
                elif degrees == 10:
                    self.action_queue.put({'command': 'right_rot', 'duration': .05})
                elif degrees == 15:
                    self.action_queue.put({'command': 'right_rot', 'duration': .05})
            bad_tries += 1
        if found:
            pass
            # set speed 150
            #pid fwd
            self.action_queue.put({'command': 'fwd', 'speed': 100})
            self.motion_child.join()
        else:
            pass


if __name__ == '__main__':
    gpa = GoPiAutonomous()
    gpa.start('red')

# if __name__ == '__main__':
#     debug(debug_mode)
#     run(host='0.0.0.0', port=port, debug=debug_mode)

