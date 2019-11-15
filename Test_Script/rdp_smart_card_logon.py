import pyautogui as pg
from Test_Script.rdp_utils import *
import yaml
from Test_Script.common_function import *
from ftplib import FTP

log = logger()


class NormalLogonTest:
    def __init__(self):
        screen_size = pg.size()
        self.width = screen_size[0]
        self.height = screen_size[1]
        # self.root = root
        # self.parent_root = parent_root
        # print(self.root)
        # print("parent root", parent_root)
        self.logon = RDPUtil()
        self.config_file = os.path.join('./Test_Data/RDP_Config.yml')
        print(self.config_file)
        self.get_config()
        self.logon_flag = False

    def get_config(self):
        with open(self.config_file, 'r') as f:
            try:
                data = yaml.safe_load(f)
                # print(data)
                self.ftp_server = data['FTP_Server']
                self.username = data['Username']
                self.password = data['Password']
                self.domain = data['Domain']
                # self.smartcard_driver_path = data['smartcard_driver_path']
                # self.smartcard_driver_name = data['smartcard_driver_name']
                self.rdp_server = data['RDP_Server']
                self.rdp_file_path = data['rdp_file_path']
                # all server should be prepared before test
                self.rect_offsets = data['Offset_Map']
                self.rdp_smartcard_logon = data["test_item"]["rdp_smartcard_logon"]
                #  all offset based top_left point rect
            except:
                print('read configuration.ymal Exception')
                pass

    def create_new_connection(self):
        pg.rightClick(self.width - 10, 10)
        pg.press('down', interval=0.2)
        pg.press('right', interval=0.2)
        pg.press('down', interval=0.2)
        pg.press('enter', interval=0.2)
        time.sleep(1)
    # ==========These functions write for new smartcard testing ==========

    # def open_x_term(self):
    #     pg.hotkey('ctrl', 'alt', 's')
    #     time.sleep(1)
    #     pg.typewrite('xterm', interval=0.2)
    #     time.sleep(1)
    #     pg.press('enter')
    #
    # def download_smartcard_driver(self):
    #     ftp = MyFtp(self.ftp_server, self.username, self.password)
    #     ftp.download_file(self.root, self.smartcard_driver_path, '/Test_Data', self.smartcard_driver_name)
    #
    # def install_smartcard_driver(self):
    #     self.download_smartcard_driver()
    #     time.sleep(2)
    #     self.open_x_term()
    #     time.sleep(5)
    #     # go to /Test_Data
    #     pg.typewrite('cd %s' % os.path.join(self.root, 'Test_Data'), interval=0.2)
    #     pg.press('enter')
    #     time.sleep(2)
    #     # install driver
    #     pg.typewrite("fsunlock")
    #     pg.press('enter')
    #     time.sleep(2)
    #     pg.typewrite('dpkg -i %s' % self.smartcard_driver_name)
    #     pg.press('enter')
    #     time.sleep(8)

    def del_connection(self):
        while 1:
            rdp_icon = self.logon.wait_element(['Test_Data/RDP/rdp_icon_10_5.png',
                                                'Test_Data/RDP/rdp_icon1_10_5.png',
                                                'Test_Data/RDP/rdp_icon2_10_5.png',
                                                'Test_Data/RDP/rdp_icon3_10_5.png'])
            if rdp_icon is None:
                break
            else:
                pg.rightClick(rdp_icon)
                pg.press('down', presses=5, interval=0.2)
                pg.press('enter', interval=0.2)
                time.sleep(1)

    def start_connection(self):
        rdp_icon = self.logon.wait_element(['Test_Data/RDP/rdp_icon_10_5.png',
                                            'Test_Data/RDP/rdp_icon1_10_5.png',
                                            'Test_Data/RDP/rdp_icon2_10_5.png',
                                            'Test_Data/RDP/rdp_icon3_10_5.png'])
        pg.rightClick(rdp_icon)
        time.sleep(0.5)
        pg.press('down', interval=0.2)
        pg.press('enter')
        log.info('start RDP connection')
        return True

    def stop_connection(self):
        rdp_icon = self.logon.wait_element(['Test_Data/RDP/rdp_icon_active_10_5.png'])
        pg.hotkey('ctrlleft', 'altleft', 'end')
        time.sleep(3)
        pg.rightClick(rdp_icon)
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
            log.info("stop connection from taskbar")
            return True
        else:
            log.error("can't find rdp icon in taskbar")
            return False

    def edit_normal_connection(self, server):
        """
        server: logon server keys, server address can be found by it's value
                in RDP_Config.yml
        username: pre-defined in yml
        password: pre-defined in yml
        """
        rdp_icon = self.logon.wait_element(['Test_Data/RDP/rdp_icon_10_5.png',
                                            'Test_Data/RDP/rdp_icon1_10_5.png',
                                            'Test_Data/RDP/rdp_icon2_10_5.png',
                                            'Test_Data/RDP/rdp_icon3_10_5.png'])
        if rdp_icon is None:
            log.info('No RDP icon in desktop...creating new RDP connection')
            self.create_new_connection()
            rdp_icon = self.logon.wait_element(['Test_Data/RDP/rdp_icon_10_5.png',
                                                'Test_Data/RDP/rdp_icon1_10_5.png',
                                                'Test_Data/RDP/rdp_icon2_10_5.png',
                                                'Test_Data/RDP/rdp_icon3_10_5.png'])
        pg.rightClick(rdp_icon)
        time.sleep(1)
        pg.press('down', presses=2, interval=0.1)
        time.sleep(0.2)
        pg.press('enter', interval=1)
        time.sleep(3)
        # ==========wait edit connection dialog============
        print('wait RDP connection edit window')
        top_left = self.logon.wait_element(['Test_Data/RDP/rdp_title_0_0.png',
                                            'Test_Data/RDP/rdp_title1_0_0.png',
                                            'Test_Data/RDP/rdp_icon2_10_5.png',
                                            'Test_Data/RDP/rdp_icon3_10_5.png'])
        connection_name = self.logon.rect_offset(top_left, tuple(self.rect_offsets['connection_name']))
        print(connection_name)
        address = self.logon.rect_offset(top_left, tuple(self.rect_offsets['address']))
        user_password = self.logon.rect_offset(top_left, tuple(self.rect_offsets['user_password']))
        username_box = self.logon.rect_offset(top_left, tuple(self.rect_offsets['username_box']))
        password_box = self.logon.rect_offset(top_left, tuple(self.rect_offsets['password_box']))
        domain_box = self.logon.rect_offset(top_left, tuple(self.rect_offsets['domain_box']))
        # ok_button = self.logon.rect_offset(top_left, tuple(self.rect_offsets['ok_button']))
        ok_button = self.logon.wait_element(['Test_Data/RDP/rdp_ok_5_3.png'])
        pg.click(connection_name, interval=0.2)
        pg.press('backspace', presses=30)
        pg.typewrite(server)
        pg.click(address, interval=0.2)
        pg.press('backspace', presses=30)
        pg.typewrite(self.rdp_server[server])
        pg.click(user_password, interval=0.2)
        pg.click(username_box)
        pg.press('backspace', presses=30)
        pg.typewrite(self.username)
        pg.click(password_box)
        pg.press('backspace', presses=30)
        pg.typewrite(self.password)
        pg.click(domain_box)
        pg.press('backspace', presses=10)
        pg.typewrite(self.domain)
        time.sleep(2)
        pg.click(ok_button)
        return True

    def edit_smartcard_connection(self, server):
        """
        server: logon server keys, server address can be found by it's value
                in RDP_Config.yml
        username: pre-defined in yml
        password: pre-defined in yml
        """
        rdp_icon = self.logon.wait_element(['Test_Data/RDP/rdp_icon_10_5.png',
                                            'Test_Data/RDP/rdp_icon1_10_5.png',
                                            'Test_Data/RDP/rdp_icon2_10_5.png',
                                            'Test_Data/RDP/rdp_icon3_10_5.png'])
        if rdp_icon is None:
            print('No RDP icon in desktop, Creating RDP icon...')
            log.error('No RDP icon in desktop, Creating RDP icon...')
            self.create_new_connection()
            rdp_icon = self.logon.wait_element(['Test_Data/RDP/rdp_icon_10_5.png',
                                                'Test_Data/RDP/rdp_icon1_10_5.png',
                                                'Test_Data/RDP/rdp_icon2_10_5.png',
                                                'Test_Data/RDP/rdp_icon3_10_5.png'])
        # ==========choose edit RDP connection==========
        pg.rightClick(rdp_icon)
        time.sleep(1)
        pg.press('down', presses=2, interval=0.1)
        time.sleep(0.2)
        pg.press('enter', interval=1)
        # ==========wait edit connection dialog==========
        print('wait RDP Connection Manager window...')
        log.info('wait RDP Connection Manager window...')
        time.sleep(5)
        # ==========Enter Connection name, address, choose to use smartcard to logon==========
        log.info('Enter Connection name, address, choose to use smartcard to logon')
        top_left = self.logon.wait_element(['Test_Data/RDP/rdp_title_0_0.png',
                                            'Test_Data/RDP/rdp_title1_0_0.png'])
        connection_name = self.logon.rect_offset(top_left, tuple(self.rect_offsets['connection_name']))
        # print(connection_name)
        address = self.logon.rect_offset(top_left, tuple(self.rect_offsets['address']))
        pg.click(connection_name, interval=0.2)
        pg.press('backspace', presses=30)
        pg.typewrite(server)
        pg.click(address, interval=0.2)
        pg.press('backspace', presses=30)
        pg.typewrite(self.rdp_server[server])
        # ==========choose use smartcard to log in==========
        smartcard = self.logon.wait_element(['Test_Data/RDP/smart_card_10_5.png'])
        pg.click(smartcard)
        time.sleep(2)
        # ok_button = self.logon.rect_offset(top_left, tuple(self.rect_offsets['ok_button']))
        ok_button = self.logon.wait_element(['Test_Data/RDP/rdp_ok_5_3.png'])
        pg.click(ok_button)
        return True

    def check_smartcard_exist(self):
        pass

    def click_accept_button(self):
        cert_accept_button = self.logon.wait_element(['Test_Data/RDP/rdp_certificate_accept_5_5.png',
                                                      'Test_Data/RDP/rdp_accept1_5_5.png'])
        if cert_accept_button:
            pg.click(cert_accept_button)
            log.info('click accept button')
        else:
            log.error('No accept window pops up, program exit')
            return False
        time.sleep(15)

    def upload_test_item_exe_location(self, location):
        with open('./Test_Data/test_item.txt', "w") as f:
            f.write(location)
        ftp = FTP(self.ftp_server)
        ftp.login(self.username, self.password)
        ftp.cwd(self.rdp_file_path)
        ftp.storbinary('STOR %s' % "test_item.txt", open('./Test_Data/test_item.txt', 'rb'))
        os.remove('./Test_Data/test_item.txt')
        if "test_result.txt" in ftp.nlst():
            ftp.delete("test_result.txt")

    def record_result(self, test_name):
        for i in range(180):
            ftp = FTP(self.ftp_server)
            ftp.login(self.username, self.password)
            ftp.cwd(self.rdp_file_path)
            files = ftp.nlst()
            # ==========check test_result.txt exist, if yes record result to report.txt==========
            if "test_result.txt" in files:
                self.logon_flag = True
                log.info("remote desktop logon successfully")
                log.info("get result from FTP")
                ftp.retrbinary("RETR %s" % "test_result.txt", open(os.path.join("./Test_Report/test_result.txt" ),"wb").write, 1024)
                with open(os.path.join("./Test_Report/test_result.txt"), "r") as f:
                    result = f.read()
                if "Pass" in result:
                    pass_report(test_name)
                    log.info("test pass")
                elif "Fail" in result:
                    fail_report(result, test_name)
                    log.error(result)
                else:
                    fail_report("result status unknown", test_name)
                    log.error("result status unknown")
                os.remove("./Test_Report/test_result.txt")
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
            log.error('Connection Failed')
            log.error("Failed to logon remote desktop or can't find exe to execute in remote desktop")
            fail_report("Failed to logon remote desktop or can't find exe to execute in remote desktop", test_name)
            self.kill_process("freerdp")
            return False

    def kill_process(self, process_name):
        session = os.popen('ps -ef | grep %s' % process_name).read()
        if session:
            os.popen('pkill -f %s' % process_name)
            time.sleep(3)
            # kill process for one time, will get black window in remote log on screen.
            # kill twice to make sure this process be killed.
            os.popen('pkill -f %s' % process_name)
            log.info("kill process")
            return True
        else:
            log.info("process does not exist")
            return False

    def close_usb_update_window(self):
        usb_window = self.logon.wait_element(['Test_Data/RDP/USB_Update_window_0_0.png'])
        cancel_icon = self.logon.wait_element(['Test_Data/RDP/USB_Update_cancel_0_0.png'])
        if usb_window:
            pg.click(cancel_icon)

    def set_key_usbr(self):
        rdp_icon = self.logon.wait_element(['Test_Data/RDP/rdp_icon_10_5.png',
                                            'Test_Data/RDP/rdp_icon1_10_5.png',
                                            'Test_Data/RDP/rdp_icon2_10_5.png',
                                            'Test_Data/RDP/rdp_icon3_10_5.png'])
        # ==========choose edit RDP connection==========
        pg.rightClick(rdp_icon)
        time.sleep(1)
        pg.press('down', presses=2, interval=0.1)
        time.sleep(0.2)
        pg.press('enter', interval=1)
        # ==========wait edit connection dialog==========
        log.info('wait RDP Connection Manager window...')
        time.sleep(2)

        top_left = self.logon.wait_element(['Test_Data/RDP/rdp_title_0_0.png',
                                            'Test_Data/RDP/rdp_title1_0_0.png'])
        local_resources = self.logon.rect_offset(top_left, tuple(self.rect_offsets['local_resources']))
        pg.click(local_resources, interval=0.2)
        log.info("choose Local Resources")
        time.sleep(3)
        key_usbr = self.logon.rect_offset(top_left, tuple(self.rect_offsets["key_usbr"]))
        pg.click(key_usbr, interval=0.2)
        log.info("choose USBR for USB Storage")
        time.sleep(2)
        # ok_button = self.logon.rect_offset(top_left, tuple(self.rect_offsets['ok_button']))
        ok_button = self.logon.wait_element(['Test_Data/RDP/rdp_ok_5_3.png'])
        pg.click(ok_button)

    def set_key_mapping(self):
        rdp_icon = self.logon.wait_element(['Test_Data/RDP/rdp_icon_10_5.png',
                                            'Test_Data/RDP/rdp_icon1_10_5.png',
                                            'Test_Data/RDP/rdp_icon2_10_5.png',
                                            'Test_Data/RDP/rdp_icon3_10_5.png'])
        # ==========choose edit RDP connection==========
        pg.rightClick(rdp_icon)
        time.sleep(1)
        pg.press('down', presses=2, interval=0.1)
        time.sleep(0.2)
        pg.press('enter', interval=1)
        # ==========wait edit connection dialog==========
        print('wait RDP Connection Manager window...')
        log.info('wait RDP Connection Manager window...')
        time.sleep(5)

        top_left = self.logon.wait_element(['Test_Data/RDP/rdp_title_0_0.png',
                                            'Test_Data/RDP/rdp_title1_0_0.png'])
        local_resources = self.logon.rect_offset(top_left, tuple(self.rect_offsets['local_resources']))
        pg.click(local_resources, interval=0.2)
        log.info("choose Local Resources")
        time.sleep(3)
        key_mapping = self.logon.rect_offset(top_left, tuple(self.rect_offsets["key_mapping"]))
        log.info("choose mapping(High-Level) for USB Storage")
        pg.click(key_mapping)
        time.sleep(2)
        # ok_button = self.logon.rect_offset(top_left, tuple(self.rect_offsets['ok_button']))
        ok_button = self.logon.wait_element(['Test_Data/RDP/rdp_ok_5_3.png'])
        pg.click(ok_button)

    def normal_logon(self, server, test_name):
        self.edit_normal_connection(server)
        self.start_connection()
        time.sleep(8)
        # ==========upload test_name.txt to FTP==========
        self.upload_test_item_exe_location(test_name)
        log.info("upload test_item.txt to FTP")
        self.click_accept_button()


