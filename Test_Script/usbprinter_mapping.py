from win32com.client import Dispatch
import logging
from Lib.my_ftp import MyFtp
import os
import time
import subprocess


myftp = MyFtp("15.83.240.98", "sh/automation", "Shanghai2014")
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


def get_mapped_usbprinter():
    try:
        mylogger.info('search mapped USB printer')
        net = Dispatch('Wscript.network')
        for j in range(10):
            mapped_printers = net.EnumPrinterConnections()
            for i in range(0, mapped_printers.length-1, 2):
                print('printer %s, resource_name: %s---printer_name: %s' % (str(i), mapped_printers.Item(i), mapped_printers.Item(i+1)))
                if ('CLIENT' in mapped_printers.Item(i).upper() or 'TS' in mapped_printers.Item(i).upper()) and (
                        'HP LaserJet P3010'.upper() in mapped_printers.Item(i+1).upper() or 'HP-LaserJet-P3010'.upper() in mapped_printers.Item(i+1).upper()):
                    mylogger.info('find the mapped USB printer: %s' % mapped_printers.Item(i+1))
                    mylogger.info('find the mapped USB printer port: %s' % mapped_printers.Item(i))
                    net.SetDefaultPrinter(mapped_printers.Item(i+1))
                    return mapped_printers.Item(i+1)
            time.sleep(1)
        mylogger.info('Cannot find the mapped USB Printer')
    except LookupError:
        mylogger.error('get_mapped_usbprinter', exc_info=True)
    except OSError:
        mylogger.error('get_mapped_usbprinter', exc_info=True)


def run_usbprinter_mapping():
    printer = get_mapped_usbprinter()
    if printer:
        mylogger.info('print a page')
        test_file = temp_folder+'\\documents\\username.txt'
        subprocess.run("notepad.exe /p %s" % test_file, shell=True)
    myftp.upload_new_file(temp_folder + '\\documents', 'Automation\\Linux\\flags', 'test_result.txt', 'Passed')
    mylogger.info('finish tested usbprinter mapping')
    mylogger.info('will log off connection in 10s')
    myftp.upload_existed_file('C:\log', 'Automation\\Linux\\logs', 'vdi_summary.log')
    time.sleep(10)
    os.popen('shutdown /l')


run_usbprinter_mapping()