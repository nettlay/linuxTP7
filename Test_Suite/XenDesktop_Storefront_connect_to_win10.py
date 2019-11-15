from Test_Script import script_difference
from Test_Script.common_function import pass_report, fail_report
import Test_Script.common_function as comfun


def run():
    module_name = 'XenDesktop_Storefront_connect_to_win10'
    desktop_list = ['citrix_win10.png']
    comfun.check_resolution()
    if not comfun.check_network_status():
        fail_report('Network status is not available', module_name)
        return
    flag = script_difference.login_storefront(desktop_list)
    if flag is not True:
        fail_report(flag, module_name)
        return False
    flag = script_difference.logoff()
    if flag is not True:
        fail_report(flag, module_name)
        return False
    else:
        pass_report(module_name)
