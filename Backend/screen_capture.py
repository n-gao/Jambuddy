import win32gui
import win32ui
import win32process
import win32api
import win32con
from ctypes import windll
from PIL import Image
import time

hwnd = win32gui.FindWindow(None, 'Unbenannt - paint.net v4.0.21')

# def iter(handle, extra):
#     _, procpid = win32process.GetWindowThreadProcessId(handle)
#     try:
#         proc = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, procpid)
#         procname = win32process.GetModuleFileNameEx(proc, 0)
#         print(procname)
#         if procname.endswith('Discord.exe'):
#             hwnd = handle
#             return False
#     except:
#         pass

# try:
#     win32gui.EnumWindows(iter, None)
# except:
#     pass

left, top, right, bottom = win32gui.GetWindowRect(hwnd)
w = right - left
h = bottom - top

hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

bitmap = win32ui.CreateBitmap()
bitmap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(bitmap)
while True:
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    print(result)

    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)


    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)


win32gui.DeleteObject(bitmap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)

if result == 1:
    #PrintWindow Succeeded
    im.save("test.png")
