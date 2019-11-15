import pyautogui as pg
from Test_Script.rdp_utils import *
import yaml
from Test_Script.common_function import *

log = logger()


class LogonTest:
    def __init__(self):
        screen_size = pg.size()
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.logon = RDPUtil()
        self.config_file = './Test_Data/RDP_Config.yml'
        self.logon_flag = False
        with open(self.config_file, 'r') as f:
            try:
                self.data = yaml.safe_load(f)
            except:
                log.error('read configuration.ymal Exception')
            self.ftp_server = self.data['FTP_Server']
            self.username = self.data['Username']
            self.password = self.data['Password']
            self.domain = self.data['Domain']
            self.rdp_servers = self.data['RDP_Server']
            self.rdp_file_path = self.data['rdp_file_path']
            self.normal_rdp_logon = self.data["test_item"]["rdp_normal_logon"]
            # print(self.normal_rdp_logon)
            # all server should be prepared before test
            self.rect_offsets = self.data['Offset_Map']
            #  all offset based top_left point rect

    # def get_config(self):
    #     with open(self.config_file, 'r') as f:
    #         try:
    #             data = yaml.safe_load(f)
    #         except:
    #             print('read configuration.ymal Exception')
    #         # print(data)
    #         self.ftp_server = data['FTP_Server']
    #         self.username = data['Username']
    #         self.password = data['Password']
    #         self.domain = data['Domain']
    #         self.rdp_servers = data['RDP_Server']
    #         self.rdp_file_path = data['rdp_file_path']
    #         # all server should be prepared before test
    #         self.rect_offsets = data['Offset_Map']
    #         #  all offset based top_left point rect

    def create_new_connection(self):
        pg.rightClick(self.width - 10, 10)
        pg.press('down', interval=0.2)
        pg.press('right', interval=0.2)
        pg.press('down', interval=0.2)
        pg.press('enter', interval=0.2)
        time.sleep(1)

    def get_point_from_config(self, point=(0, 0), item=""):
        """
        Point-picture-offset mapping: under RDP_Config.yml->Offset_Map
        if last 2 value of list is integer, just operate the offset from the base position
        if last 2 value is not integer, find the all the pictures on screen
        :return (x,y) position of item
        :point Base for offset
        :item element name
        """
        config = self.data['Offset_Map'][item]
        if isinstance(config[-1], int) and isinstance(config[-2], int):
            rect = self.logon.rect_offset(point, (config[-2], config[-1]))
        else:
            rect = self.logon.wait_element(self.data['Offset_Map'][item])
        return rect

    def edit_connection(self, profile):
        """
        profile: server name | username | password | domain
        profile position: RDP_config.yml->RDP_Test-> test1 | test2 ...
        """
        # -----------------------------------------------------------------
        #       Get test profile contains username|password|domain|server
        # -------------------------------------------------------------------
        connection = self.data[profile]['Server']
        server_address = self.data['RDP_Server'][connection]
        username = self.data[profile]['Username']
        password = self.data[profile]['Password']
        domain = self.data[profile]['Domain']
        # ==================Get RDP Icon on Desktop and Edit It====================
        rdp_icon = self.get_point_from_config(item='rdp_icon')
        if rdp_icon is None:
            log.error('No RDP icon in desktop.., will create')
            self.create_new_connection()
            rdp_icon = self.get_point_from_config(item='rdp_icon')
        pg.rightClick(rdp_icon)
        time.sleep(1)
        pg.press('down', presses=2, interval=0.1)
        time.sleep(0.2)
        pg.press('enter', interval=1)
        time.sleep(5)
        # ==========wait edit connection dialog============
        log.info('wait edit window')
        top_left = self.get_point_from_config(item='top_left')
        # ----------------------------------------------------------------
        #       Get element rect base top_left's position
        # ----------------------------------------------------------------
        connection_name = self.get_point_from_config(top_left, 'connection_name')
        address = self.get_point_from_config(top_left, 'address')
        user_password = self.get_point_from_config(top_left, 'user_password')
        username_box = self.get_point_from_config(top_left, 'username_box')
        password_box = self.get_point_from_config(top_left, 'password_box')
        domain_box = self.get_point_from_config(top_left, 'domain_box')
        # ok_button = self.get_point_from_config(top_left, 'ok_button')
        ok_button = self.get_point_from_config(item='ok_button')
        # ================= create connection according test profiles ==============
        pg.click(connection_name, interval=0.2)
        pg.press('backspace', presses=30)
        pg.typewrite(connection)
        pg.click(address, interval=0.2)
        pg.press('backspace', presses=30)
        pg.typewrite(server_address)
        pg.click(user_password, interval=0.2)
        pg.click(username_box)
        pg.press('backspace', presses=30)
        pg.typewrite(username)
        pg.click(password_box)
        pg.press('backspace', presses=30)
        pg.typewrite(password)
        pg.click(domain_box)
        pg.press('backspace', presses=10)
        pg.typewrite(domain)
        time.sleep(5)
        pg.click(ok_button)
        return True

    def del_connection(self):
        while 1:
            rdp_icon = self.get_point_from_config(item='rdp_icon')
            if rdp_icon is None:
                break
            else:
                pg.rightClick(rdp_icon)
                pg.press('down', presses=5, interval=0.2)
                pg.press('enter', interval=0.2)
                time.sleep(1)

    def start_connection(self):
        rdp_icon = self.get_point_from_config(item='rdp_icon')
        pg.rightClick(rdp_icon)
        time.sleep(0.5)
        pg.press('down', interval=0.2)
        pg.press('enter')
        return True

    def stop_connection(self):
        rdp_icon_active = self.get_point_from_config(item='rdp_icon_active')
        pg.hotkey('ctrlleft', 'altleft', 'end')
        time.sleep(3)
        pg.rightClick(rdp_icon_active)
        time.sleep(0.5)
        pg.press('down', interval=0.2)
        pg.press('enter')
        return True

    def stop_connection_taskbar(self):
        pg.hotkey('ctrlleft', 'altleft', 'end')
        time.sleep(3)
        rdp_taskbar = self.logon.wait_element(["Test_Data/RDP/rdp_active_icon_taskbar_0_0.png"])
        if rdp_taskbar:
            pg.rightClick(rdp_taskbar)
            time.sleep(1)
            pg.press("up", interval=0.2)
            time.sleep(1)
            pg.press("enter")
            return True
        else:
            log.error("can't find rdp icon in taskbar")
            return False

    def kill_process(self, process_name):
        session = os.popen('ps -ef | grep %s' % process_name).read()
        if session:
            os.popen('pkill -f %s' % process_name)
            # kill process for one time, will get black window in remote log on screen.
            # kill twice to make sure this process be killed.
            os.popen('pkill -f %s' % process_name)
            log.info("kill process")
            return True
        else:
            log.info("process does not exist")
            return False

    def login(self, server, test_name):
        self.edit_connection(server)
        self.start_connection()
        # ////get ftp and check if flag file exist, if exist delete it//////
        ftp = self.logon.get_ftp(self.ftp_server, self.username, self.password)
        ftp.cwd(self.rdp_file_path)
        # -----------------------------------------------------------
        #    Check FTP server is rdp_test.txt and rdp_test_result.txt
        #    Exist, delete them
        # -----------------------------------------------------------
        files = ftp.nlst()
        if 'test_item.txt' in files:
            ftp.delete('test_item.txt')
        if 'test_result.txt' in files:
            ftp.delete('test_result.txt')
        # -------------------------------------------------------------------------
        # Create temp file rdp_test.txt with content rdp_normal_logon
        # This content's format is pre-defined, rdp_[test item]
        # rdp_test_result.txt content's format: rdp_[test item]_[result](PASS/FAIL)
        # -------------------------------------------------------------------------
        exe_location = self.normal_rdp_logon
        with open("test_item.txt", "w") as f:
            f.write(exe_location)
        RDPUtil().upload_ftp(ftp, 'test_item.txt')
        os.remove('test_item.txt')
        time.sleep(10)
        cert_accept_button = self.get_point_from_config(item='rdp_certificate_accept')
        if cert_accept_button:
            pg.click(cert_accept_button)
            for i in range(180):
                files = ftp.nlst()
                if 'test_result.txt' in files:
                    RDPUtil().download_ftp(ftp, 'test_result.txt')
                    with open('test_result.txt') as f:
                        rs = f.read()
                    if "Pass" in rs:
                        self.logon_flag = True
                        ftp.delete('test_result.txt')
                        os.remove('test_result.txt')
                        ftp.quit()
                        log.info("test pass")
                        pass_report(test_name)
                    elif "Fail" in rs:
                        fail_report(rs, test_name)
                        log.error(rs)
                    else:
                        fail_report("result status unknown", test_name)
                        log.error("result status unknown")
                    return self.logon_flag
                else:
                    log.info("waiting for test_result.txt...")
                    process = os.popen('ps -ef | grep RDP\\ Client\\ Error | grep -v grep').read()
                    if process:
                        log.error("get error window")
                        log.info("will kill freerdp process and RDP Client Error process")
                        self.kill_process("freerdp")
                        self.kill_process("RDP\\ Client\\ Error")
                        return self.logon_flag
                    time.sleep(1)
                    continue
            if not self.logon_flag:
                # 1. check error dialog
                # 2. if no dialog, logon timeout, force stop connection
                log.error("Connection Failed or can't find exe to execute in remote desktop")
                fail_report("Connection Failed or can't find exe to execute in remote desktop", test_name)
                self.kill_process("freerdp")
                return False
        else:
            log.error('No accept window pops up , program exit')
            fail_report('No accept window pops up , program exit', test_name)
            self.kill_process("freerdp")
            self.kill_process("RDP\\ Client\\ Error")
        time.sleep(30)
        # -----------------------------------------------------------------
        #  watching ftp server, check if rdp_test_result uploaded by TC
        # -----------------------------------------------------------------

    def login_rfx(self, server):
        self.edit_connection(server)
        self.start_connection()
        # ////get ftp and check if flag file exist, if exist delete it//////
        ftp = self.logon.get_ftp(self.ftp_server, self.username, self.password)
        ftp.cwd(self.rdp_file_path)
        # -----------------------------------------------------------
        #    Check FTP server is rdp_test.txt and rdp_test_result.txt
        #    Exist, delete them
        # -----------------------------------------------------------
        # -------------------------------------------------------------------------
        # Create temp file rdp_test.txt with content rdp_normal_logon
        # This content's format is pre-defined, rdp_[test item]
        # rdp_test_result.txt content's format: rdp_[test item]_[result](PASS/FAIL)
        # -------------------------------------------------------------------------
        time.sleep(10)
        cert_accept_button = self.get_point_from_config(item='rdp_certificate_accept')
        if cert_accept_button:
            pg.click(cert_accept_button)
            return True
        else:
            reason = 'No accept window pops up , program exit'
            log.error(reason)
            return reason


