from Test_Script import wireless
import time
import pyautogui as pag
from Test_Script import common_function as report
import os


def run():
    file_name = 'Connectivity_static_wireless'
    log = report.logger()
    wire = wireless.Wireless('R1_TC_5G_n', 'static_wireless_password')
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
        boot_times = 1
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
        apply_settings = wire.apply_settings()
        if apply_settings is not True:
            report.fail_report('Fail:%s' % apply_settings, file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        if wire.check_profile() is False:
            report.fail_report('Fail:add profile fail', file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        time.sleep(25)
        if wire.static_method() is not True:
            report.fail_report('Fail:not find IPv4 option', file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        time.sleep(25)
        if wire.ping() is False:
            report.fail_report('Fail:ping to static wireless fail after change method to static', file_name)
            write()
            wire.switch_wired('remove', 'up')
            pag.hotkey('ctrl', 'alt', 'f4')
            return False
        wire.write_boot_time('2')
        wire.reboot()
    if boot_times == '2':
        time.sleep(5)
        if wire.ping() is False:
            report.fail_report('Fail:ping to static wireless fail after reboot', file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False
        wire.open_wireless()
        delete_profile = wire.delete_profiles()
        if delete_profile is not True:
            report.fail_report('Fail:%s' % delete_profile, file_name)
            pag.hotkey('ctrl', 'alt', 'f4')
            write()
            wire.switch_wired('remove', 'up')
            return False
        time.sleep(10)
        if wire.ping() is False:
            log.info('delete profile,ping test success')
            report.pass_report(file_name)
            write('pass')
            wire.switch_wired('remove', 'up')
        else:
            report.fail_report('Fail:delete profile complete,but can ping to network,check time delay os connection',
                               file_name)
            write()
            wire.switch_wired('remove', 'up')
            return False


def write(message='t'):
    with open('test.txt', 'w') as test:
        test.write(message)
