from ftplib import FTP
import yaml
import os
import sys
import time
import logging
#from Test_Script.common_function import *
# root = os.getcwd()
# parent_root = os.path.split(root)[0]



class logger:
    def __init__(self, set_level="debug",
                 name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
                 log_name=time.strftime("%Y-%m-%d.log", time.localtime()),
                 # log_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "log"),
                 log_path="C:\\SCRIPTS\\log",
                 use_console=True):
        '''
            set_level： 设置日志的打印级别，默认为DEBUG
            name： 日志中将会打印的name，默认为运行程序的name
            log_name： 日志文件的名字，默认为当前时间（年-月-日.log）
            log_path： 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
            use_console： 是否在控制台打印，默认为True
        '''
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
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_file_path = os.path.join(log_path, log_name)
        log_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        log_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(log_handler)
        if use_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
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


def get_config():
    with open("C:\SCRIPTS\\rdp_config.yml", "r") as f:
        rdp_config = yaml.load(f.read(), Loader=yaml.FullLoader)
    return rdp_config


def get_test_name():
    server_name = get_config()["FTP_Server"]
    username = get_config()["Username"]
    password = get_config()["Password"]
    rdp_file_path = get_config()["rdp_file_path"]
    ftp = FTP(server_name)
    ftp.login(username, password)
    ftp.cwd(rdp_file_path)
    # require_test_name get from test_name.txt，uploaded by TC
    ftp.retrbinary("RETR %s" % "rdp_test.txt", open("C:\scripts\\rdp_test.txt", "wb").write, 1024)
    ftp.delete("rdp_test.txt")

def execute_test():
    get_test_name()
    with open("C:\scripts\\rdp_test.txt", "r") as f:
        test_name = f.read().strip()
        print(test_name)
    if test_name in get_config()["Test Name"]:
        current_test_name = get_config()["Test Name"][test_name]
        # print(current_test_name)
        os.system(current_test_name)
        log.info("current test is %s" % test_name)
        log.info("start to execute test case")
    else:
        print("can't find file to execute")


log = logger()
execute_test()