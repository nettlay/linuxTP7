from Test_Script import wireless
import time
import pyautogui as pag
from Test_Script import common_function as report
import os


def run():
    file_name = 'Connectivity_WPA2P'
    log = report.logger()
    wire = wireless.Wireless('R1_TC_2.4G_n_WPA2P', 'WPA2P_password')
    check_wireless = wire.check_wireless()
    if check_wireless is not True:
        report.fail_report('Fail:%s' % check_wireless, file_name)
        return False
    try:
        with open('test.txt', 'r') as test:
            wire.switch_root()
            if test.readlines()[0] == 'pass':
                os.remove('test.txt')
                return True
            else:
                os.remove('test.txt')
                return False
    except:
        print('continue')
    boot_times = wire.read_boot_time()
    if boot_times is False:
        wire.switch_wired('1', 'down')
        boot_times = '1'
    wire.switch_root()
    if boot_times == '1':
        wire.clear_profiles()
        wire.open_wireless()
        add_wireless = wire.add_wireless()
        if add_wireless is not True:
            report.fail_report('Fail:%s' % add_wireless, file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        connect_wpa2a = wire.connect_with_security()
        if connect_wpa2a is not True:
            report.fail_report('Fail:%s' % connect_wpa2a, file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        if wire.check_profile() is False:
            pag.hotkey('ctrl', 'alt', 'f4')
            report.fail_report('Fail:not found wireless profile', file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        time.sleep(25)
        if wire.ping() is False:
            report.fail_report('Fail:ping to network fail,check if the wifi is or not available, or delay too short',
                               file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        log.info('connect wireless success')
        check_connect = wire.check_auto_connect()
        if check_connect is not True:
            pag.hotkey('ctrl', 'alt', 'tab')
            time.sleep(1)
            pag.hotkey('ctrl', 'alt', 'f4')
            report.fail_report('Fail:%s' % check_connect, file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        if wire.del_profile() is not True:
            report.fail_report('Fail:delete profile fail', file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        time.sleep(10)
        if wire.ping() is False:
            pag.hotkey('ctrl', 'alt', 'f4')
            log.info('delete profile,ping test success')
            report.pass_report(file_name)
            write('pass')
            wire.switch_wired('remove', 'up')
        else:
            pag.hotkey('ctrl', 'alt', 'f4')
            report.fail_report('Fail:delete profile complete,but can ping to network,check time delay os connection',
                               file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False


def write(message='t'):
    with open('test.txt', 'w') as test:
        test.write(message)
