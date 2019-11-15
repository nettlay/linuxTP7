import datetime
import os
import sys
import time
import pyautogui
import logging


test_name = os.path.split(os.path.splitext(sys.argv[0])[0])[-1]
report_path = "./Test_Report/report.txt"


class logger:
    def __init__(self, set_level="debug",
                 name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
                 log_name=time.strftime("%Y-%m-%d"+".log", time.localtime()),
                 log_path="./Test_Report/log/",
                 use_console=True):
        '''
            set_level： 设置日志的打印级别，默认为DEBUG
            name： 日志中将会打印的name，默认为运行程序的name
            log_name： 日志文件的名字，默认为当前时间（年-月-日.log）
            log_path： 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
            use_console： 是否在控制台打印，默认为True
        '''
        if os.name == "nt":
            log_path = "C:\\log/"
        elif os.name == "posix":
            log_path = "./Test_Report/log/"
        self.logger = logging.getLogger(name)
        if set_level.lower() == "critical":
            self.logger.setLevel(logging.CRITICAL)
        elif set_level.lower() == "error":
            self.logger.setLevel(logging.ERROR)
        elif set_level.lower() == "warning":
            self.logger.setLevel(logging.WARNING)
        elif set_level.lower() == "info":
            self.logger.setLevel(logging.INFO)
        elif set_level.lower() == "debug":
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.NOTSET)
        if not self.logger.handlers:
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            log_file_path = log_path+''+log_name
            log_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            log_handler.setFormatter(logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s"))
            self.logger.addHandler(log_handler)
            if use_console:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s"))
                self.logger.addHandler(console_handler)

    def addHandler(self, hdlr):
        self.logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        self.logger.removeHandler(hdlr)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)


def pass_report(file_name='controller'):
    if not os.access(report_path, os.F_OK):
        with open(report_path, "w") as f:
            platform = os.popen("dmidecode | grep -i -A5 \"System Information\" | grep -i \"Product Name\" | cut -d: -f2").readlines()[0]
            tp_version = os.popen("cat /etc/imageid").readlines()[0].strip()
            sp_version = os.popen("dpkg -l | grep -i hptc-sp").readlines()
            if sp_version:
                sp_version1 = os.popen("dpkg -l | grep -i hptc-sp").readlines()[0].split(0)[2]
                image_version = tp_version + " service pack " + sp_version1
            else:
                image_version = tp_version
            f.writelines("Image Version: %s\n" % image_version)
            f.writelines("Test Platform: %s\n" % platform)
            f.writelines(" %s : PASS \n" % file_name)
    else:
        with open(report_path, "a") as f:
            f.writelines(" %s : PASS \n" % file_name)


def fail_report(detail, file_name='controller'):
    if not os.access(report_path, os.F_OK):
        with open(report_path, "w") as f:
            platform = os.popen("dmidecode | grep -i -A5 \"System Information\" | grep -i \"Product Name\" | cut -d: -f2").readlines()[0]
            tp_version = os.popen("cat /etc/imageid").readlines()[0].strip()
            sp_version = os.popen("dpkg -l | grep -i hptc-sp").readlines()
            if sp_version:
                sp_version1 = os.popen("dpkg -l | grep -i hptc-sp").readlines()[0].split(0)[2]
                image_version = tp_version + " service pack " + sp_version1
            else:
                image_version = tp_version
            f.writelines("Image Version: %s\n" % image_version)
            f.writelines("Test Platform: %s\n" % platform)
            f.writelines(" %s : FAIL : %s \n" % (file_name, detail))
    else:
        with open(report_path, "a") as f:
            f.writelines(" %s : FAIL : %s \n" % (file_name, detail))


def check_network_status():
    log = logger()
    network_status = os.popen("mclient get tmp/network/status | cut -d' ' -f2").readlines()[0]
    if int(network_status) == 1:
        log.info(" PASS: Network status available")
        return True
    elif int(network_status) == 0:
        log.info(" FAIL: Network status is not available")
        return False
    else:
        log.info("FAIL: Network status is abnormal")
        return False


def check_resolution():
    log = logger()
    x = pyautogui.size().width
    y = pyautogui.size().height
    resolution = "%s*%s" % (x, y)
    log.info(" Current resolution is %s*%s" % (x, y))
    return resolution

