import screen_capture
from PIL import ImageChops, Image
import time
import os

class VstReader:
    def __init__(self, key_dir):
        self.capture = screen_capture.ScreenCapture('.*VSTHost.*')
        self.files = os.listdir(key_dir)
        self.file_paths = []
        for f in self.files:
            self.file_paths.append(key_dir + '/' + f)
        self.images = {}
        for i in range(len(self.files)):
            self.images[self.files[i][:-4]] = Image.open(self.file_paths[i])

    def get_key(self):
        with self.capture:
            img = self.capture.capture()
            key_img = get_key_image(img)
            for key, im in self.images.items():
                if check_equality(im, key_img):
                    return key, key_img
            return None, key_img


"""Extracts the region where the chord is displayed from the given image.
"""
def get_chord_image(img):
    return img.crop((200, 192, 360, 246))

"""Extracts the region where the key is displayed from the given image.
"""
def get_key_image(img):
    return img.crop((200, 260, 360, 312))

"""Return true if both images are equal.
"""
def check_equality(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

if __name__ == '__main__':
    while True:
        key, key_img = VstReader('./Keys').get_key()
        if key == None:
            key_img.show()
            key = input('Key: ')
            key_img.save('Keys/%s.png' % key)
        print(key)

# if __name__ == '__main__':
#     with screen_capture.ScreenCapture(".*VSTHost.*") as cap:
#         while True:
#             key = input('Key: ')
#             key_img = get_key_image(cap.capture())
#             key_img.save('Keys/%s.png' % key)
