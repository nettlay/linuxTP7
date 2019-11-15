from Lib.thinpro_citrix import NewController
from Lib import my_ftp
from Test_Script import script_general
from Test_Script.rdp_smart_card_logon import *
from Test_Script.script_difference import load_yaml

my_logger = logger()
myftp = my_ftp.MyFtp()


def edit_connection_storefront_smartcard():
    url = load_yaml('storefront_server')
    my_logger.info('edit connection')
    icon_list = ['citrix_icon.png']
    citrix_icon = NewController('desktop_root.png', icon_list, 'ICON')
    citrix_icon.rightclick_position()
    time.sleep(1)
    pyautogui.press(['down', 'down'])
    pyautogui.press('enter')
    rdp_connnection_table_controller = NewController('desktop_connection.png',
                                                     ['edit_title.png', 'edit_title_italic.png'], 'WINDOW',
                                                     'citrix_config.yml')
    my_logger.info('click current mode button')
    flag = rdp_connnection_table_controller.click_position('connection_table_current_mode')
    if flag:
        pyautogui.press(['down', 'enter'])
        my_logger.info('click URL button')
        rdp_connnection_table_controller.click_position('connection_table_url')
        pyautogui.typewrite(url)
        my_logger.info('click predefined smartcard')
        rdp_connnection_table_controller.click_position('smart_card')
        pyautogui.press(['tab', 'down'])
        # my_logger.info('click predefined user, password...button')
        # rdp_connnection_table_controller.click_position('connection_table_use_predefined')
        # my_logger.info('click user button')
        # rdp_connnection_table_controller.click_position('connection_table_user')
        # pyautogui.typewrite('automation')
        # my_logger.info('click password button')
        # rdp_connnection_table_controller.click_position('connection_table_password')
        # pyautogui.typewrite('Shanghai2014')
        # my_logger.info('click domain button')
        # rdp_connnection_table_controller.click_position('connection_table_domain')
        # pyautogui.typewrite('sh.dto')
        button_list = ['ok.png']
        my_logger.info('click ok button')
        ok_button = NewController('desktop_root.png', button_list, 'ICON')
        ok_button.click_position()
        return True
    else:
        #capture_screen()
        reason = 'failed to find edit window'
        my_logger.info(reason)
        # fail_report('failed to open edit window')
        os.popen('pkill -f CitrixApps')
        return reason


def login_storefront_smartcard(desktop_list):
    # pyautogui.hotkey('ctrl', 'alt', 'end')
    script_general.initialize()
    my_logger.info('check certificate')
    script_general.import_cer()
    script_general.remove_citrix()
    script_general.create_citrix()
    flag = edit_connection_storefront_smartcard()
    if flag is not True:
        print("flag1 fail")
        return flag
    my_logger.info('start connection')
    flag = script_general.start_connection()
    if flag is not True:
        print("flag2 fail")
        return flag
    script = r"//15.83.240.98/Automation/Linux/scripts/logoff.exe"
    myftp.upload_new_file('./Test_Data/', 'Automation/Linux/flags', 'test_item.txt', script)
    time.sleep(30)
    if verify_smartcard_local(desktop_list) is False:
        print("flag3 fail")
        return False
    else:
        return True


