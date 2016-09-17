"""
from PIL import Image
import zbarlight

file_path = 'qr_code.jpg'
with open(file_path, 'rb') as image_file:
    image = Image.open(image_file)
    image.load()

codes = zbarlight.scan_codes('qrcode', image)
print('QR codes: %s' % codes)
"""

"""
from qrtools import QR
myCode = QR(filename=u"qr_code.jpg")
if myCode.decode():
  print myCode.data
"""

import picamera
from qrtools import QR
import time

with picamera.PiCamera() as camera:
    while True:
        camera.capture('QR.jpg')
        print "PIC!"
        myCode = QR(filename=u"QR.jpg")
        if myCode.decode():
            print myCode.data