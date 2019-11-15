from ftplib import FTP
import time
import yaml


config_yml_path = './Test_Data/config.yml'
configuration = yaml.safe_load(open(config_yml_path))


class MyFtp:

    def __init__(self, ip=configuration['ftp_server'],
                 user=configuration['ftp_username'],
                 password=configuration['ftp_password']):
        self.ip = ip
        self.user = user
        self.password = password

    def upload_new_file(self, local_abs_path, ftp_rel_path, file_name, content):
        ftp = FTP(self.ip)
        ftp.login(self.user, self.password)
        ftp.cwd(ftp_rel_path)
        file_list = ftp.nlst()
        if file_name in file_list:
            ftp.delete(file_name)
        cmd = 'STOR ' + file_name
        local_file = local_abs_path + '\\' + file_name
        with open(local_file, 'w')as f:
            f.write(content)
        with open(local_file, 'rb')as fp:
            ftp.storbinary(cmd, fp)
        ftp.quit()

    def upload_existed_file(self, root, local_rel_path, ftp_rel_path, file_name):

        ftp = FTP(self.ip)
        ftp.login(self.user, self.password)
        ftp.cwd(ftp_rel_path)
        file_list = ftp.nlst()
        if file_name in file_list:
            ftp.delete(file_name)
        cmd = 'STOR ' + file_name
        local_file = root+local_rel_path + '/' + file_name
        with open(local_file, 'rb')as fp:
            ftp.storbinary(cmd, fp)
        ftp.quit()

    def download_file(self, ftp_rel_path, local_abs_path, file_name):

        ftp = FTP(self.ip)
        ftp.login(self.user, self.password)
        ftp.cwd(ftp_rel_path)
        for i in range(180):
            file_list = ftp.nlst()
            if file_name in file_list:
                cmd = 'RETR ' + file_name
                local_file = local_abs_path + '\\' + file_name
                with open(local_file, 'wb')as fp:
                    ftp.retrbinary(cmd, fp.write)
                    ftp.quit()
                    return True# if run ftp.quit(), we should exit cycle, else error will raise
            else:
                time.sleep(1)

    def delete_file(self, ftp_rel_path, file_name):
        ftp = FTP(self.ip)
        ftp.login(self.user, self.password)
        ftp.cwd(ftp_rel_path)
        file_list = ftp.nlst()
        if file_name in file_list:
            ftp.delete(file_name)


