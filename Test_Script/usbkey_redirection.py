from win32com.client import Dispatch
import logging
from Lib.my_ftp import MyFtp
import os
import time


myftp = MyFtp("15.83.240.98", "sh\\automation", "Shanghai2014")
shell = Dispatch("Wscript.Shell")
env_path = shell.ExpandEnvironmentStrings("%HOMEPATH%")
temp_folder = 'C:'+'\\test_temp'
mylogger = logging.getLogger()
mylogger.setLevel(logging.DEBUG)
if not mylogger.handlers:
    file = 'C:\\log\\vdi_summary.log'
    fh = logging.FileHandler(filename=file)
    fh.setLevel(logging.INFO)
    fh_fmt = "%(asctime)s - %(levelname)s - %(message)s"
    datefmt = '%Y-%m-%d %H:%M:%S'
    fh_formatter = logging.Formatter(fh_fmt, datefmt)
    fh.setFormatter(fh_formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch_fmt = "%(asctime)s - %(levelname)s - %(message)s"
    ch_formatter = logging.Formatter(ch_fmt, datefmt)
    ch.setFormatter(ch_formatter)
    mylogger.addHandler(fh)
    mylogger.addHandler(ch)


def clear_folder(abs_path):
    """
    remove all files and sub-folders in a folder
    :param abs_path: the folder path
    :return:
    """
    for root, dirs, files in os.walk(abs_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def get_redirected_usbdrive():
    try:
        mylogger.info('search redirected USB key')
        time.sleep(10)
        usb_key = ''
        fso = Dispatch('Scripting.FileSystemObject')
        for i in range(30):
            for drive in fso.drives:
                if drive.DriveType == 1 and drive.IsReady:
                    mylogger.info('find the redirected USB Key')
                    usb_key = drive.Path+'/'
                    return usb_key
        if usb_key == '':
            mylogger.info('Cannot find the redirected USB Key')
    except Exception:
        mylogger.error('get_redirected_usbdrive', exc_info=True)


def copyfile_to_usb():
    try:
        src = temp_folder + "\\downloads\\transfer.txt"
        with open(src, 'w')as f:
            f.write('usbkey redirection test')
        fso = Dispatch("Scripting.FileSystemObject")
        des = fso.BuildPath(redirected_usb, "transfer_check.txt")
        fso.CopyFile(src, des, True)
        mylogger.info('delay 30s')
        time.sleep(30)
        if fso.FileExists(des):
            mylogger.info('find transfer_check.txt in usb key')
        else:
            mylogger.info('There has no file transfer.txt in USB key')
    except Exception:
        mylogger.error('copyfile_from_usb', exc_info=True)


def read_txt(file):
    try:
        with open(file)as f:
            content = f.read()
            return content
    except FileNotFoundError:
        mylogger.error('read_txt', exc_info=True)
    except OSError:
        mylogger.error('read_txt', exc_info=True)


def compare(file1, file2):
    try:
        content1 = read_txt(file1)
        content12 = read_txt(file2)
        if content1 == content12:
            mylogger.info('file transfer.txt in USB key is same with it on session')
            mylogger.info('Test passed')
            return True
        else:
            mylogger.info('file transfer.txt in USB key is not same with it on session')
            mylogger.info('Test failed')
            return False
    except FileNotFoundError:
        mylogger.error('compare', exc_info=True)
    except Exception:
        mylogger.error('compare', exc_info=True)


def run_usb_redirected():
    try:

        if redirected_usb:
            # mylogger.info('download transfer.txt from ftp to disk')
            # myftp.download_file('C:\\', 'Linux\\Log\\Citrix\\flags', temp_folder+'\\Downloads', 'transfer.txt')
            # mylogger.info('try to copy transfer.txt from disk to usb key')
            copyfile_to_usb()
        else:
            myftp.upload_new_file(temp_folder+'\\Documents', 'Automation\\Linux\\flags', 'test_result.txt', 'Failed')
            return
        fso = Dispatch("Scripting.FileSystemObject")
        transfer = temp_folder + '\\downloads\\transfer.txt'
        transfer_check = fso.BuildPath(redirected_usb, "transfer_check.txt")
        mylogger.info('try to compare files')
        compare_result = compare(transfer, transfer_check)
        if compare_result:
            myftp.upload_new_file(temp_folder+'\\documents', 'Automation\\Linux\\flags', 'test_result.txt', 'Passed')
        else:

            myftp.upload_new_file(temp_folder+'\\documents', 'Automation\\Linux\\flags', 'test_result.txt', 'Failed')
        # if fso.FileExists(transfer) and fso.FileExists(transfer_check):
        #     compare_result = compare(transfer, transfer_check)
        # else:
        #     myftp.upload_new_file('C:\\', temp_folder+'\\Documents', 'Linux/Log\\Citrix\\flags', 'case_status.txt', 'Failed')
        #     return
        # if compare_result:
        #
        #     myftp.upload_new_file('C:\\', temp_folder+'\\Documents', 'Linux\\Log\\Citrix\\flags', 'case_status.txt', 'Passed')
        # else:
        #
        #     myftp.upload_new_file('C:\\', temp_folder+'\\Documents', 'Linux\\Log\\Citrix\\flags', 'case_status.txt', 'Failed')
        # myftp.upload_existed_file('C:\\', '\\Users\\automation', 'Linux\\Log\\Citrix\\flags', 'usbkey_test.log')
    except FileNotFoundError:
        mylogger.error('run_usb_mapping', exc_info=True)
    except Exception:
        mylogger.error('run_usb_mapping', exc_info=True)


mylogger.info('*************************************')
mylogger.info('start to test usbkey redirection')

mylogger.info('clear %s, %s' % (temp_folder + '\\downloads', temp_folder + '\\documents'))
clear_folder(temp_folder + '\\downloads')
clear_folder(temp_folder + '\\documents')
redirected_usb = get_redirected_usbdrive()
run_usb_redirected()
mylogger.info('finish tested usbkey redirection')
mylogger.info('will log off connection in 10s')
myftp.upload_existed_file('C:\\log', 'Automation\\Linux\\logs', 'vdi_summary.log')
time.sleep(10)
os.popen('shutdown /l')
