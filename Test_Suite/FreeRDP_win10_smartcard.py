from Test_Script.rdp_smart_card_logon import *


def run():
    try:
        test = SmartcardTest()
        test_name = "FreeRDP_win10_smartcard"
        if test.smartcard_logon("rfx_win10", test_name):
            test.record_result(test_name)
    except Exception as e:
        log.error(e)
