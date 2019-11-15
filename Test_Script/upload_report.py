import os
from Test_Script import my_ftp
import time


def upload_result(result):    # the result is supposed to write as "Passed" or "Failed"
    try:
        ftp_work_path = "Automation\\Linux\\flags"
        file_name = "test_result.txt"
        doc_path = "C:\\test_temp\\documents\\"
        ftp = my_ftp.MyFtp()
        ftp.upload_new_file(doc_path, ftp_work_path, file_name, result)
    except Exception as e:
        print(e)


def upload_log():
    try:
        ftp = my_ftp.MyFtp()
        local_rel_path = "C:\\log\\"
        ftp_rel_path = "Automation\\Linux\\logs"
        file_name = time.strftime("%Y-%m-%d" + ".log")
        ftp.upload_existed_file(local_rel_path, ftp_rel_path, file_name)
    except Exception as e:
        print(e)
