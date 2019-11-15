import Test_Script.rdp_logon as rdp_logon
import pyautogui as pg
import os
import traceback


def run():
    pg.hotkey('ctrl', 'altleft', 'end')
    # current_root = os.path.dirname(__file__)
    # root = os.path.dirname(current_root)
    logon = rdp_logon.LogonTest()
    test_name = "FreeRDP_rfx_win10"
    try:
        print(logon.login('RDP_Logon_Win10', test_name))
    except Exception as e:
        traceback.print_exc()
        print("Error", e)
