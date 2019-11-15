import os
from Test_Script import upload_report
from Test_Script import common_function
import time

upload_report.upload_result("Passed")
log = common_function.logger()
log.info("test pass, will sign out in 10 seconds")
upload_report.upload_log()
time.sleep(10)
os.system("shutdown -l")

