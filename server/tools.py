from bottle import request, response


def handle_padded(handler):
    def decorator(**kwargs):
        r = handler(kwargs)
        try:
            callback = request.query.get('callback')
        except Exception, e:
            callback = None
        if callback is None:
            return r
        else:
            response.content_type = 'text/javascript'
            return "%s(%r);" % (callback, r)
    return decorator
