from Test_Script import thinpro_view
from Test_Script import view_ftp
from Test_Script import certificate
from Test_Script import common_function as report
from Test_Script import get_config as gc


def run(server_name='rdp_server_name', operation='//15.83.240.98/Automation/Linux/scripts/logoff.exe'):
    test_name = 'VMware_win10_rdp'
    cer = certificate.Cert('ROOTCA')
    find_cert = cer.check_cert()
    if find_cert is False:
        insert = cer.import_cert()
        if insert is False:
            report.fail_report('import cert fail', test_name)
            return False
    print('cert already exist')
    name, password = 'username', 'password'
    case = thinpro_view.View(server_name, name, password)
    case.del_connection()
    case.create_connection()
    username = case.edit_connection()
    if username != gc.get_config(name):
        report.fail_report(username, test_name)
        return
    case.start_connection()
    connect = case.log_on_desktop()
    if connect is not True:
        report.fail_report(connect, test_name)
        return
    confirm_result = view_ftp.confirm_username(username)
    if confirm_result is False:
        case.logon_fail()
        report.fail_report('not find username.txt', test_name)
        return
    view_ftp.upload_test(operation)
    result = view_ftp.confirm_result()
    if result is False:
        case.logon_fail()
        report.fail_report('not find test_result.txt', test_name)
        return
    elif result.lower() == 'pass':
        if case.check_logoff() is True:
            report.pass_report(test_name)
            return
        else:
            report.fail_report('VDI test success,logoff fail', test_name)
            return
    else:
        if case.check_logoff() is True:
            report.fail_report('VDI test fail:%s' % result, test_name)
            return
        else:
            report.fail_report('VDI test fail:%s,and logoff fail' % result, test_name)
            return
