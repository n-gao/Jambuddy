import win32gui
import win32ui
import win32process
import win32api
import win32con
from ctypes import windll
from PIL import Image, ImageChops
import time
import re

""" Used to capture screenshots of applications.
    Usage: with ScreenCapture('VSTHost.*') as capture:
        img = capture.capture()
        ...
"""
class ScreenCapture:
    def __init__(self, app_name):
        self.app_name = app_name

    
    def __enter__(self):
        # Initialize windows stuff and allocate bitmap
        self.handle = win32gui.FindWindow(None, self.app_name)
        if self.handle == 0:
            self.handle = _find_window_wildcard(self.app_name)
        
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.handle)
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        
        self.handle_dc = win32gui.GetWindowDC(self.handle)
        self.mfc_dc = win32ui.CreateDCFromHandle(self.handle_dc)
        self.save_dc = self.mfc_dc.CreateCompatibleDC()
        
        self.bitmap = win32ui.CreateBitmap()
        self.bitmap.CreateCompatibleBitmap(self.mfc_dc, self.width, self.height)
        
        self.save_dc.SelectObject(self.bitmap)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Free everything
        win32gui.DeleteObject(self.bitmap.GetHandle())
        self.save_dc.DeleteDC()
        self.mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.handle, self.handle_dc)
        if exc_type:
            raise exc_type(exc_value)

    """Captures a screenshot of the given application and returns it as PIL Image.
    Returns:
        PIL.Image -- Screenshot
    """
    def capture(self):
        succ = windll.user32.PrintWindow(self.handle, self.save_dc.GetSafeHdc(), 0)
        if succ == 0:
            print('Failed to take capture.')
            return
        bmpinfo = self.bitmap.GetInfo()
        bmpstr = self.bitmap.GetBitmapBits(True)
        result = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight'])
            , bmpstr, 'raw', 'BGRX', 0, 1)
        return result

# Callback for iteration
def _window_enum_callback(hwnd, data):
    """Pass to win32gui.EnumWindows() to check all the opened windows"""
    if re.match(data[0], str(win32gui.GetWindowText(hwnd))) is not None:
        data[1] = hwnd
        return False

# Helper to use wildcards when finding windows
def _find_window_wildcard(wildcard):
    """find a window whose title matches the wildcard regex"""
    data = [wildcard, None]
    try:
        win32gui.EnumWindows(_window_enum_callback, data)
    except:
        pass
    return data[1]

if __name__ == '__main__':
    with ScreenCapture(".*VSTHost.*") as cap:
        # while True:
        #     key = input('Key: ')
        #     key_img = get_key_image(cap.capture())
        #     key_img.save('Keys/%s.png' % key)
        cap.capture().show()
        # cap.capture().crop((20, 240, 190, 400)).show()
