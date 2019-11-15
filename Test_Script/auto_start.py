from Lib.my_ftp import MyFtp
from win32com.client import Dispatch
import os
import subprocess
import getpass
import time
import logging


shell = Dispatch("Wscript.Shell")
env_path = shell.ExpandEnvironmentStrings("%HOMEPATH%")
temp_folder = 'C:'+'\\test_temp'
if not os.path.exists('C:\\log'):
    os.mkdir('C:\\log')
myftp = MyFtp("15.83.240.98", "sh\\automation", "Shanghai2014")
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


def clear_folder(root):
    """
    remove all files and sub-folders in a folder
    :param root: the folder path
    :return:
    """
    try:
        for root, dirs, files in os.walk(root, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))

            for name in dirs:
                os.rmdir(os.path.join(root, name))
    except OSError:
        mylogger.error('clear_folder', exc_info=True)


def run(task_file):
    try:

        username = getpass.getuser()
        mylogger.info('upload username to ftp')
        myftp.upload_new_file(temp_folder+'\\documents', 'Automation\\Linux\\flags', 'username.txt', username)
        while True:
            local_scripts_path = temp_folder+'\\downloads'
            local_file = local_scripts_path + '\\' + task_file
            mylogger.info('waiting next task...')
            myftp.download_file('Automation\\Linux\\flags', local_scripts_path, task_file)
            if os.path.exists(local_file):
                mylogger.info('find %s' % local_file)
                with open(local_file)as f:
                    test_item_script_name = f.read()
            else:
                mylogger.info('failed to find %s' % local_file)
                myftp.upload_new_file(temp_folder+'\\documents', 'Automation\\Linux\\flags', 'test_result.txt',
                                      'Failed')

                return
            if not test_item_script_name:
                mylogger.info('the script file name is blank, something exception')
                myftp.upload_new_file(temp_folder + '\\documents', 'Automation\\Linux\\flags', 'test_result.txt',
                                      'Failed')
                myftp.upload_new_file(temp_folder + '\\documents', 'Automation\\Linux\\flags', 'test_result.txt',
                                      'Failed')
                return
            mylogger.info('succeed getting script file name %s' % test_item_script_name)
            file_name = test_item_script_name.split('/')[-1].strip()
            myftp.download_file('Automation\\Linux\\scripts', temp_folder + '\\scripts', file_name)
            time.sleep(10)
            mylogger.info('remove test_item.txt file from ftp and vdi session')
            myftp.delete_file('Automation\\Linux\\flags', task_file)
            if os.path.exists(temp_folder + '\\downloads\\' + task_file):
                os.remove(temp_folder + '\\downloads\\' + task_file)
            exe_file = temp_folder+'\\scripts\\'+file_name
            if os.path.exists(exe_file):
                mylogger.info('succeed download script file %s' % exe_file)
                mylogger.info('******************************************************')
                mylogger.info('execute %s script' % exe_file)
                subprocess.run(exe_file)
                # os.remove(exe_file)

            else:
                mylogger.info('failed to download script file %s' % exe_file)
                myftp.upload_new_file(temp_folder+'\\documents', 'Automation\\Linux\\flags', 'test_result.txt',
                                      'Failed')
    except LookupError:
        mylogger.error('run', exc_info=True)
    except OSError:
        mylogger.error('run', exc_info=True)


def main():
    mylogger.info('create following new folders:\n%s\n%s\n%s' % (temp_folder + '\\downloads',
                  temp_folder + '\\documents', temp_folder + '\\scripts'))
    if os.path.exists(temp_folder):
        clear_folder(temp_folder)
        os.mkdir(temp_folder + '\\downloads')
        os.mkdir(temp_folder + '\\documents')
        os.mkdir(temp_folder + '\\scripts')
        time.sleep(5)
        run('test_item.txt')
    else:
        os.mkdir(temp_folder)
        os.mkdir(temp_folder + '\\downloads')
        os.mkdir(temp_folder + '\\documents')
        os.mkdir(temp_folder + '\\scripts')
        time.sleep(5)
        run('test_item.txt')


if __name__ == '__main__':
    main()