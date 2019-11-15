import time
import pyautogui
import Test_Script.common_function as co
from Test_Script import Check_window as Cw


log = co.logger()


def get_screensize():
    time.sleep(1)
    resolution = pyautogui.size()
    log.info("Current Resolution : " + str(resolution))


def open_systeminfo():
    pyautogui.hotkey('ctrl', 'alt', 'end')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'alt', 's')
    time.sleep(1)
    pyautogui.typewrite('system information')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    if Cw.check_window("F", "./Test_Data/1920x1200/template_file/system_window.png"):
        return True
    else:
        return False

