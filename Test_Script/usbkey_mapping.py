from win32com.client import Dispatch
# from Lib.my_logger import mylogger
from Lib.my_ftp import MyFtp
import os
import time
import logging


shell = Dispatch("Wscript.Shell")
env_path = shell.ExpandEnvironmentStrings("%HOMEPATH%")
temp_folder = 'C:' + '\\test_temp'
myftp = MyFtp("15.83.240.98", "sh/automation", "Shanghai2014")
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


def get_mapped_usbdrive():
    """
    All the even-indexed elements in the collection are local names,
    while all the odd-indexed elements in the collection are remote names.
    The first item in the collection is at index zero (0).
    Further, the elements are paired (0 and 1 are the first drive, 2 and 3 are the second drive, etc.)
    :return:
    """
    try:
        mylogger.info('search mapped USB key')
        usb_key = ''
        net = Dispatch('Wscript.network')
        for j in range(30):
            mapped_drives = net.EnumNetworkDrives()
            for i in range(0, mapped_drives.length, 2):
                mylogger.info('local_name: %s'%mapped_drives.Item(i))
                mylogger.info('remote_name: %s'%mapped_drives.Item(i+1))
                mappeddrive = mapped_drives.Item(i+1)
                if mappeddrive:
                    mylogger.info('find the mapped USB Key: %s' % mappeddrive)
                    usb_key = mappeddrive+'/'
                    return usb_key
            time.sleep(1)
        if usb_key == '':
            mylogger.info('Cannot find the mapped USB Key')
    except LookupError:
        mylogger.error('get_mappeddrive', exc_info=True)
    except OSError:
        mylogger.error('get_mappeddrive', exc_info=True)


def copyfile_to_usb():
    try:
        src = temp_folder + "\\downloads\\transfer.txt"
        with open(src, 'w')as f:
            f.write('usbkey mapping test')
        fso = Dispatch("Scripting.FileSystemObject")
        des = fso.BuildPath(mapped_usb, "transfer_check.txt")
        fso.CopyFile(src, des, True)
        mylogger.info('delay 30s')
        time.sleep(30)
        if fso.FileExists(des):
            mylogger.info('find transfer_check in usb key')
        else:
            mylogger.info('There has no file transfer.txt in USB key')
    except LookupError:
        mylogger.error('copyfile_to_usb', exc_info=True)
    except OSError:
        mylogger.error('copyfile_to_usb', exc_info=True)


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
    except OSError:
        mylogger.error('compare', exc_info=True)


def run_usb_mapping():
    try:
        if mapped_usb:
            # mylogger.info('download transfer.txt from ftp to disk')
            # myftp.download_file('C:\\', 'Automation\\Linux\\flags', temp_folder+'\\downloads', 'transfer.txt')
            # mylogger.info('try to copy transfer.txt from usb key to disk')
            copyfile_to_usb()
        else:
            myftp.upload_new_file(temp_folder+'\\documents', 'Automation\\Linux\\flags', 'test_result.txt', 'Failed')
            return
        # fso = Dispatch("Scripting.FileSystemObject")
        fso = Dispatch("Scripting.FileSystemObject")
        transfer = temp_folder + '\\downloads\\transfer.txt'
        transfer_check = fso.BuildPath(mapped_usb, "transfer_check.txt")
        mylogger.info('try to compare files')
        compare_result = compare(transfer, transfer_check)
        if compare_result:
            myftp.upload_new_file(temp_folder+'\\documents', 'Automation\\Linux\\flags', 'test_result.txt', 'Passed')
        else:

            myftp.upload_new_file(temp_folder+'\\documents', 'Automation\\Linux\\flags', 'test_result.txt', 'Failed')

    except FileNotFoundError:
        mylogger.error('run_usb_mapping', exc_info=True)
    except OSError:
        mylogger.error('run_usb_mapping', exc_info=True)


mylogger.info('*************************************')
mylogger.info('start to test usbkey mapping')

mylogger.info('clear %s, %s' % (temp_folder + '\\downloads', temp_folder + '\\documents'))
clear_folder(temp_folder + '\\downloads')
clear_folder(temp_folder + '\\documents')
mapped_usb = get_mapped_usbdrive()
run_usb_mapping()
mylogger.info('finish tested usbkey mapping')
mylogger.info('will log off connection in 10s')
myftp.upload_existed_file('C:\\log', 'Automation\\Linux\\logs', 'vdi_summary.log')
time.sleep(10)
os.popen('shutdown /l')