def verify_smartcard_local(desktop_list):
    # print("verify smartcard local")
    # --------------------check pin appear------------------------------
    pin_list = ["pin.png"]
    pin = NewController("desktop_root.png", pin_list, "ICON")
    pin_flag = pin.click_position()
    if pin_flag:
        my_logger.info("input pin")
        pyautogui.press("0")
        pyautogui.press("0")
        pyautogui.press("0")
        pyautogui.press("0")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(5)
        my_logger.info('select desktop')
        flag = script_general.select_desktop(desktop_list)
        print(flag)
        # --------------------add verify_smartcard---------------
        #  no need  verify_smartcard()
        if flag is False:
            print("can't find desktop")
            return flag
        else:
            # fail_report('select desktop fail')
            time.sleep(20)
            launch_error = ["xd_smartcard_unable_to_launch.png"]
            launch = NewController("desktop_root.png", launch_error, "ICON")
            launch_flag = launch.click_position()
            if launch_flag:
                log.error("can't launch remote desktop")
                log.info("will kill Citrix process")
                os.popen("pkill -f Citrix")
                fail_report(test_name)
                return False
            else:
                print("login to remote desktop")
                time.sleep(5)
                pg.press("ctrl")
                smartcard_list = ["xd_smartcard_switch_smart_card_3.png"]
                smartcard = NewController("desktop_root.png", smartcard_list, "ICON")
                smartcard_flag = smartcard.click_position()
                if smartcard_flag:
                    util = RDPUtil()
                    sign_in_option = util.wait_element([
                        'Test_Data/1366x768/template_file/xd_smartcard_sign_in_options_10_0.png'])
                    if sign_in_option:
                        verify_smartcard()
                    return True
    else:
        # --------------------check if smartcard and smartcard reader not found-------------------
        list = ["xd_smartcard_not_found_error.png"]
        smart_card_not_found = NewController("desktop_root.png", list, "ICON")
        not_found_flag = smart_card_not_found.click_position()
        if not_found_flag:
            cancel_list = ["xd_smartcard_not_found_cancel.png"]
            cancel_button = NewController("desktop_root.png", cancel_list, "ICON")
            cancel_button.click_position()
            smartcard_button = ["xd_smartcard_not_found_error2.png"]
            citrix_error = NewController("desktop_root.png", smartcard_button, "ICON")
            error_flag = citrix_error.click_position()
            if error_flag:
                ok_list = ["xd_smartcard_not_found_ok.png"]
                ok_button = NewController("desktop_root.png", ok_list, "ICON")
                ok_button.click_position()
                my_logger.error("can't find smartcard, test fail")
                fail_report("Failed, can't find smartcard")
                return False
        else:
            # --------------------check if smartcard not valid---------------
            not_valid_list = ["xd_smartcard_not_valid.png"]
            smart_card_not_valid = NewController("desktop_root.png", not_valid_list, "ICON")
            not_valid_flag = smart_card_not_valid.click_position()
            if not_valid_flag:
                cancel_list = ["xd_smartcard_not_found_cancel.png"]
                cancel_button = NewController("desktop_root.png", cancel_list, "ICON")
                cancel_button.click_position()
                smartcard_button = ["xd_smartcard_not_found_error2.png"]
                citrix_error = NewController("desktop_root.png", smartcard_button, "ICON")
                error_flag = citrix_error.click_position()
                if error_flag:
                    ok_list = ["xd_smartcard_not_found_ok.png"]
                    ok_button = NewController("desktop_root.png", ok_list, "ICON")
                    ok_button.click_position()
                    my_logger.error("smartcard not valid, test fail")
                    fail_report("Failed, smartcard not valid")
                    return False
    process = os.popen('ps -ef | grep Citrix\\ Error | grep -v grep').read()
    if process:
        log.error("get error window")
        log.info("will kill Citrix process")
        os.popen("pkill -f Citrix")
        return False

def verify_smartcard():
    util = RDPUtil()
    logon = NormalLogonTest()
    # ==========choose smartcard, input PIN==========
    pin = util.wait_element(['Test_Data/RDP/smart_card_pin_5_5.png',
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

        connect_smartcard = util.wait_element(['Test_Data/RDP/connect_smartcard_0_0.png',
                                               'Test_Data/RDP/connect_smartcard1_0_0.png'])
        if connect_smartcard:
            log.error("no smartcard, please confirm you have insert smartcard")

            os.popen('pkill -f Citrix')
            log.info("kill process")
            fail_report("test failed, no smartcard, please confirm you have insert smartcard")
            return False
        sign_in_option = util.wait_element(['Test_Data/RDP/sign_in_option_10_0.png',
                                            'Test_Data/RDP/sign_in_option2_10_0.png'])
        if sign_in_option:
            pg.click(sign_in_option)
            log.info("click sign_in_option icon")
            time.sleep(1)
            smartcard_icon = util.wait_element(['Test_Data/RDP/smart_card_icon_0_0.png',
                                                'Test_Data/RDP/smart_card_icon1_0_0.png'])
            if smartcard_icon:
                pg.click(smartcard_icon)
                time.sleep(2)
                pin2 = util.wait_element(['Test_Data/RDP/smart_card_pin_5_5.png',
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
                    fail_report("test failed, can't find pin window, please confirm")
                    os.popen('pkill -f Citrix')
                    log.info("kill process")
                    return False
            else:
                log.error("can't find smartcard icon")
                fail_report("test failed, can't find smartcard icon window, please confirm")
                os.popen('pkill -f Citrix')
                log.info("kill process")
                return False
        else:
            log.error("can't find smart_card_icon, please confirm you have insert smartcard")
            fail_report("test failed. can't find smart_card_icon, please confirm you have insert smartcard")
            os.popen('pkill -f Citrix')
            log.error("test failed, kill process")
            time.sleep(5)
        return False

