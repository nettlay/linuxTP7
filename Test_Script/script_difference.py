import time
from Lib.thinpro_citrix import NewController
import pyautogui
from Test_Script.common_function import logger
from Lib import my_ftp
import subprocess
import os
from Test_Script import script_general
import yaml
import Test_Script.rdp_logon as rdp_logon


my_logger = logger()
myftp = my_ftp.MyFtp()


def load_yaml(key_name):
    try:
        with open('./Test_Data/1920x1200/config_file/citrix_config.yml')as f:
            dict1 = yaml.safe_load(f)
            return dict1[key_name]
    except OSError:
        my_logger.error('load_yaml', exc_info=True)
    except LookupError:
        my_logger.error('load_yaml', exc_info=True)


def edit_connection_pnagent():
    url = load_yaml('pnagent_server')
    user = load_yaml('user')
    password = load_yaml('password')
    domain = load_yaml('domain')
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
        pyautogui.press(['down', 'down', 'enter'])
        my_logger.info('click URL button')
        rdp_connnection_table_controller.click_position('connection_table_url')
        pyautogui.typewrite(url)
        my_logger.info('click predefined user, password...button')
        rdp_connnection_table_controller.click_position('connection_table_use_predefined')
        my_logger.info('click user button')
        rdp_connnection_table_controller.click_position('connection_table_user')
        pyautogui.typewrite(user)
        my_logger.info('click password button')
        rdp_connnection_table_controller.click_position('connection_table_password')
        pyautogui.typewrite(password)
        my_logger.info('click domain button')
        rdp_connnection_table_controller.click_position('connection_table_domain')
        pyautogui.typewrite(domain)
        pyautogui.hotkey('ctrl', 'alt', 'f5')
        time.sleep(2)
        button_list = ['ok.png']
        my_logger.info('click ok button')
        ok_button = NewController('desktop_root.png', button_list, 'ICON')
        ok_button.click_position()
        return True
    else:
        reason = 'failed to find edit window'
        my_logger.info(reason)
        os.popen('pkill -f CitrixApps')
        return reason


def edit_connection_storefront():
    url = load_yaml('storefront_server')
    user = load_yaml('user')
    password = load_yaml('password')
    domain = load_yaml('domain')
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
        my_logger.info('click predefined user, password...button')
        rdp_connnection_table_controller.click_position('connection_table_use_predefined')
        my_logger.info('click user button')
        rdp_connnection_table_controller.click_position('connection_table_user')
        pyautogui.typewrite(user)
        my_logger.info('click password button')
        rdp_connnection_table_controller.click_position('connection_table_password')
        pyautogui.typewrite(password)
        my_logger.info('click domain button')
        rdp_connnection_table_controller.click_position('connection_table_domain')
        pyautogui.typewrite(domain)
        pyautogui.hotkey('ctrl', 'alt', 'f5')
        time.sleep(2)
        button_list = ['ok.png']
        my_logger.info('click ok button')
        ok_button = NewController('desktop_root.png', button_list, 'ICON')
        ok_button.click_position()
        return True
    else:
        reason = 'failed to find edit window'
        my_logger.info(reason)
        os.popen('pkill -f CitrixApps')
        return reason


def edit_connection_storefront_smart_card():
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
        my_logger.info('click predefined smart card')
        rdp_connnection_table_controller.click_position('smart_card')
        pyautogui.press(['tab', 'down'])
        button_list = ['ok.png']
        my_logger.info('click ok button')
        ok_button = NewController('desktop_root.png', button_list, 'ICON')
        ok_button.click_position()
        return True
    else:
        reason = 'failed to find edit window'
        my_logger.info(reason)
        os.popen('pkill -f CitrixApps')
        return reason


def edit_connection_rdp():
    my_logger.info('edit connection')
    icon_list = ['rdp_icon.png']
    rdp_icon = NewController('desktop_root.png', icon_list, 'ICON')
    rdp_icon.rightclick_position()
    time.sleep(1)
    pyautogui.press(['down', 'down'])
    pyautogui.press('enter')
    rdp_connnection_table_controller = NewController('desktop_connection.png',
                                                     ['rdp_title.png', 'rdp_title_italic.png'], 'WINDOW',
                                                     'config.yml')
    my_logger.info('click url')
    flag = rdp_connnection_table_controller.click_position('rdp_local_resource')
    if flag:
        pyautogui.typewrite('rfxw10-auto')
        my_logger.info('click predefined user, password...button')
        rdp_connnection_table_controller.click_position('rdp_table_use_predefined')
        my_logger.info('click user button')
        rdp_connnection_table_controller.click_position('rdp_table_user')
        pyautogui.typewrite('automation')
        my_logger.info('click password button')
        rdp_connnection_table_controller.click_position('rdp_table_password')
        pyautogui.typewrite('Shanghai2014')
        my_logger.info('click domain button')
        rdp_connnection_table_controller.click_position('rdp_table_domain')
        pyautogui.typewrite('sh.dto')
        button_list = ['ok.png']
        my_logger.info('click ok button')
        ok_button = NewController('desktop_root.png', button_list, 'ICON')
        ok_button.click_position()
        return True
    else:
        reason = 'failed to find edit window'
        my_logger.info(reason)
        os.popen('pkill -f CitrixApps')
        return reason


