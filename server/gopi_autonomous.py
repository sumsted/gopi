from bottle import get, debug, run, view
from tools import handle_padded
import common_views


debug_mode = True
port = 8083

@get("/")
@view("autonomous.html")
def landing():
    return {}


if __name__ == '__main__':
    debug(debug_mode)
    run(host='0.0.0.0', port=port, debug=debug_mode)
