from bottle import get, route, request, response, run, post, debug
import gopigo
import views


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


@get('/write_i2c_block/<address>/<block>')
@handle_padded
def write_i2c_block(kargs):
    r = {'return_value': gopigo.write_i2c_block(int(kargs['address']), int(kargs['block']))}
    return r


@get('/writeNumber/<value>')
@handle_padded
def writeNumber(kargs):
    r = {'return_value': gopigo.writeNumber(int(kargs['value']))}
    return r


@get('/readByte')
@handle_padded
def readByte(kargs):
    r = {'return_value': gopigo.readByte()}
    return r


@get('/motor1/<direction>/<speed>')
@handle_padded
def motor1(kargs):
    r = {'return_value': gopigo.motor1(int(kargs['direction']), int(kargs['speed']))}
    return r


@get('/motor2/<direction>/<speed>')
@handle_padded
def motor2(kargs):
    r = {'return_value': gopigo.motor2(int(kargs['direction']), int(kargs['speed']))}
    return r


@get('/fwd')
@handle_padded
def fwd(kargs):
    r = {'return_value': gopigo.fwd()}
    return r


@get('/motor_fwd')
@handle_padded
def motor_fwd(kargs):
    r = {'return_value': gopigo.motor_fwd()}
    return r


@get('/bwd')
@handle_padded
def bwd(kargs):
    r = {'return_value': gopigo.bwd()}
    return r


@get('/motor_bwd')
@handle_padded
def motor_bwd(kargs):
    r = {'return_value': gopigo.motor_bwd()}
    return r


@get('/left')
@handle_padded
def left(kargs):
    r = {'return_value': gopigo.left()}
    return r


@get('/left_rot')
@handle_padded
def left_rot(kargs):
    r = {'return_value': gopigo.left_rot()}
    return r


@get('/right')
@handle_padded
def right(kargs):
    r = {'return_value': gopigo.right()}
    return r


@get('/right_rot')
@handle_padded
def right_rot(kargs):
    r = {'return_value': gopigo.right_rot()}
    return r


@get('/stop')
@handle_padded
def stop(kargs):
    r = {'return_value': gopigo.stop()}
    return r


@get('/increase_speed')
@handle_padded
def increase_speed(kargs):
    r = {'return_value': gopigo.increase_speed()}
    return r


@get('/decrease_speed')
@handle_padded
def decrease_speed(kargs):
    r = {'return_value': gopigo.decrease_speed()}
    return r


@get('/trim_test/<value>')
@handle_padded
def trim_test(kargs):
    r = {'return_value': gopigo.trim_test(int(kargs['value']))}
    return r


@get('/trim_read')
@handle_padded
def trim_read(kargs):
    r = {'return_value': gopigo.trim_read()}
    return r


@get('/trim_write/<value>')
@handle_padded
def trim_write(kargs):
    r = {'return_value': gopigo.trim_write(int(kargs['value']))}
    return r


@get('/digitalRead/<pin>')
@handle_padded
def digitalRead(kargs):
    r = {'return_value': gopigo.digitalRead(int(kargs['pin']))}
    return r


@get('/digitalWrite/<pin>/<value>')
@handle_padded
def digitalWrite(kargs):
    r = {'return_value': gopigo.digitalWrite(int(kargs['pin']), int(kargs['value']))}
    return r


@get('/pinMode/<pin>/<mode>')
@handle_padded
def pinMode(kargs):
    r = {'return_value': gopigo.pinMode(int(kargs['pin']), int(kargs['mode']))}
    return r


@get('/analogRead/<pin>')
@handle_padded
def analogRead(kargs):
    r = {'return_value': gopigo.analogRead(int(kargs['pin']))}
    return r


@get('/analogWrite/<pin>/<value>')
@handle_padded
def analogWrite(kargs):
    r = {'return_value': gopigo.analogWrite(int(kargs['pin']), int(kargs['value']))}
    return r