def set_citrix_usbkey_mapping():
    my_logger.info('set usb key mapping to registry')
    cmd1 = 'mclient --quiet set root/ConnectionType/xen/general/enableUSBRedirection 0'
    cmd2 = 'mclient commit'
    cmd3 = 'mclient --quiet set root/ConnectionType/xen/general/enableDynamicDriveMapping 1'
    disable_usbr = cmd1 + '&&' + cmd2
    enable_dmapping = cmd3 + '&&' + cmd2
    subprocess.run(disable_usbr, shell=True)
    subprocess.run(enable_dmapping, shell=True)


def set_citrix_usbprinter_mapping():
    my_logger.info('set usb printer mapping to registry')
    cmd1 = 'mclient --quiet set root/ConnectionType/xen/general/printerAutoCreation 1'
    cmd2 = 'mclient commit'
    printer_mapping = cmd1 + '&&' + cmd2
    subprocess.run(printer_mapping, shell=True)


def set_rdp_printer_mapping():
    my_logger.info('set usb printer mapping')
    rdp_icon = NewController('desktop_root.png', ['rdp_icon.png'], 'ICON')

    rdp_icon.rightclick_position('')
    pyautogui.press(['down', 'down'])
    pyautogui.press('enter')

    rdp_connnection_table_controller = NewController('desktop_connection.png',
                                                     ['rdp_title.png', 'rdp_title_italic.png'], 'WINDOW',
                                                     'rdp_config.yml')
    flag = rdp_connnection_table_controller.click_position('rdp_local_resource')
    if flag:
        rdp_connnection_table_controller.click_position('rdp_high_level')
        button_list = ['ok.png']
        my_logger.info('click ok button')
        ok_button = NewController('desktop_root.png', button_list, 'ICON')
        ok_button.click_position()
        return True
    else:
        reason = 'failed to open edit window'
        my_logger.info(reason)
        os.popen('pkill -f CitrixApps')
        return reason


def set_citrix_usbkey_usbr():
    my_logger.info('set usb key usbr to registry')
    cmd1 = 'mclient --quiet set root/ConnectionType/xen/general/enableUSBRedirection 1'
    cmd2 = 'mclient commit'
    cmd3 = 'mclient --quiet set root/ConnectionType/xen/general/enableDynamicDriveMapping 0'
    enable_usbr = cmd1 + '&&' + cmd2
    disable_dmapping = cmd3 + '&&' + cmd2
    subprocess.run(enable_usbr, shell=True)
    subprocess.run(disable_dmapping, shell=True)


def login_pnagent(desktop_list):
    try:
        script_general.initialize()
        my_logger.info('check certificate')
        script_general.import_cer()
        script_general.remove_citrix()
        script_general.create_citrix()
        flag = edit_connection_pnagent()
        if flag is not True:
            return flag
        my_logger.info('start connection')
        flag = script_general.start_connection()
        if flag is not True:
            return flag
        time.sleep(5)
        my_logger.info('select desktop')
        flag = script_general.select_desktop(desktop_list)
        if flag is not True:
            return flag
        my_logger.info('download username.txt')
        myftp.download_file('Automation/Linux/flags', './Test_Report/', 'username.txt')

        if os.path.exists('./Test_Report/username.txt'):
            with open('./Test_Report/username.txt')as f1:
                username = f1.read()
        else:
            reason = 'cannot find username.txt'
            my_logger.info(reason)
            os.popen('pkill -f Citrix')
            return reason
        if username != 'automation':
            reason = 'username is not automation'
            my_logger.info(reason)
            os.popen('pkill -f Citrix')
            return reason
        else:
            my_logger.info('username is automation')
            return True
    except OSError:
        my_logger.error('Program Exception', exc_info=True)