# Added by Lena
class LogonTestSpec(LogonTest):
    def __init__(self, profile):
        self.profile = profile
        LogonTest.__init__(self)

    def edit_connection_spec(self, profile):
        """
        profile: server name | username | password | domain
        profile position: RDP_config.yml->RDP_Test-> test1 | test2 ...
        """
        # -----------------------------------------------------------------
        #       Get test profile contains username|password|domain|server
        # -------------------------------------------------------------------
        connection = self.data[profile]['Server']
        server_address = self.data['RDP_Server'][connection]
        username = self.data[profile]['Username']
        password = self.data[profile]['Password']
        domain = self.data[profile]['Domain']
        # ==================Get RDP Icon on Desktop and Edit It====================
        # -----------modified by Lena. If there is no connection of freerdp in Registry, then there is no freerdp.-----
        # rdp_icon = self.get_point_from_config(item='rdp_icon')
        connections_rdp = os.popen("mclient --quiet get root/ConnectionType/freerdp/connections").readlines()
        # if rdp_icon is None:
        if len(connections_rdp) == 0:
            print('No RDP icon in desktop..')
            self.create_new_connection()
            # rdp_icon = self.get_point_from_config(item='rdp_icon')
        rdp_icon = self.get_point_from_config(item='rdp_icon')
        pg.rightClick(rdp_icon)
        time.sleep(1)
        pg.press('down', presses=2, interval=0.1)
        time.sleep(0.2)
        pg.press('enter', interval=1)
        time.sleep(5)
        # ==========wait edit connection dialog============
        print('wait edit window')
        top_left = self.get_point_from_config(item='top_left')
        # ----------------------------------------------------------------
        #       Get element rect base top_left's position
        # ----------------------------------------------------------------
        connection_name = self.get_point_from_config(top_left, 'connection_name')
        address = self.get_point_from_config(top_left, 'address')
        user_password = self.get_point_from_config(top_left, 'user_password')
        username_box = self.get_point_from_config(top_left, 'username_box')
        password_box = self.get_point_from_config(top_left, 'password_box')
        domain_box = self.get_point_from_config(top_left, 'domain_box')
        # ok_button = self.get_point_from_config(top_left, 'ok_button')
        ok_button = self.get_point_from_config(item='ok_button')

        # ================= create connection according test profiles ==============
        pg.click(connection_name, interval=0.2)
        pg.press('backspace', presses=30)
        pg.typewrite(connection)
        pg.click(address, interval=0.2)
        pg.press('backspace', presses=30)
        pg.typewrite(server_address)
        pg.click(user_password, interval=0.2)
        pg.click(username_box)
        pg.press('backspace', presses=30)
        pg.typewrite(username)
        pg.click(password_box)
        pg.press('backspace', presses=30)
        if profile == 'RDP_Logon_SpecUser2':
            # Input spec password for spec user 2
            pg.typewrite('+=_,-?', interval=0.1)
            pg.hotkey('shift', ',')  # Input '<'
            pg.typewrite('>~', interval=0.1)
        else:
            pg.typewrite(password)
        pg.click(domain_box)
        pg.press('backspace', presses=10)
        pg.typewrite(domain)
        time.sleep(5)
        pg.press('tab', presses=6)  # modified by Lena
        pg.hotkey('space')
        pg.click(ok_button)
        return True

    def login_spec(self, server, test_name):
        self.edit_connection_spec(server)
        self.start_connection()
        # ////get ftp and check if flag file exist, if exist delete it//////
        ftp = self.logon.get_ftp(self.ftp_server, self.username, self.password)
        ftp.cwd(self.rdp_file_path)
        # -----------------------------------------------------------
        #    Check FTP server is rdp_test.txt and rdp_test_result.txt
        #    Exist, delete them
        # -----------------------------------------------------------
        files = ftp.nlst()
        if 'test_item.txt' in files:
            ftp.delete('test_item.txt')
        if 'test_result.txt' in files:
            ftp.delete('test_result.txt')
        # -------------------------------------------------------------------------
        # Create temp file rdp_test.txt with content rdp_normal_logon
        # This content's format is pre-defined, rdp_[test item]
        # rdp_test_result.txt content's format: rdp_[test item]_[result](PASS/FAIL)
        # -------------------------------------------------------------------------
        exe_location = self.normal_rdp_logon
        with open("test_item.txt", "w") as f:
            f.write(exe_location)
        RDPUtil().upload_ftp(ftp, 'test_item.txt')
        os.remove('test_item.txt')
        time.sleep(10)
        cert_accept_button = self.get_point_from_config(item='rdp_certificate_accept')
        if cert_accept_button:
            pg.click(cert_accept_button)
            for i in range(180):
                files = ftp.nlst()
                if 'test_result.txt' in files:
                    RDPUtil().download_ftp(ftp, 'test_result.txt')
                    with open('test_result.txt') as f:
                        rs = f.read()
                    if "Pass" in rs:
                        self.logon_flag = True
                        ftp.delete('test_result.txt')
                        os.remove('test_result.txt')
                        ftp.quit()
                        log.info("test pass")
                        # pass_report(test_name)    # Only Report failed users
                    elif "Fail" in rs:
                        fail_report(rs, test_name)
                        log.error(rs)
                    else:
                        fail_report("result status unknown", test_name)
                        log.error("result status unknown")
                    return self.logon_flag
                else:
                    log.info("waiting for test_result.txt...")
                    process = os.popen('ps -ef | grep RDP\\ Client\\ Error | grep -v grep').read()
                    if process:
                        log.error("get error window")
                        log.info("will kill freerdp process and RDP Client Error process")
                        self.kill_process("freerdp")
                        self.kill_process("RDP\\ Client\\ Error")
                        return self.logon_flag
                    time.sleep(1)
                    continue
            if not self.logon_flag:
                # 1. check error dialog
                # 2. if no dialog, logon timeout, force stop connection
                log.error("Connection Failed or can't find exe to execute in remote desktop")
                fail_report("Connection Failed or can't find exe to execute in remote desktop", test_name)
                self.kill_process("freerdp")
                return False
        else:
            log.error('No accept window pops up , program exit')
            fail_report('No accept window pops up , program exit', test_name)
            self.kill_process("freerdp")
            self.kill_process("RDP\\ Client\\ Error")
        time.sleep(30)
        return True
        # -----------------------------------------------------------------
        #  watching ftp server, check if rdp_test_result uploaded by TC
        # -----------------------------------------------------------------
