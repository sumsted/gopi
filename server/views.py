from bottle import get, route, request, response, run, post, view, static_file, error


@route('/static/<filepath:path>')
def render_static(filepath):
    return static_file(filepath, root='./static')


@get("/")
@view("landing.html")
def landing():
    return {}


@get("/pid")
@view("pid.html")
def pid():
    return {}


@error(404)
@view("not_found.html")
def not_found(error):
    return {}


@error(404)
@view("server_error.html")
def not_found(error):
    return {}
