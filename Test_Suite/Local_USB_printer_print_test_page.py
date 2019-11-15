import pyautogui
import Test_Script.addprinter as ad
import Test_Script.check_printer as cp
import Test_Script.common_function as co


def run():
    log = co.logger()
    testname = "Local_USB_printer_print_test_page"
    pyautogui.hotkey('ctrl', 'alt', 'end')
    co.check_resolution()
    co.check_network_status()
    if not cp.check_printer_by_system(testname):
        return
    if cp.check_printers() > 0:
        cp.clear_previous_printer()
    flag = ad.open_window('printer', "./Test_Data/1920x1200/template_file/printers_localhost.png")
    if flag:
        flag = ad.add_printer()
    else:
        return False
    if flag:
        log.logger.info("Printer added successful.")
        flag = cp.check_printer_added()
    else:
        return False
    if flag:
        ad.print_page()
        flag = ad.delete_printer()
    else:
        return False
    if flag:
        log.logger.info("Printer deleted successful.")
        ad.close_window("./Test_Data/1920x1200/template_file/printers_localhost.png")
        return True
    else:
        return False



