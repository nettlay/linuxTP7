import time
import Lib.main_function as mf
from Test_Script import common_function as comfun
from Test_Script.call_main_function import execute_main_function

log = comfun.logger()


def run():
    time.sleep(3)
    execute_main_function()
    try:
        mf.ftp_link_test()
    except Exception:
        comfun.fail_report("The automated server connection may fail due to network failure!!! ")
    mf.execute_testing_program()
    mf.delete_file()
    mf.ftp_upload_report()
    mf.ftp_upload_screenshot()
    mf.ftp_upload_log()


if __name__ == '__main__':
    run()


