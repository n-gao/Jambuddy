import screen_capture
from PIL import ImageChops, Image
from subprocess import run, Popen
import numpy as np
import time
import os
import win32gui
import win32api
import win32con
import math
from pentatonic import _base_notes
import pytesseract

class VstReader:
    def __init__(self, exe_path = None, save_file = None, key_dir = './Keys'):
        try:
            self.capture = screen_capture.ScreenCapture('.*VSTHost.*')
        except:
            if exe_path is None:
                raise ValueError('VSTHost not running and no exe provided.')
            Popen([exe_path, save_file])
            time.sleep(3)
            self.capture = screen_capture.ScreenCapture('.*VSTHost.*')
        self.files = os.listdir(key_dir)
        self.file_paths = []
        for f in self.files:
            self.file_paths.append(key_dir + '/' + f)
        self.images = {}
        for i in range(len(self.files)):
            self.images[self.files[i][:-4]] = Image.open(self.file_paths[i])
        self.key_name = 'Cmaj'

    def get_key(self):
        try:
            return _base_notes[self.key_name[:-3]], self.key_name[:-3], self.key_name[-3:]
        except:
            return None

    def _read_key(self):
        with self.capture:
            img = self.capture.capture()
            key_img = get_key_image(img)
            lowest_err = -1
            lowest_key_err = -1
            for key, im in self.images.items():
                error = get_rms(key_img, im)
                if error < lowest_err or lowest_err == -1:
                    lowest_err = error
                    lowest_key_err = key
                    if error == 0:
                        return key, 0, key_img
            if lowest_err > 0.1:
                return None, 0, key_img
            return lowest_key_err, lowest_err, key_img
        
    def read_key(self):
        result = self._read_key()
        self.key_name = result[0]
        return result

    def continously_read(self, interval = 0.2):
        while True:
            self.key_name, _, _ = self.read_key()
            time.sleep(interval)

    def reset(self):
        # win32gui.SetForegroundWindow(self.capture.handle)
        # x = self.capture.left + 425
        # y = self.capture.top + 200
        self.capture.click(425, 200)

    def fix_audio(self):
        previous = win32gui.GetForegroundWindow()
        self.capture.set_forground()
        time.sleep(1/100)
        self.capture.click(300, 40, False)
        time.sleep(1/100)
        self.capture.click(300, 80, False)
        time.sleep(1/3)
        self.capture.click(None, None, False)
        time.sleep(1/100)
        win32gui.SetForegroundWindow(previous)
        time.sleep(1/100)

    def get_key_probabilities(self):
        with self.capture:
            img = get_key_probabilities_image(self.capture.capture())
            img.show()

 
"""Extracts the region where the chord is displayed from the given image.
"""
def get_chord_image(img):
    return img.crop((200, 192, 360, 246))

"""Extracts the region where the key is displayed from the given image.
"""
def get_key_image(img):
    return img.crop((200, 260, 360, 312))

def get_key_probabilities_image(img):
    return img.crop((400, 260, 500, 340))

"""Return true if both images are equal.
"""
def check_equality(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

def get_rms(im1, im2):
    diff = np.asarray(ImageChops.difference(im1, im2)) / 255
    return math.sqrt(np.mean(np.square(diff)))

if __name__ == '__main__':
    VstReader('./Keys').get_key_probabilities()
    while False:
        start = time.time()
        reader = VstReader('./Keys')
        key, error, key_img = reader.read_key()
        if key == None:
            key_img.show()
            key = input('Key: ')
            key_img.save('Keys/%s.png' % key)
        print('%s %f' % (key, error))
        # reader.reset()
        time.sleep(1)


# if __name__ == '__main__':
#     with screen_capture.ScreenCapture(".*VSTHost.*") as cap:
#         while True:
#             key = input('Key: ')
#             key_img = get_key_image(cap.capture())
#             key_img.save('Keys/%s.png' % key)
