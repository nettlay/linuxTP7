from Test_Script import certificate
from Test_Script import common_function as report


def run(cert='ROOTCA'):
    test_name = 'Verify_can_add_certificate'
    cer = certificate.Cert(cert)
    find_cert = cer.check_cert()
    if find_cert is True:
        delete = cer.delete_cert()
        if delete is False:
            report.fail_report('Fail:remove cert fail before execute test', test_name)
            return False
    insert = cer.import_cert()
    if insert is False:
        report.fail_report('Fail:import cert fail', test_name)
        return False
    delete = cer.delete_cert()
    if delete is False:
        report.fail_report('Fail:remove cert fail', test_name)
        return False
    report.pass_report(test_name)
    return True
