import time
import pyautogui
import Test_Script.common_function as co


log = co.logger()


def check_window(runflag, picture):
    count = 0
    time.sleep(3)
    if runflag == "F":
        system_window = pyautogui.locateOnScreen(picture)
        if system_window is not None:
            log.info("window opens successfully")
            return True
        else:
            while count <= 5:
                log.info("window opens failed!")
                count += 1
                if count == 6:
                    return False
    else:
            system_window = pyautogui.locateOnScreen(picture)
            if system_window is None:
                log.info("window closes successfully")
                return True
            else:
                while count <= 5:
                    log.info("window closes failed!")
                    count += 1
                    if count == 6:
                        return False


