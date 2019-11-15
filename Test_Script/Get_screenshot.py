import os
import time
import datetime
import pyautogui
import Test_Script.common_function as co


log = co.logger()


def get_screenshot():
    time.sleep(1)
    s = str(datetime.datetime.today())
    s1 = s.replace(' ', '-')[:19]
    s2 = s1.replace(':', '-')
    pyautogui.screenshot('./Test_Report/screenshot/SystermInfo-' + s2 + '.png')
    time.sleep(3)
    log.info("Get the screen shot named as SystemInfo"+s2+".png.")
    if os.path.exists('./Test_Report/screenshot/SystermInfo-' + s2 + '.png'):
        co.pass_report("Check_System_information")
        return True
    else:
        co.fail_report("Screenshot save failed", "Check_System_information")
        return