@get('/volt')
@handle_padded
def volt(kargs):
    r = {'return_value': gopigo.volt()}
    return r


@get('/brd_rev')
@handle_padded
def brd_rev(kargs):
    r = {'return_value': gopigo.brd_rev()}
    return r


@get('/us_dist/<pin>')
@handle_padded
def us_dist(kargs):
    r = {'return_value': gopigo.us_dist(int(kargs['pin']))}
    return r


@get('/read_motor_speed')
@handle_padded
def read_motor_speed(kargs):
    r = {'return_value': gopigo.read_motor_speed()}
    return r


@get('/led_on/<l_id>')
@handle_padded
def led_on(kargs):
    r = {'return_value': gopigo.led_on(int(kargs['l_id']))}
    return r


@get('/led_off/<l_id>')
@handle_padded
def led_off(kargs):
    r = {'return_value': gopigo.led_off(int(kargs['l_id']))}
    return r


@get('/servo/<position>')
@handle_padded
def servo(kargs):
    r = {'return_value': gopigo.servo(int(kargs['position']))}
    return r


@get('/enc_tgt/<m1>/<m2>/<target>')
@handle_padded
def enc_tgt(kargs):
    r = {'return_value': gopigo.enc_tgt(int(kargs['m1']), int(kargs['m2']), int(kargs['target']))}
    return r


@get('/enc_read/<motor>')
@handle_padded
def enc_read(kargs):
    r = {'return_value': gopigo.enc_read(int(kargs['motor']))}
    return r


@get('/fw_ver')
@handle_padded
def fw_ver(kargs):
    r = {'return_value': gopigo.fw_ver()}
    return r


@get('/enable_encoders')
@handle_padded
def enable_encoders(kargs):
    r = {'return_value': gopigo.enable_encoders()}
    return r


@get('/disable_encoders')
@handle_padded
def disable_encoders(kargs):
    r = {'return_value': gopigo.disable_encoders()}
    return r


@get('/enable_servo')
@handle_padded
def enable_servo(kargs):
    r = {'return_value': gopigo.enable_servo()}
    return r


@get('/disable_servo')
@handle_padded
def disable_servo(kargs):
    r = {'return_value': gopigo.disable_servo()}
    return r


@get('/set_left_speed/<speed>')
@handle_padded
def set_left_speed(kargs):
    r = {'return_value': gopigo.set_left_speed(int(kargs['speed']))}
    return r


@get('/set_right_speed/<speed>')
@handle_padded
def set_right_speed(kargs):
    r = {'return_value': gopigo.set_right_speed(int(kargs['speed']))}
    return r


@get('/set_speed/<speed>')
@handle_padded
def set_speed(kargs):
    r = {'return_value': gopigo.set_speed(int(kargs['speed']))}
    return r


@get('/enable_com_timeout/<timeout>')
@handle_padded
def enable_com_timeout(kargs):
    r = {'return_value': gopigo.enable_com_timeout(int(kargs['timeout']))}
    return r


@get('/disable_com_timeout')
@handle_padded
def disable_com_timeout(kargs):
    r = {'return_value': gopigo.disable_com_timeout()}
    return r


@get('/read_status')
@handle_padded
def read_status(kargs):
    r = {'return_value': gopigo.read_status()}
    return r


@get('/read_enc_status')
@handle_padded
def read_enc_status(kargs):
    r = {'return_value': gopigo.read_enc_status()}
    return r


@get('/read_timeout_status')
@handle_padded
def read_timeout_status(kargs):
    r = {'return_value': gopigo.read_timeout_status()}
    return r


@get('/ir_read_signal')
@handle_padded
def ir_read_signal(kargs):
    r = {'return_value': gopigo.ir_read_signal()}
    return r


@get('/ir_recv_pin/<pin>')
@handle_padded
def ir_recv_pin(kargs):
    r = {'return_value': gopigo.ir_recv_pin(int(kargs['pin']))}
    return r

debug(True)
run(host='0.0.0.0', port=8080, debug=True)
