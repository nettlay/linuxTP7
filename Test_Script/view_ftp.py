import os
import time
from ftplib import FTP
from Test_Script import get_config as gc


def confirm_username(username):
    ftp = FTP(gc.get_config('ftp_server'))
    ftp.login(gc.get_config('ftp_username'), gc.get_config('ftp_password'))
    ftp.cwd('Automation/Linux/flags')
    i = 180
    while i:
        files = ftp.nlst()
        if 'username.txt' in files:
            file_name = 'RETR ' + 'username.txt'
            file = open('username.txt', 'wb')
            ftp.retrbinary(file_name, file.write)
            file.close()
            file = open('username.txt', 'r')
            for line in file.readlines():
                content = line
                if content == username:
                    print('log on success')
                    ftp.delete('username.txt')
                    file.close()
                    os.remove('username.txt')
                    ftp.quit()
                    return True
                else:
                    ftp.delete('username.txt')
                    ftp.quit()
                    return False
        else:
            time.sleep(1)
            i = i-1
            if i == 0:
                ftp.quit()
                return False


def confirm_result():
    ftp = FTP(gc.get_config('ftp_server'))
    ftp.login(gc.get_config('ftp_username'), gc.get_config('ftp_password'))
    ftp.cwd('Automation/Linux/flags')
    i = 200
    while i:
        files = ftp.nlst()
        if 'test_result.txt' in files:
            file_name = 'RETR ' + 'test_result.txt'
            file = open('test_result.txt', 'wb')
            ftp.retrbinary(file_name, file.write)
            file = open('test_result.txt', 'r')
            for line in file.readlines():
                content = line
                if content.lower() == 'passed':
                    file.close()
                    os.remove('test_result.txt')
                    ftp.delete('test_result.txt')
                    ftp.quit()
                    return 'PASS'
                else:
                    file.close()
                    os.remove('test_result.txt')
                    ftp.delete('test_result.txt')
                    ftp.quit()
                    return content
        else:
            time.sleep(1)
            i = i-1
            if i == 0:
                ftp.quit()
                return False


def upload_test(operation):
    ftp = FTP(gc.get_config('ftp_server'))
    ftp.login(gc.get_config('ftp_username'), gc.get_config('ftp_password'))
    ftp.cwd('Automation/Linux/flags')
    files = ftp.nlst()
    if 'test_item.txt' in files:
        ftp.delete('test_item.txt')
    file_name = 'STOR ' + 'test_item.txt'
    file = open('test_item.txt', 'w')
    file.write(operation)
    file.close()
    file = open('test_item.txt', 'rb')
    ftp.storbinary(file_name, file)
    file.close()
    ftp.quit()
    os.remove('test_item.txt')
