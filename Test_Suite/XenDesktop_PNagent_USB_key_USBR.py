from Test_Script import script_general, script_difference
from Test_Script.common_function import pass_report, fail_report
import Test_Script.common_function as comfun


def run():
    desktop_list = ['citrix_win10_pnagent.png']
    module_name = 'XenDesktop_PNagent_USB_key_USBR'
    comfun.check_resolution()
    if not comfun.check_network_status():
        fail_report('Network status is not available', module_name)
        return
    flag = script_general.check_localusb_exist()
    if flag:
        script_general.remove_usb_file()
        script_difference.set_citrix_usbkey_usbr()
    else:
        fail_report('can not find local usb key', module_name)
        return False
    flag = script_difference.login_pnagent(desktop_list)
    if flag is not True:
        fail_report(flag, module_name)
        return False
    usbr = script_difference.xen_usbkey_redirection()
    sign_out = script_general.check_succeed_signout()
    if usbr is not True:
        fail_report(usbr, module_name)
        return False
    if sign_out is not True:
        fail_report(sign_out, module_name)
        return False
    flag = script_difference.confirm_usbkeyredirection_file()
    if flag is not True:
        fail_report(flag, module_name)
        return False
    else:
        pass_report(module_name)