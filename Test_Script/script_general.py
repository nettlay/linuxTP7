from Lib.thinpro_citrix import NewController
import time
import pyautogui
import datetime
from Test_Script import certificate
from Lib import my_ftp
import os
import subprocess
from Test_Script.common_function import logger, pass_report, fail_report


my_logger = logger()
myftp = my_ftp.MyFtp()


def write_citrix_offset_to_yml():
    remove_citrix()
    create_citrix()
    citrix_icon = NewController('desktop_root.png', ['citrix_icon.png'], 'ICON')
    citrix_icon.rightclick_position('')
    pyautogui.press(['down', 'down'])
    pyautogui.press('enter')

    rdp_connnection_table_controller = NewController('desktop_connection.png',
                                                        ['edit_title.png', 'edit_title_italic.png'], 'WINDOW',
                                                        'citrix_config.yml')

    rdp_connnection_table_controller.click_position_tool('connection_table_current_mode.png')
    edit_dict = {'connection_table_current_mode': rdp_connnection_table_controller.relative_offset}
    pyautogui.press(['down', 'enter'])
    rdp_connnection_table_controller.click_position_tool('connection_table_url.png', (0.9, 0.5))
    edit_dict['connection_table_url'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('connection_table_use_predefined.png')
    edit_dict['connection_table_use_predefined'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('connection_table_user.png', (0.9, 0.5))
    edit_dict['connection_table_user'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('connection_table_password.png', (0.9, .5))
    edit_dict['connection_table_password'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('connection_table_domain.png', (0.9, 0.5))
    edit_dict['connection_table_domain'] = rdp_connnection_table_controller.relative_offset
    # rdp_connnection_table_controller.click_position_tool(root, 'ok.png')
    # edit_dict['ok'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.dump_to_yaml(edit_dict)


def write_rdp_offset_to_yml():
    # remove_rdp()
    # create_rdp()
    rdp_icon = NewController('desktop_root.png', ['rdp_icon.png'], 'ICON')
    rdp_icon.rightclick_position('')
    pyautogui.press(['down', 'down'])
    pyautogui.press('enter')

    rdp_connnection_table_controller = NewController('desktop_connection.png',
                                                     ['rdp_title.png', 'rdp_title_italic.png'], 'WINDOW',
                                                     'rdp_config.yml')
    edit_dict = {}
    # rdp_connnection_table_controller.click_position_tool('connection_table_current_mode.png')
    # edit_dict = {'connection_table_current_mode': rdp_connnection_table_controller.relative_offset}
    # pyautogui.press(['down', 'enter'])
    rdp_connnection_table_controller.click_position_tool('rdp_table_url.png', (0.9, 0.5))
    edit_dict['rdp_table_url'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('rdp_table_use_predefined.png')
    edit_dict['rdp_table_use_predefined'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('rdp_table_user.png', (0.9, 0.5))
    edit_dict['rdp_table_user'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('rdp_table_password.png', (0.9, .5))
    edit_dict['rdp_table_password'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('rdp_table_domain.png', (0.9, 0.5))
    edit_dict['rdp_table_domain'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('rdp_local_resource.png')
    edit_dict['rdp_local_resource'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.click_position_tool('rdp_high_level.png')
    edit_dict['rdp_high_level'] = rdp_connnection_table_controller.relative_offset
    # rdp_connnection_table_controller.click_position_tool(root, 'ok.png')
    # edit_dict['ok'] = rdp_connnection_table_controller.relative_offset
    rdp_connnection_table_controller.dump_to_yaml(edit_dict)


def generate_time_str():
    today = datetime.datetime.today()
    time_str = today.strftime('%Y-%m-%d_%H-%M-%S')
    return time_str


def check_localusb_exist():
    my_logger.info('check if local usb key exist')
    for i in range(30):
        usb_info = subprocess.Popen('ls /media', stdout=subprocess.PIPE, shell=True).communicate()
        usb_devname = usb_info[0].decode('utf-8')
        if usb_devname:
            my_logger.info('find local usb key')
            return usb_devname.strip('\n')
        else:
            time.sleep(1)
    reason = 'cannot find local usb key'
    my_logger.info(reason)
    return False


def remove_usb_file(file_name='transfer_check.txt'):
    my_logger.info('remove transfer_check.txt from usb key')
    usbkey = check_localusb_exist()
    if usbkey:
        os.popen('rm -f /media/%s/%s' % (usbkey, file_name))


def remove_citrix():
    my_logger.info('remove connection')
    citrix_icon = NewController('desktop_root.png', ['citrix_icon.png', 'citrix_icon_2.png'], 'ICON')
    t = citrix_icon.rightclick_position('')
    time.sleep(1)
    pyautogui.press(['down', 'down', 'down', 'down', 'down'])
    pyautogui.press('enter')
    if not t:
        reason = 'failed to remove connection'
        my_logger.info(reason)
        # fail_report('failed to remove connection')
    else:
        return True


def remove_rdp():
    my_logger.info('remove connection')
    rdp_icon = NewController('desktop_root.png', ['rdp_icon.png', 'rdp_icon_2.png'], 'ICON')
    t = rdp_icon.rightclick_position('')
    time.sleep(1)
    pyautogui.press(['down', 'down', 'down', 'down', 'down'])
    pyautogui.press('enter')
    if not t:
        reason = 'failed to remove connection'
        my_logger.info(reason)
        #fail_report('failed to remove connection')
    else:
        return True


def create_citrix():
    my_logger.info('create connection')
    time.sleep(1)
    width, height = pyautogui.size()
    pyautogui.moveTo(width, 0, 0.5)
    pyautogui.rightClick()
    time.sleep(1)
    pyautogui.press('down')
    pyautogui.press('enter')
    pyautogui.press('enter')


def create_rdp():
    my_logger.info('create connection')
    time.sleep(1)
    width, height = pyautogui.size()
    pyautogui.moveTo(width, 0, 0.5)
    pyautogui.rightClick()
    time.sleep(1)
    pyautogui.press('down')
    pyautogui.press('enter')
    pyautogui.press('down')
    pyautogui.press('enter')


def start_connection():
    my_logger.info('start connection')
    citrix_icon = NewController('desktop_root.png', ['citrix_icon.png'], 'ICON')
    t = citrix_icon.rightclick_position()
    time.sleep(1)
    pyautogui.press(['down', 'enter'])
    if not t:
        reason = 'failed to start connection'
        my_logger.info(reason)
        return reason
    else:
        return True


def select_desktop(name):
    broker = NewController('desktop_root.png', ['citrix_broker.png', 'citrix_broker_italic.png'], 'ICON')
    flag = broker.click_position()
    if not flag:
        reason = 'failed to look up citrix broker'
        my_logger.info(reason)
        os.popen('pkill -f citrix')
        return reason
    pyautogui.hotkey('ctrl', 'alt', 'f5')
    time.sleep(5)
    pool = NewController('desktop_root.png', name, 'ICON')
    flag = pool.doubleclick_position()
    if flag:
        return True
    else:
        reason = 'failed to look up '+', '.join(name)
        my_logger.info(reason)
        os.popen('pkill -f citrixApps')
        return reason


def import_cer():
    cert = certificate.Cert('ROOTCA')
    if not cert.check_cert():
        cert.import_cert()


def initialize():
    my_logger.info('initialize')
    file_list = ['test_item.txt', 'transfer.txt', 'username.txt', 'test_result.txt']
    for file_name in file_list:
        myftp.delete_file('Automation/Linux/flags', file_name)
        if os.path.exists('./Test_Report/' + file_name):
            os.remove('./Test_Report/' + file_name)


def check_succeed_signout():
    try:
        my_logger.info('check if desktop sign out normolly')
        time.sleep(10)
        for i in range(120):
            session_pid = os.popen('ps -ef | grep [s]fnsvr.sh.dto').read()
            if not session_pid:
                my_logger.info('desktop sign out successfully')
                time.sleep(10)
                os.popen('pkill -f CitrixApps')
                # pass_report()
                return True
            else:
                time.sleep(1)
        session_pid = os.popen('ps -ef | grep [s]fnsvr.sh.dto').read()
        if session_pid:
            reason = 'session failed to sign out, so kill the process'
            my_logger.info(reason)
            os.popen('pkill -f sfnsvr.sh.dto')
            os.popen('pkill -f citrixApps')
            #fail_report('connection failed to sign out')
            return reason
    except OSError:
        my_logger.error('Program Exception', exc_info=True)
