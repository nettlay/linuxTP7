import pyautogui
import time
from Test_Script import Check_window as Cw


def close_window():
    time.sleep(1)
    width, height = pyautogui.size()
    pyautogui.click(width/2, height/2)
    pyautogui.hotkey('ctrl', 'alt', 'f4')
    time.sleep(1)
    if Cw.check_window("T", "./Test_Data/1920x1200/template_file/system_window.png"):
        return True
    else:
        return False
