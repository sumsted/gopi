import multiprocessing
from bottle import get, route, request, response, run, post, debug, view
from pidcontroller import PidController
from tools import handle_padded
import common_views


debug_mode = True
port = 8081


# Start the pid controller process
action_queue = multiprocessing.JoinableQueue()
results_queue = multiprocessing.Queue()
motion_child = PidController(action_queue, results_queue)
motion_child.start()


#################
###### views ####
#################
@get("/")
@view("pid.html")
def landing():
    return {}


#################
###### api ######
#################
@get('/pid/fwd/<speed>/<direction>/<calibration>/<kp>/<ki>/<kd>')
@handle_padded
def pid_fwd(kargs):
    action = {'command': 'fwd', 'speed': int(kargs['speed']), 'direction': int(kargs['direction']),
              'calibration': int(kargs['calibration']), 'kp': int(kargs['kp']), 'ki': int(kargs['ki']),
              'kd': int(kargs['kd'])}
    action_queue.put(action)
    return 1


@get('/pid/bwd/<speed>/<direction>/<calibration>/<kp>/<ki>/<kd>')
@handle_padded
def pid_bwd(kargs):
    action = {'command': 'bwd', 'speed': int(kargs['speed']), 'direction': int(kargs['direction']),
              'calibration': int(kargs['calibration']), 'kp': int(kargs['kp']), 'ki': int(kargs['ki']),
              'kd': int(kargs['kd'])}
    action_queue.put(action)
    return 1


@get('/pid/tune/<calibration>/<kp>/<ki>/<kd>')
@handle_padded
def pid_tune(kargs):
    action = {'command': 'tune',
              'calibration': int(kargs['calibration']), 'kp': int(kargs['kp']), 'ki': int(kargs['ki']),
              'kd': int(kargs['kd'])}
    action_queue.put(action)
    return 1


@get('/pid/speed/<speed>')
@handle_padded
def pid_speed(kargs):
    action = {'command': 'speed', 'speed': int(kargs['speed'])}
    action_queue.put(action)
    return 1


# todo: add tune call
# @get('/pid/tune/<direction>/<direction>')
# @handle_padded
# def pid_direction(kargs):
#     action = {'command': 'direction', 'direction': int(kargs['direction'])}
#     action_queue.put(action)
#     return 1


@get('/pid/kp/<kp>')
@handle_padded
def pid_kp(kargs):
    action = {'command': 'kp', 'kp': int(kargs['kp'])}
    action_queue.put(action)
    return 1


@get('/pid/ki/<ki>')
@handle_padded
def pid_ki(kargs):
    action = {'command': 'ki', 'ki': int(kargs['ki'])}
    action_queue.put(action)
    return 1


@get('/pid/kd/<kd>')
@handle_padded
def pid_kd(kargs):
    action = {'command': 'kd', 'kd': int(kargs['kd'])}
    action_queue.put(action)
    return 1

@get('/pid/stop')
@handle_padded
def pid_stop(kargs):
    action = {'command': 'stop'}
    action_queue.put(action)
    return 1

@get('/pid/end')
@handle_padded
def pid_end(kargs):
    action = {'command': 'end'}
    action_queue.put(action)
    return 1


if __name__ == '__main__':
    debug(debug_mode)
    run(host='0.0.0.0', port=port, debug=debug_mode)