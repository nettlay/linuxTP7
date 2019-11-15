from Test_Script import Get_screenshot as Gs
from Test_Script import Open_systeminfo as Os
from Test_Script import Close_Systeminfo as Cs


def run():
    Os.get_screensize()
    if Os.open_systeminfo():
        Gs.get_screenshot()
    else:
        return
    if Cs.close_window():
        return True
    else:
        return False
