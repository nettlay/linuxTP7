import Test_Script.addprinter as ad
import Test_Script.check_printer as cp
import Test_Script.common_function as co
from Test_Script import script_difference, script_general
from Test_Script.common_function import pass_report, fail_report
from Test_Script.addprinter import delete_printer, close_window


log = co.logger()


def run():
    desktop_list = ['citrix_win10.png']
    module_name = 'XenDesktop_Storefront_USB_printer_mapping'
    co.check_resolution()
    if not co.check_network_status():
        fail_report('Network status is not available', module_name)
        return
    if not cp.check_printer_by_system(module_name):
        return
    if cp.check_printers() > 0:
        log.info('clear printer')
        cp.clear_previous_printer()
    flag = ad.open_window('printer', "./Test_Data/1920x1200/template_file/printers_localhost.png")
    if flag:
        flag = ad.add_printer()
    else:
        return False
    if flag:
        ad.cancel_print_page()
        # ad.close_window("./Test_Data/1920x1200/template_file/printers_localhost.png")
        log.logger.info("Printer added successful.")
        flag = cp.check_printer_added()
    else:
        return False
    if flag:
        script_difference.set_citrix_usbprinter_mapping()
        flag = script_difference.login_storefront(desktop_list)
    else:
        return
    if flag is not True:
        fail_report(flag, module_name)
        delete_printer()
        close_window("./Test_Data/1920x1200/template_file/printers_localhost.png")
        return False
    mapping = script_difference.usbprinter_mapping()
    sign_out = script_general.check_succeed_signout()
    delete_printer()
    close_window("./Test_Data/1920x1200/template_file/printers_localhost.png")
    if mapping is not True:
        fail_report(mapping, module_name)
        return False
    if sign_out is not True:
        fail_report(sign_out, module_name)
        return False
    else:
        pass_report(module_name)


