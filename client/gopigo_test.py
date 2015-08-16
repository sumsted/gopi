from unittest import TestCase
from client.gopigo_client import *


class TestGopigo(TestCase):
    def test_write_i2c_block(self):
        address = 1
        block = 1
        self.assertEqual(write_i2c_block(address, block), 1)

    def test_writeNumber(self):
        value = 1
        self.assertEqual(writeNumber(value), 1)

    def test_readByte(self):
        self.assertEqual(readByte(), 1)

    def test_motor1(self):
        direction = 1
        speed = 1
        self.assertEqual(motor1(direction, speed), 1)

    def test_motor2(self):
        direction = 1
        speed = 1
        self.assertEqual(motor2(direction, speed), 1)

    def test_fwd(self):
        self.assertEqual(fwd(), 1)

    def test_motor_fwd(self):
        self.assertEqual(motor_fwd(), 1)

    def test_bwd(self):
        self.assertIsNone(bwd())

    def test_motor_bwd(self):
        self.assertEqual(motor_bwd(), 1)

    def test_left(self):
        self.assertEqual(left(), 1)

    def test_left_rot(self):
        self.assertEqual(left_rot(), 1)

    def test_right(self):
        self.assertEqual(right(), 1)

    def test_right_rot(self):
        self.assertEqual(right_rot(), 1)

    def test_stop(self):
        self.assertEqual(stop(), 1)

    def test_increase_speed(self):
        self.assertEqual(increase_speed(), 1)

    def test_decrease_speed(self):
        self.assertEqual(decrease_speed(), 1)

    def test_trim_test(self):
        value = 1
        self.assertEqual(trim_test(value), 1)

    def test_trim_read(self):
        self.assertEqual(trim_read(), 1)

    def test_trim_write(self):
        value = 1
        self.assertEqual(trim_write(value), 1)

    def test_digitalRead(self):
        pin = 1
        self.assertEqual(digitalRead(pin), 1)

    def test_digitalWrite(self):
        pin = 1
        value = 1
        self.assertEqual(digitalWrite(pin, value), 1)

    def test_pinMode(self):
        pin = 1
        mode = 1
        self.assertEqual(pinMode(pin, mode), 1)

    def test_analogRead(self):
        pin = 1
        self.assertEqual(analogRead(pin), 1)

    def test_analogWrite(self):
        pin = 1
        value = 1
        self.assertEqual(analogWrite(pin, value), 1)

    def test_volt(self):
        self.assertEqual(volt(), 1)

    def test_brd_rev(self):
        self.assertEqual(brd_rev(), 1)

    def test_us_dist(self):
        pin = 1
        self.assertEqual(us_dist(pin), 1)

    def test_read_motor_speed(self):
        self.assertEqual(read_motor_speed(), 1)

    def test_led_on(self):
        l_id = 1
        self.assertEqual(led_on(l_id), 1)

    def test_led_off(self):
        l_id = 1
        self.assertIsNone(led_off(l_id))

    def test_servo(self):
        position = 1
        self.assertEqual(servo(position), 1)

    def test_enc_tgt(self):
        m1 = 1
        m2 = 1
        target = 1
        self.assertEqual(enc_tgt(m1, m2, target), 1)

    def test_enc_read(self):
        motor = 1
        self.assertEqual(enc_read(motor), 1)

    def test_fw_ver(self):
        self.assertEqual(fw_ver(), 1)

    def test_enable_encoders(self):
        self.assertEqual(enable_encoders(), 1)

    def test_disable_encoders(self):
        self.assertEqual(disable_encoders(), 1)

    def test_enable_servo(self):
        self.assertEqual(enable_servo(), 1)

    def test_disable_servo(self):
        self.assertEqual(disable_servo(), 1)

    def test_set_left_speed(self):
        speed = 1
        self.assertEqual(set_left_speed(speed), 1)

    def test_set_right_speed(self):
        speed = 1
        self.assertEqual(set_right_speed(speed), 1)

    def test_set_speed(self):
        speed = 1
        self.assertEqual(set_speed(speed), 1)

    def test_enable_com_timeout(self):
        timeout = 1
        self.assertEqual(enable_com_timeout(timeout), 1)

    def test_disable_com_timeout(self):
        self.assertEqual(disable_com_timeout(), 1)

    def test_read_status(self):
        self.assertEqual(read_status(), 1)

    def test_read_enc_status(self):
        self.assertEqual(read_enc_status(), 1)

    def test_read_timeout_status(self):
        self.assertEqual(read_timeout_status(), 1)

    def test_ir_read_signal(self):
        self.assertEqual(ir_read_signal(), 1)

    def test_ir_recv_pin(self):
        pin = 1
        self.assertEqual(ir_recv_pin(pin), 1)