def login_storefront(desktop_list):
    try:
        script_general.initialize()
        my_logger.info('check certificate')
        script_general.import_cer()
        script_general.remove_citrix()
        script_general.create_citrix()
        flag = edit_connection_storefront()
        if flag is not True:
            return flag
        my_logger.info('start connection')
        flag = script_general.start_connection()
        if flag is not True:
            return flag
        time.sleep(5)
        my_logger.info('select desktop')
        flag = script_general.select_desktop(desktop_list)
        if flag is not True:
            return flag
        my_logger.info('download username.txt')
        myftp.download_file('Automation/Linux/flags', './Test_Report/', 'username.txt')

        if os.path.exists('./Test_Report/username.txt'):
            with open('./Test_Report/username.txt')as f1:
                username = f1.read()
        else:
            reason = 'cannot find username.txt'
            my_logger.info(reason)
            os.popen('pkill -f Citrix')
            return reason
        if username != 'automation':
            reason = 'username is not automation'
            my_logger.info(reason)
            os.popen('pkill -f Citrix')
            return reason
        else:
            my_logger.info('username is automation')
            return True
    except OSError:
        my_logger.error('Program Exception', exc_info=True)


def login_storefront_smart_card(desktop_list):
    try:
        # pyautogui.hotkey('ctrl', 'alt', 'end')
        script_general.initialize()
        my_logger.info('check certificate')
        script_general.import_cer()
        script_general.remove_citrix()
        script_general.create_citrix()
        flag = edit_connection_storefront_smart_card()
        if flag is not True:
            return flag
        my_logger.info('start connection')
        flag = script_general.start_connection()
        if flag is not True:
            return flag
        time.sleep(5)
        my_logger.info('select desktop')
        flag = script_general.select_desktop(desktop_list)
        if flag is not True:
            return flag
            # fail_report('select desktop fail')
        my_logger.info('download username.txt')
        myftp.download_file('Automation/Linux/flags', './Test_Report/', 'username.txt')
        if os.path.exists('./Test_Report/username.txt'):
            with open('./Test_Report/username.txt')as f1:
                username = f1.read()
        else:
            reason = 'cannot find username.txt'
            my_logger.info(reason)
            # fail_report('cannot find username.txt')
            os.popen('pkill -f Citrix')
            return reason
        if username != 'automation':
            reason = 'username is not automation'
            my_logger.info(reason)
            # fail_report('username is not automation')
            os.popen('pkill -f Citrix')
            return reason
        else:
            my_logger.info('username is automation')
            return True
    except OSError:
        my_logger.error('Program Exception', exc_info=True)


def login_rdp():

    logon = rdp_logon.LogonTest()
    try:
        flag = logon.login_rfx('RDP_Logon_Win10')
        if flag is not True:
            return flag
        myftp.download_file('Automation/Linux/flags', './Test_Report/', 'username.txt')
        if os.path.exists('./Test_Report/username.txt'):
            with open('./Test_Report/username.txt')as f1:
                username = f1.read()
        else:
            reason = 'cannot find username.txt'
            my_logger.info(reason)
            # fail_report('cannot find username.txt')
            os.popen('pkill -f Citrix')
            return reason
        if username != 'automation':
            reason = 'username is not automation'
            my_logger.info(reason)
            # fail_report('username is not automation')
            os.popen('pkill -f Citrix')
            return reason
        else:
            my_logger.info('username is automation')
            return True
    except Exception as e:
        my_logger.error('Program Exception', exc_info=True)
        return e


def logoff():
    try:
        my_logger.info('send logoff command')
        myftp.upload_new_file('./Test_Report/', 'Automation/Linux/flags', 'test_item.txt',
                              r'//15.83.240.98/Automation/Linux/scripts/logoff.exe')
        flag = script_general.check_succeed_signout()
        if flag is not True:
            # pass_report()
            # my_logger.info('test passed')
            return flag
        else:
            return True
            # fail_report('failed sign out')
    except OSError:
        my_logger.error('Program Exception', exc_info=True)


def xen_usbkey_mapping():
    my_logger.info('send usbkey mapping task')
    myftp.upload_new_file('./Test_Report/', 'Automation/Linux/flags', 'test_item.txt',
                          r'//15.83.240.98/Automation/Linux/scripts/usbkey_mapping.exe')
    my_logger.info('download test_result.txt')
    myftp.download_file('Automation/Linux/flags', './Test_Report/', 'test_result.txt')

    if os.path.exists('./Test_Report/test_result.txt'):
        with open('./Tes'
                  't_Report/test_result.txt')as f2:
            case_result = f2.read()
    else:
        reason = 'cannot find usbkey mapping test_result.txt'
        my_logger.info(reason)
        os.popen('pkill -f CitrixApps')
        return reason
    if case_result == 'Passed':
        my_logger.info('xen_subkey_mapping test Passed')
        return True
    elif 'Failed' in case_result:
        reason = case_result.split(':')[1]
        my_logger.info(reason)
        return reason
    else:
        reason = 'test unknown error'
        my_logger.info(reason)
        return reason


