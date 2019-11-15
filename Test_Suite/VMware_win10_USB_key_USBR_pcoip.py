from Test_Script import thinpro_view
from Test_Script import view_ftp
from Test_Script import certificate
import pyautogui as pag
import time
import os
from Test_Script import common_function as report
from Test_Script import get_config as gc


pcoip_usbr_log = report.logger()


def run(server_name='pcoip_server_name'):
    file_name = 'VMware_win10_USB_key_USBR_pcoip'
    local_usb = check_usb()
    if local_usb is not True:
        report.fail_report(local_usb, file_name)
        return False
    operation = '//15.83.240.98/Automation/Linux/scripts/usbkey_redirection.exe'
    cer = certificate.Cert('ROOTCA')
    find_cert = cer.check_cert()
    if find_cert is False:
        insert = cer.import_cert()
        if insert is False:
            report.fail_report('import cert fail', file_name)
            return False
        pcoip_usbr_log.info('import cert success for %s' % file_name)
    name, password = 'username', 'password'
    case = thinpro_view.View(server_name, name, password)
    case.del_connection()
    case.create_connection()
    username = case.edit_connection()
    if username != gc.get_config(name):
        report.fail_report(username, file_name)
        return False
    enable_usbr = edit_connection(case)
    if enable_usbr is not True:
        report.fail_report(enable_usbr, file_name)
        return False
    case.start_connection()
    connect = case.log_on_desktop()
    if connect is not True:
        report.fail_report(connect, file_name)
        return False
    confirm_result = view_ftp.confirm_username(username)
    if confirm_result is False:
        case.logon_fail()
        report.fail_report('not confirm username', file_name)
        return False
    view_ftp.upload_test(operation)
    result = view_ftp.confirm_result()
    time.sleep(10)
    if result is False:
        case.logon_fail()
        report.fail_report('not find test_result.txt', file_name)
        return
    elif result.lower() == 'pass':
        if case.check_logoff() is True:
            file_check = check_file()
            if file_check is not True:
                report.fail_report('VDI test success,%s' % file_check, file_name)
                return False
            report.pass_report(file_name)
            return True
        else:
            file_check = check_file()
            if file_check is not True:
                report.fail_report('VDI test success,logoff fail,%s' % file_check, file_name)
                return False
            report.fail_report('VDI test success,logoff fail,check file exist on local', file_name)
            return True
    else:
        if case.check_logoff() is True:
            report.fail_report('VDI test fail:%s' % result, file_name)
            return False
        else:
            report.fail_report('VDI test fail:%s, and log off fail' % result, file_name)


def edit_connection(case):
    icon = case.image_match('view_icon', 3)
    pag.rightClick(icon)
    pag.press('down', presses=2, interval=0.1)
    pag.press('enter')
    time.sleep(8)
    window = case.image_match('view_edit', 3)
    if window is None:
        pcoip_usbr_log.error('not find edit connection window')
        return 'not find edit connection window'
    pag.press('down')
    usb_r = case.image_match('view_usbr', 3)
    if usb_r is None:
        pcoip_usbr_log.error('not find usbr settings')
        pag.hotkey('ctrl', 'alt', 'f4')
        return 'not find usbr settings'
    pag.click(usb_r)
    time.sleep(1)
    pag.press('down')
    pag.press('space')
    time.sleep(1)
    pag.press('down')
    pag.press('space')
    time.sleep(1)
    pag.click(case.image_match('ok', 3))
    pcoip_usbr_log.info('enable usbr settings')
    return True


def check_usb():
    if len(os.popen('ls /media').readlines()) == 0:
        pcoip_usbr_log.error('not find usb key')
        return 'not find usb key'
    return True


def check_file():
    try:
        usb_name = os.popen('ls /media').readlines()[0].strip()
    except:
        return 'not find usb key'
    if 'transfer_check.txt\n' not in os.popen('ls /media/%s' % usb_name).readlines():
        pcoip_usbr_log.error('file not exist after logoff')
        return 'file not exist after logoff'
    file = open('/media/%s/transfer_check.txt' % usb_name, 'r')
    for line in file.readlines():
        if line == 'usbkey redirection test':
            file.close()
            os.remove('/media/%s/transfer_check.txt' % usb_name)
            pcoip_usbr_log.info('usbr test success,copy file to usb success')
            return True
        else:
            file.close()
            os.remove('/media/%s/transfer_check.txt' % usb_name)
            pcoip_usbr_log.error('the content of file is incorrect')
            return 'the content of file is incorrect'
