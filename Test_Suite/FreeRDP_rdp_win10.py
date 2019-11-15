import Test_Script.rdp_logon as rdp_logon
import pyautogui as pg
import traceback


def run():
    pg.hotkey('ctrl', 'altleft', 'end')
    logon = rdp_logon.LogonTest()
    test_name = "FreeRDP_rdp_Win10"
    try:
        print(logon.login('FreeRDP_Logon_Win10', test_name))
    except Exception as e:
        traceback.print_exc()
        print("Error", e)
