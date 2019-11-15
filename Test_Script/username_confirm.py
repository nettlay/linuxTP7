import getpass
from ftplib import FTP
import os
import time
import yaml


def find_test():
    for i in range(100):
        file_list = ftp.nlst()
        if 'test.txt' in file_list:
            download = 'RETR ' + 'test.txt'
            file_test = open('test.txt', 'wb')
            ftp.retrbinary(download, file_test.write)
            file_test = open('test.txt', 'r')
            for line in file_test.readlines():
                content = line
            ftp.delete('test.txt')
            ftp.quit()
            os.startfile('c:\\temp\\%s.exe' % content)
            break
        if i == 99:
            ftp.delete('confirm.txt')
            os.startfile('c:\\temp\\test_fail.exe')
        time.sleep(1)


if __name__ == '__main__':
    file = 'view_configuration.yml'
    configuration = yaml.safe_load(open(file))
    ftp = FTP(configuration['ftp_server'])
    ftp.login(configuration['ftp_username'], configuration['ftp_password'])
    ftp.cwd('Linux/Log')
    files = ftp.nlst()
    if 'confirm.txt' in files:
        ftp.delete('confirm.txt')
    file_name = 'STOR ' + 'confirm.txt'
    path = os.path.dirname(__file__)
    file = open(path + '/confirm.txt', 'w')
    file.write(getpass.getuser())
    file.close()
    file = open(path + '/confirm.txt', 'rb')
    ftp.storbinary(file_name, file)
    file.close()
    time.sleep(5)
    find_test()
