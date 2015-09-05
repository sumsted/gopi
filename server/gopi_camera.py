import base64
from PIL import Image, ImageDraw
from bottle import get, debug, run, view
import picamera
import cStringIO
import io
from tools import handle_padded
import common_views


debug_mode = True
port = 8082


@get("/")
@view("camera.html")
def landing():
    return {}


class GopiImage():
    IMAGE_SIZE = (320, 240)
    SPOT_MAP = {
        -15: (20, 100, 60, 140),
        -10: (60, 100, 100, 140),
        -5: (100, 100, 140, 140),
        0: (140, 100, 180, 140),
        5: (180, 100, 220, 140),
        10: (220, 100, 260, 140),
        15: (260, 100, 300, 140)
    }

    def __init__(self):
        self.image_byte_array = None

    def write(self, image_byte_array):
        self.image_byte_array = image_byte_array

    def get_image_target_overlay(self):
        image = Image.open(cStringIO.StringIO(self.image_byte_array))
        red = '#FF0000'
        green = '#48BD41'
        draw = ImageDraw.Draw(image)

        width = image.size[0]
        height = image.size[1]

        xc = width / 2
        yc = height / 2
        radius = width / 5
        center_space = radius / 5
        fat_space = radius / 2
        x0 = xc - radius
        x1 = xc + radius
        y0 = yc - radius
        y1 = yc + radius
        for i in range(5):
            box = (x0 + i, y0 + i, x1 - i, y1 - i)
            draw.ellipse(box, outline=green)

        line = (x0, yc, xc - center_space, yc)
        draw.line(line, fill=green, width=3)
        line = (x1, yc, xc + center_space, yc)
        draw.line(line, fill=green, width=3)
        line = (xc, y1, xc, yc + center_space)
        draw.line(line, fill=green, width=3)

        line = (x0, yc, xc - fat_space, yc)
        draw.line(line, fill=green, width=5)
        line = (x1, yc, xc + fat_space, yc)
        draw.line(line, fill=green, width=5)
        line = (xc, y1, xc, yc + fat_space)
        draw.line(line, fill=green, width=5)

        center = (xc, yc)
        box = (xc - 2, yc - 2, xc + 2, yc + 2)
        # draw.point(center, fill='#FF0000')
        draw.ellipse(box, fill=red)

        fp = io.BytesIO()
        image.save(fp, 'PNG')
        image_byte_array = fp.getvalue()
        fp.close()
        return 'data:image/png;base64,' + base64.b64encode(image_byte_array)

    def get_image_spot_overlay(self):
        image = Image.open(cStringIO.StringIO(self.image_byte_array))
        red = '#FF0000'
        green = '#48BD41'
        yellow = '#FFFF00'

        draw = ImageDraw.Draw(image)

        width = image.size[0]
        height = image.size[1]

        for degrees, spot in self.SPOT_MAP.iteritems():
            line = (spot[0], spot[1], spot[2], spot[1])
            draw.line(line, fill=yellow, width=1)
            line = (spot[2], spot[1], spot[2], spot[3])
            draw.line(line, fill=yellow, width=1)
            line = (spot[2], spot[3], spot[0], spot[3])
            draw.line(line, fill=yellow, width=1)
            line = (spot[0], spot[3], spot[0], spot[1])
            draw.line(line, fill=yellow, width=1)

        fp = io.BytesIO()
        image.save(fp, 'PNG')
        image_byte_array = fp.getvalue()
        fp.close()
        return 'data:image/png;base64,' + base64.b64encode(image_byte_array)

    def get_image_byte_array(self):
        return self.image_byte_array

    def get_b64(self):
        return 'data:image/png;base64,' + base64.b64encode(self.image_byte_array)

    def get_spot(self):
        pass


@get('/cam/image')
@handle_padded
def cam_image(kargs):
    gpi = GopiImage()

    with picamera.PiCamera() as camera:
        camera.resolution = gpi.IMAGE_SIZE
        camera.capture_sequence([gpi], format="jpeg", use_video_port=False)

    # return {'image': gpi.get_image_target_overlay()}
    return {'image': gpi.get_image_spot_overlay()}


@get('/cam/spot/<degrees>')
@handle_padded
def cam_spot(kargs):
    pass


# if __name__ == '__main__':
#     infile = 'static/images/pi1.jpg'
#     outfile = 'static/images/wo.html'
#     iba = open(infile, 'rb').read()
#     gpi = GopiImage()
#     gpi.write(iba)
#     b = gpi.get_image_with_overlay()
#     with open(outfile, 'w') as of:
#         of.write('<html><body><img src="data:image/png;base64,' + b + '"></body></html>')
#     pass
#

if __name__ == '__main__':
    debug(debug_mode)
    run(host='0.0.0.0', port=port, debug=debug_mode)
