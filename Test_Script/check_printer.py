import subprocess
import os
import time
import glob
import Test_Script.common_function as co
import Test_Script.addprinter as ad


log = co.logger()


def check_printer_by_system(testname):
    # get the /dev/usb/lp* character devices's number
    printer_path = '/dev/usb/lp*'
    for i in range(1, 5):
        if glob.glob(printer_path):
            printer_num=glob.glob(printer_path)
            for p in printer_num:
                log.info("Pass: Detect USB printer {} by system".format(p))
            return True
        else:
            if i < 4:
                disable_usb_ports()
                enable_usb_ports()
            else:
                log.info("Fail: No USB Printer have been detected by system.")
                co.fail_report("No USB Printer have been detected by system.", testname)


def check_printers():
    added_printers = 0
    printer_list = [subprocess.getoutput('mclient --quiet get root/printerwd')]
    for printer in printer_list:
        printer = os.path.basename(printer)
        if len(printer) != 0 and printer != "Default":
            log.info(printer + " has been added in the system")
            added_printers += 1
    return added_printers


def clear_previous_printer():
    count_clear_time = 0
    if operate_delete_printer():
        check_printers()
        if check_printers() == 0:
            log.info("Pass: Previous added printers have all been cleared")
            return
        else:
            if count_clear_time < 2:
                operate_delete_printer()
                count_clear_time += 1
            elif count_clear_time == 2:
                log.info("Fail: Previous added printer can not clean up")


def check_printer_added():
    check_printers()
    if check_printers() >= 0:
        log.info("Pass: Detect USB Printer has been added")
        return True
    elif check_printers() == 0:
        log.info("Fail: USb Printer has not been added")


def operate_delete_printer():
    if ad.open_window('printer', "./Test_Data/1920x1200/template_file/printers_localhost.png"):
        i = 1
        while i <= check_printers():
            ad.delete_printer()
    if ad.close_window("./Test_Data/1920x1200/template_file/printers_localhost.png"):
        return True
    else:
        return False


def disable_usb_ports():
    path = subprocess.getoutput('ls -d /sys/bus/usb/devices/usb*').split('\n')
    for item in path:
        os.system('echo 0 >{}/authorized'.format(item))
    time.sleep(10)
    return True


def enable_usb_ports():
    path = subprocess.getoutput('ls -d /sys/bus/usb/devices/usb*').split('\n')
    for item in path:
        os.system('echo 1 >{}/authorized'.format(item))
    time.sleep(10)
    if ad.close_usbupdate_window():
        return True
    else:
        return False

