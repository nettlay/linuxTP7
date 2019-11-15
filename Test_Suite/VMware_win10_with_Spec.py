from Test_Script import thinpro_view
from Test_Script import view_ftp
from Test_Script import common_function as report
from Test_Script import view_common_functions
from Test_Script import common_connection
import time
import os
from Test_Script import get_config


log_for_vmware_spec = report.logger()  # Create instance of log


def run_single(server_name, operation, name, password):
    case = thinpro_view.ViewSpec(server_name, name, password)
    name_in_config = get_config.get_config(name)
    common_connection.clear_connections("view")
    # case.del_vmware_in_task_bar()  # Delete vmware in task bar if exists
    # case.del_connection()
    # If vmware view exists in task bar, kill the process of vmware.
    max_loc = case.image_match('vmware_in_task_bar', 1)
    if max_loc is not None:
        os.popen('pkill vmware')
        vm_process = os.popen("ps -A | grep vmware").readlines()
        if len(vm_process) == 0:
            log_for_vmware_spec.info("Kill process for vmware successfully.")
    case.create_connection()
    if name == 'spec_username2':
        username = case.edit_connection_spec2()
    else:
        username = case.edit_connection()
    if username != name_in_config:
        # report.fail_report('edit connection fail', test_name)
        log_for_vmware_spec.error('%s for user %s.' % (username, name_in_config))
        return '%s for user %s.' % (username, name_in_config)
    # change viewSecurityLevel to "All all connections" in registry
    # path of vmware in registry: "root/ConnectionType/view/connections"
    view_common_functions.change_view_sec_allow_all("root/ConnectionType/view/connections")
    case.start_connection()
    connect = case.log_on_desktop_spec()
    if connect is not True:
        if connect == 'desktop_unavailable':
            return 'desktop_unavailable'
        # report.fail_report(connect, test_name)
        log_for_vmware_spec.error('%s for user %s.' % (connect, name_in_config))
        return '%s for user %s.' % (connect, name_in_config)
    confirm_result = view_ftp.confirm_username(username)
    if confirm_result is False:
        case.logon_fail()
        # report.fail_report('not confirm username', test_name)
        log_for_vmware_spec.error('not confirm username %s' % name_in_config)
        return 'not confirm username %s' % name_in_config
    view_ftp.upload_test(operation)
    result = view_ftp.confirm_result()
    if result is False:
        case.logon_fail()
        log_for_vmware_spec.error("Not find test result for user %s." % name_in_config)
        return "Not find test result for user %s." % name_in_config
    elif result.lower() == 'pass':
        if case.check_logoff() is True:
            # report.pass_report(test_name)     # Only report failed users
            return True
        else:
            log_for_vmware_spec.error('VDI test success,logoff fail for user %s.' % name_in_config)
            # return 'VDI test success,logoff fail for user %s.' % name_in_config
            return 'logoff_fail'
    else:
        if case.check_logoff() is True:
            # report.fail_report('VDI test fail', test_name)
            log_for_vmware_spec.error('VDI test fail for user %s : %s' % (name_in_config, result))
            return 'VDI test fail for user %s : %s' % (name_in_config, result)
        else:
            log_for_vmware_spec.error('VDI test fail and logoff fail for user %s: %s' % (name_in_config, result))
            return 'VDI test fail and logoff fail for user %s: %s' % (name_in_config, result)


def run():
    test_case_name = "vmware_spec"
    credentials = {
        'spec_username1': 'spec_password1',
        'spec_username2': 'spec_password2',
        'spec_username3': 'spec_password3',
        'spec_username4': 'spec_password4',
        'spec_username5': 'spec_password5',
        'spec_username6': 'spec_password6'
    }
    list_fail = []
    index = 1
    for name, password in credentials.items():
        # common_connection.clear_connections("view")    # Delete vmware viewer connections if exist
        result = run_single('spec_server_name_%s' % index, '//15.83.240.98/Automation/Linux/scripts/logoff.exe', name,
                            password)
        if result is not True:
            # If previous user doesn't logoff normally, exit the iteration and stop testing.
            if result == 'logoff_fail':
                report.fail_report(
                    'Previous user %s is not logoff normally, please check whether the remote desktop is '
                    'available or not. Testing stops.' % name, test_case_name)
                return
            elif result == 'desktop_unavailable':
                report.fail_report('Remote desktop is unavailable now. Please check the environment. Testing will '
                                   'stop.', test_case_name)
                return
            list_fail.append(result)
        time.sleep(30)  # Waif sometime for next login to avoid resource unavailable issue.
        index = index + 1
    if len(list_fail) == 0:
        report.pass_report(test_case_name)
    else:
        report.fail_report(list_fail, test_case_name)


