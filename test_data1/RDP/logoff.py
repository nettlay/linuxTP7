import os
import ruamel.yaml as yaml
import ftplib


class LogOff:
    def __init__(self):
        self.config_path = 'c:/scripts/rdp_config.yml'
        # self.config_path = 'rdp_config.yml'
        self.ftp_server = ''
        self.username = ''
        self.password = ''
        self.domain = ''
        self.rdp_file_path = ''

    def load_ftp_info(self):
        with open(self.config_path) as f:
            content = yaml.safe_load(f)
        self.ftp_server = content['FTP_Server']
        self.username = content['Username']
        self.password = content['Password']
        self.domain = content['Domain']
        self.rdp_file_path = content['rdp_file_path']

    def download_test_file(self, filename):
        self.load_ftp_info()
        ftp = ftplib.FTP(self.ftp_server)
        ftp.login(r'{}\{}'.format(self.domain, self.username), self.password)
        ftp.cwd(self.rdp_file_path)
        # files = ftp.nlst()
        # print(files)
        ftp.retrbinary('RETR rdp_test.txt', open(filename, 'wb').write, 1024)
        print('Download rdp_test.txt pass')
        ftp.quit()

    def upload_result(self, filename):
        self.load_ftp_info()
        ftp = ftplib.FTP(self.ftp_server)
        ftp.login(r'{}\{}'.format(self.domain, self.username), self.password)
        ftp.cwd(self.rdp_file_path)
        files = ftp.nlst()
        print(files)
        ftp.storbinary('STOR rdp_test_result.txt'.format(filename), open(filename, 'rb'), 1024)
        ftp.quit()

    def logoff(self):
        self.download_test_file('c:\\scripts\\rdp_test.txt')
        with open('c:/scripts/rdp_test.txt', 'r') as f:
            data = f.read()
        os.system('echo {}_PASS > c:\\scripts\\rdp_test_result.txt'.format(data))
        self.upload_result('c:\\scripts\\rdp_test_result.txt')
        if os.path.exists('c:/scripts/rdp_test.txt'):
            os.remove('c:/scripts/rdp_test.txt')
        if os.path.exists('rdp_test_result'):
            os.remove('rdp_test_result')
        os.system('shutdown -l')

LogOff().logoff()