def xen_usbkey_redirection():
    my_logger.info('send usbkey redirection task')
    myftp.upload_new_file('./Test_Report/', 'Automation/Linux/flags', 'test_item.txt',
                          r'//15.83.240.98/Automation/Linux/scripts/usbkey_redirection.exe')
    my_logger.info('download test_result.txt')
    myftp.download_file('Automation/Linux/flags', './Test_Report/', 'test_result.txt')
    if os.path.exists('./Test_Report/test_result.txt'):
        with open('./Test_Report/test_result.txt')as f2:
            case_result = f2.read()
    else:
        reason = 'cannot find usbkey_redirection test_result.txt'
        my_logger.info(reason)
        # fail_report('cannot find usbkey_redirection test_result.txt')
        os.popen('pkill -f CitrixApps')
        return reason
    if case_result == 'Passed':
        my_logger.info('xen_subkey_redirection test Passed')
        return True
    elif 'Failed' in case_result:
        reason = case_result.split(':')[1]
        my_logger.info(reason)
        return reason
    else:
        reason = 'test unknown error'
        my_logger.info(reason)
        return reason


def usbprinter_mapping():
    my_logger.info('send usb printer mapping task')
    myftp.upload_new_file('./Test_Report/', 'Automation/Linux/flags', 'test_item.txt',
                          r'//15.83.240.98/Automation/Linux/scripts/usbprinter_mapping.exe')
    my_logger.info('download test_result.txt')
    myftp.download_file('Automation/Linux/flags', './Test_Report/', 'test_result.txt')

    if os.path.exists('./Test_Report/test_result.txt'):
        with open('./Test_Report/test_result.txt')as f2:
            case_result = f2.read()
    else:
        reason = 'canno' \
                 't find usbprinter mapping test_result.txt'
        my_logger.info(reason)
        # fail_report('cannot find usbprinter mapping test_result.txt')
        os.popen('pkill -f CitrixApps')
        return reason
    if case_result == 'Passed':
        my_logger.info('xen_subprinter_mapping test Passed')
        # my_logger.info('test passed')
        # pass_report()
        return True
    elif 'Failed' in case_result:
        reason = case_result.split(':')[1]
        my_logger.info(reason)
        return reason
    else:
        reason = 'test unknown error'
        my_logger.info(reason)
        return reason


def confirm_usbkeymapping_file(file_name='transfer_check.txt'):
    my_logger.info('check local usb file again')
    usbkey = script_general.check_localusb_exist()
    if usbkey:
        usb_file = '/media/%s/%s' % (usbkey, file_name)
    else:
        reason = 'cannot find local usb key'
        #fail_report('cannot find usb key at local')
        return reason
    if os.path.exists(usb_file):
        with open(usb_file)as f:
            content = f.read()
    else:
        reason = 'cannot find /media/%s/%s' % (usbkey, usb_file)
        my_logger.info(reason)
        # fail_report('cannot find /media/%s/%s' % (usbkey, usb_file))
        return reason
    if content != 'usbkey mapping test':
        reason = 'local usb file content is not the same with vdi'
        my_logger.info(reason)
        # fail_report('local usb file content is not the same with vdi')
        return reason
    else:
        my_logger.info('local usb file content is the same with vdi')
        # my_logger.info('test passed')
        # pass_report()
        return True


def confirm_usbkeyredirection_file(file_name='transfer_check.txt'):
    my_logger.info('check local usb file again')
    usbkey = script_general.check_localusb_exist()
    if usbkey:
        usb_file = '/media/%s/%s' % (usbkey, file_name)
    else:
        reason = 'cannot find usb key at local'
        # fail_report(reason)
        return reason
    if os.path.exists(usb_file):
        with open(usb_file)as f:
            content = f.read()
    else:
        reason = 'cannot find /media/%s/%s' % (usbkey, usb_file)
        my_logger.info(reason)
        # fail_report('cannot find /media/%s/%s' % (usbkey, usb_file))
        return reason
    if content != 'usbkey redirection test':
        reason = 'local usb file content is not the same with vdi'
        my_logger.info(reason)
        # fail_report('local usb file content is not the same with vdi')
        return reason
    else:
        my_logger.info('local usb file content is the same with vdi')
        # my_logger.info('test passed')
        # pass_report()
        return True