class SmartcardTest(NormalLogonTest):

    def smartcard_logon(self, server, test_name):
        # self.check_smartcard_exist()
        # self.install_smartcard_driver()
        self.edit_smartcard_connection(server)
        self.start_connection()
        time.sleep(8)
        # ==========upload test_name.txt to FTP==========
        location = self.rdp_smartcard_logon
        self.upload_test_item_exe_location(location)
        log.info("upload test_item.txt to FTP")
        # if accept button doesn't pop out, will kill xfreerdp process
        if self.click_accept_button() is False:
            self.kill_process("RDP\\ Client\\ Error")
        else:
            # ==========choose smartcard, input PIN==========
            pg.press("ctrl")
            pin = self.logon.wait_element(['Test_Data/RDP/smart_card_pin_5_5.png',
                                           'Test_Data/RDP/smart_card_pin1_5_5.png',
                                           'Test_Data/RDP/smart_card_pin2_5_5.png'])
            pg.press("ctrl")
            if pin:
                pg.click(pin)
                pg.typewrite('0000', interval=0.2)
                pg.press('enter')
                time.sleep(8)
                log.info("found PIN icon, input PIN...")
                return True
            else:
                # press ctrl to wake up. sometimes the screen in locked status after logon.
                pg.press("ctrl")

                connect_smartcard = self.logon.wait_element(['Test_Data/RDP/connect_smartcard_0_0.png',
                                                             'Test_Data/RDP/connect_smartcard1_0_0.png'])
                if connect_smartcard:
                    log.error("no smartcard, please confirm you have insert smartcard")
                    self.kill_process("freerdp")
                    fail_report("test failed, no smartcard, please confirm you have insert smartcard", test_name)
                    return False
                sign_in_option = self.logon.wait_element(['Test_Data/RDP/sign_in_option_10_0.png',
                                                          'Test_Data/RDP/sign_in_option2_10_0.png'])
                if sign_in_option:
                    pg.click(sign_in_option)
                    log.info("click sign_in_option icon")
                    time.sleep(1)
                    smartcard_icon = self.logon.wait_element(['Test_Data/RDP/smart_card_icon_0_0.png',
                                                              'Test_Data/RDP/smart_card_icon1_0_0.png'])
                    if smartcard_icon:
                        pg.click(smartcard_icon)
                        time.sleep(2)
                        pin2 = self.logon.wait_element(['Test_Data/RDP/smart_card_pin_5_5.png',
                                                        'Test_Data/RDP/smart_card_pin1_5_5.png',
                                                        'Test_Data/RDP/smart_card_pin2_5_5.png'])
                        pg.press("ctrl")
                        if pin2:
                            pg.click(pin2)
                            pg.typewrite('0000', interval=0.2)
                            pg.press('enter')
                            log.info("import PIN, logging into remote desktop...")
                            return True
                        else:
                            log.error("can't find pin")
                            fail_report("test failed, can't find pin window, please confirm", test_name)
                            self.kill_process("freerdp")
                            return False
                    else:
                        log.error("can't find smartcard icon")
                        fail_report("test failed, can't find smartcard icon window, please confirm", test_name)
                        self.kill_process("freerdp")
                        return False
                else:
                    log.error("can't find smart_card_icon, please confirm you have insert smartcard")
                    fail_report("test failed. can't find smart_card_icon, please confirm you have insert smartcard")
                    if self.stop_connection_taskbar():
                        log.error("test failed, stop connection.")
                    else:
                        self.kill_process("freerdp")
                        log.error("test failed, kill freerdp process")
                    time.sleep(5)
                    return False

# x = NormalLogonTest()
# x.stop_connection_taskbar()
