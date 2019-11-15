import Test_Script.common_function as comfun
from Test_Script import xd_storefront_smartcard
from Test_Script.rdp_smart_card_logon import *


def run():
    test_name = 'XenDesktop_Storefront_win10_smartcard'
    desktop_list = ['xd_smartcard_win10.png']
    comfun.check_resolution()
    if not comfun.check_network_status():
        fail_report('Network status is not available', test_name)
        return
    if xd_storefront_smartcard.login_storefront_smartcard(desktop_list):
        result = NormalLogonTest()
        result.record_result(test_name)
        os.popen('pkill -f CitrixApps')
        return False


