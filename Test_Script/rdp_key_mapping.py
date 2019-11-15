import os
from win32com.client import Dispatch
import logging
import time
import sys
import yaml
import datetime
from ftplib import FTP


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


def get_mapped_usb_key():
    try:
        log.info('search mapped USB key')
        usb_key = ''
        net = Dispatch('Wscript.network')
        mapped_drives = net.EnumNetworkDrives()
        for j in range(10):
            for i in range(0, mapped_drives.length, 2):
                mapped_usb_key = mapped_drives.Item(i+1)
                if mapped_usb_key:
                    log.info('find the mapped USB Key')
                    usb_key = mapped_usb_key+'/'
                    return usb_key
        if usb_key == '':
            log.error('Cannot find the mapped USB Key')
    except Exception:
        log.error('get_mapped_usb_key', exc_info=True)


def copyfile_to_usb():
        fso = Dispatch("Scripting.FileSystemObject")
        src = "C:\\scripts\\usb_mapping.txt"
        des = fso.BuildPath(get_mapped_usb_key(), "usb_mapping_check.txt")
        if os.path.exists(src):
            os.remove(src)
        if os.path.exists(des):
            os.remove(des)
        text = "1234567890!@#$%^&*()qwertyuiopQWERTYUIOP"
        os.system("echo {} > C:\\scripts\\usb_mapping.txt".format(text))
        fso.CopyFile(src, des, True)
        log.info("copying usb_mapping.txt to USB key")
        return


def get_content(file):
    try:
        with open(file)as f:
            content = f.read()
            return content
    except FileNotFoundError:
        log.error('read_txt', exc_info=True)
    except Exception:
        log.error('read_txt', exc_info=True)


def compare(file1, file2):
    try:
        content1 = get_content(file1)
        content12 = get_content(file2)
        if content1 == content12:
            return True
        else:
            return False
    except FileNotFoundError:
        log.error('compare', exc_info=True)
    except Exception:
        log.error('compare', exc_info=True)


def upload_log():
    today = datetime.date.today()
    ftp.storbinary("STOR %s.log" % today, open("C:\\scripts\\log\\%s.log" % today, "rb"), 1024)


def run_usb_mapping():
    try:
        if get_mapped_usb_key():
            copyfile_to_usb()
            fso = Dispatch("Scripting.FileSystemObject")
            usb_mapping = "C:\\scripts\\usb_mapping.txt"
            usb_mapping_check = fso.BuildPath(get_mapped_usb_key(), "usb_mapping_check.txt")
            if fso.FileExists(usb_mapping) and fso.FileExists(usb_mapping_check):
                compare_result = compare(usb_mapping, usb_mapping_check)
                log.info('comparing files')
                if compare_result:
                    log.info("pass, two files are the same")
                    with open("C:\\scripts\\rdp_test.txt")as f:
                        data = f.read()
                    os.system("echo {}_PASS>C:\\scripts\\rdp_test_result.txt".format(data))
                    ftp.storbinary("STOR %s" % "rdp_test_result.txt", open("C:\\scripts\\rdp_test_result.txt", "rb"),
                                   1024)
                    upload_log()
                    log.info("test complete, will sign out in 10 seconds")
                    time.sleep(10)
                    os.system("shutdown -l")
                    return True
                else:
                    log.error("fail, two files are different")
                    with open("C:\\scripts\\rdp_test.txt")as f:
                        data = f.read()
                    os.system("echo {}_FAIL>C:\\scripts\\rdp_test_result.txt".format(data))
                    ftp.storbinary("STOR %s" % "rdp_test_result.txt", open("C:\\scripts\\rdp_test_result.txt", "rb"),
                                   1024)
                    upload_log()
                    log.info("test complete, will sign out in 10 seconds")
                    time.sleep(10)
                    os.system("shutdown -l")
                    return False
            else:
                log.error("fail, can't start comparison")
                with open("C:\\scripts\\rdp_test.txt")as f:
                    data = f.read()
                os.system("echo {}_FAIL>C:\\scripts\\rdp_test_result.txt".format(data))
                ftp.storbinary("STOR %s" % "rdp_test_result.txt", open("C:\\scripts\\rdp_test_result.txt", "rb"), 1024)
                upload_log()
                log.info("test complete, will sign out in 10 seconds")
                time.sleep(10)
                os.system("shutdown -l")
                return False
        else:
            return False
    except FileNotFoundError:
        log.error('run_usb_mapping', exc_info=True)
    except Exception:
        log.error('run_usb_mapping', exc_info=True)


log = logger()
test_folder = "C:\\scripts"
with open("C:\\scripts\\rdp_config.yml") as f:
    data = yaml.safe_load(f)
server_name = data["FTP_Server"]
username = data["Username"]
password = data["Password"]
path = data["rdp_file_path"]
ftp = FTP(server_name)
ftp.login(username, password)
ftp.cwd(path)

run_usb_mapping()
