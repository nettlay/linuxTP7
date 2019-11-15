from Test_Script import thinpro_view
from Test_Script import certificate
from Test_Script import view_ftp
from Test_Script import common_function as report
from Test_Script import get_config
import pyautogui as pag
import time
import os


connect_with_cert = 'VMware_Connect_with_Certificate'
cert_server_name, cert_name, cert_password = 'pcoip_server_name', 'username', 'password'
case = thinpro_view.View(cert_server_name, cert_name, cert_password)


def run():
    username = get_config.get_config(cert_name)
    cert = certificate.Cert('ROOTCA')
    find_cert = cert.check_cert()
    if find_cert is False:
        insert = cert.import_cert()
        if insert is False:
            report.fail_report('import cert fail', connect_with_cert)
            return False
    print('cert already exist')
    if create_connection() is False:
        return False
    warning = logon(username)
    if warning is not True:
        test_report('select security to be warning:'+warning+'-------')
    edit_connection('allow')
    allow = logon(username)
    if allow is not True:
        test_report('select security to be allow:'+allow+'-------')
    edit_connection('refuse')
    refuse = logon(username)
    if refuse is not True:
        test_report('select security to be refuse:'+refuse+'-------')
    if cert.delete_cert() is False:
        test_report('del cert fail,end refuse test without cert test')
        a = ''
        with open('./Test_Report/%s.txt' % connect_with_cert, 'r') as file:
            for line in file.readlines():
                a += line
        report.fail_report(a, connect_with_cert)
        os.remove('./Test_Report/%s.txt' % connect_with_cert)
        return
    if refuse_connect() is False:
        test_report('not find refuse window after delete cert')
    a = ''
    try:
        with open('./Test_Report/%s.txt' % connect_with_cert, 'r') as file:
            for line in file.readlines():
                a += line
        report.fail_report(a, connect_with_cert)
        os.remove('./Test_Report/%s.txt' % connect_with_cert)
    except:
        report.pass_report(connect_with_cert)


def logon(username):
    operation = '//15.83.240.98/Automation/Linux/scripts/logoff.exe'
    case.start_connection()
    connect = case.log_on_desktop()
    if connect is not True:
        return connect
    confirm_result = view_ftp.confirm_username(username)
    if confirm_result is False:
        case.logon_fail()
        return 'logon fail,not find username.txt'
    view_ftp.upload_test(operation)
    result = view_ftp.confirm_result()
    if result is False:
        case.logon_fail()
        return 'not find test_result.txt'
    elif result.lower() == 'pass':
        if case.check_logoff() is True:
            return True
        else:
            return 'VDI test success,logoff fail'
    else:
        if case.check_logoff() is True:
            return 'VDI test fail:%s' % result
        else:
            return 'VDI test fail:%s,and logoff fail' % result


def create_connection():
    case.del_connection()
    case.create_connection()
    username = case.edit_connection()
    if username != get_config.get_config(cert_name):
        report.fail_report(username, connect_with_cert)
        return False


def edit_connection(policy):
    max_loc = case.image_match('view_icon', 3)
    pag.rightClick(max_loc)
    pag.press('down', presses=2, interval=0.1)
    pag.press('enter')
    time.sleep(5)
    max_loc = case.image_match('Security', 3)
    pag.click(max_loc)
    time.sleep(1)
    pag.press('tab', presses=9, interval=0.1)
    pag.press('space')
    if policy == 'allow':
        pag.press('up', presses=2, interval=0.1)
    elif policy == 'refuse':
        pag.press('down', presses=2, interval=0.1)
    pag.press('enter')
    pag.click(case.image_match('ok', 3))


def refuse_connect():
    icon = case.image_match('view_icon', 3)
    pag.rightClick(icon)
    pag.press('down')
    pag.press('enter')
    time.sleep(15)
    max_loc = case.image_match('refuse', 5)
    if max_loc is None:
        return False
    time.sleep(1)
    pag.press('space')
    time.sleep(2)
    pag.hotkey('ctrl', 'alt', 'f4')


def test_report(result):
    with open('./Test_Report/%s.txt' % connect_with_cert, 'a') as file:
        file.write(result)
