from Test_Script import wired_common
import os
import pyautogui
import time
from Test_Script import common_function


log = common_function.logger()


# Description: Get value for vpn info from registry.
# Parameters:
#            Input: N/A
#            Output: reg_auto_start, reg_gw, reg_group, reg_type, reg_username
# Example: vpn_info_reg = get_value_from_reg()
def get_value_from_reg():
    vpn_reg = wired_common.get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "vpn_reg")
    reg_auto_start_string = "mclient --quiet get " + vpn_reg + "/AutoStart"
    reg_auto_start = os.popen(reg_auto_start_string).readlines()[0].strip()
    reg_gw_string = "mclient --quiet get " + vpn_reg + "/VPNC/Gateway"
    reg_gw = os.popen(reg_gw_string).readlines()[0].strip()
    reg_group_string = "mclient --quiet get " + vpn_reg + "/VPNC/Group"
    reg_group = os.popen(reg_group_string).readlines()[0].strip()
    reg_type_string = "mclient --quiet get " + vpn_reg + "/Type"
    reg_type = os.popen(reg_type_string).readlines()[0].strip()
    reg_username_string = "mclient --quiet get " + vpn_reg + "/VPNC/Username"
    reg_username = os.popen(reg_username_string).readlines()[0].strip()
    return reg_auto_start, reg_gw, reg_group, reg_type, reg_username


def set_vpn_as_cisco(target_type, vpn_cisco_gw, vpn_cisco_gn, vpn_cisco_gp, vpn_cisco_un, vpn_cisco_up):
    # If VPN is set, disable it.
    vpn_enable_flag = os.popen("mclient --quiet get root/Network/VPN/Type").readlines()[0].strip()
    if vpn_enable_flag != "None":
        wired_common.disable_vpn()
    # Set VPN
    if wired_common.get_vpn_gui() is True:
        pyautogui.press('tab', presses=4, interval=0.25)
        vpn_info_reg = get_value_from_reg()
        # If reg_auto_start is 0, check the checkbox for auto start.
        if vpn_info_reg[0] == "0":
            pyautogui.hotkey('space')
            time.sleep(1)
        pyautogui.press('tab')
        time.sleep(1)
        if target_type == "Cisco":
            pyautogui.hotkey('down')
            time.sleep(1)
            pyautogui.hotkey('tab')
            time.sleep(1)
            pyautogui.typewrite(vpn_cisco_gw, interval=0.1)
            time.sleep(1)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.typewrite(vpn_cisco_gn, interval=0.1)
            time.sleep(1)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.typewrite(vpn_cisco_gp, interval=0.1)
            time.sleep(1)
            pyautogui.press('tab', presses=2, interval=0.1)
            time.sleep(1)
            pyautogui.typewrite(vpn_cisco_un, interval=0.1)
            time.sleep(1)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.typewrite(vpn_cisco_up, interval=0.1)
            time.sleep(1)
            pyautogui.press('tab', presses=5, interval=0.1)
            time.sleep(1)
            pyautogui.hotkey('space')
            time.sleep(10)
            # Before closing control panel, judge if it exists first.
            control_panel = wired_common.image_match_new('control_panel', 1)
            if control_panel is not None:
                pyautogui.click(control_panel)
                pyautogui.hotkey('ctrl', 'alt', 'f4')
            return True


def check_cisco_settings(target_type, vpn_auto_start, vpn_cisco_gw, vpn_cisco_gn, vpn_cisco_un):
    tun0 = os.popen("ifconfig tun0 | grep 'inet addr:'").readlines()
    if len(tun0) == 0:
        log.error("FAIL: %s VPN creates fail." % target_type)
        # fail_report
        wired_common.disable_vpn()
        return False
    else:
        log.info("+ PASS: %s VPN has been established." % target_type)
    vpn_info_reg = get_value_from_reg()
    # To be optimized
    if str(vpn_info_reg[0]) == str(vpn_auto_start) and vpn_info_reg[1] == vpn_cisco_gw and vpn_info_reg[2] == vpn_cisco_gn and \
            vpn_info_reg[3] == target_type and vpn_info_reg[4] == vpn_cisco_un:
        log.info("+ PASS: %s VPN settings are correct." % target_type)
    else:
        log.error("+ FAIL: %s VPN settings are incorrect." % target_type)
        wired_common.disable_vpn()
        return False


# reg_vpn_info = get_value_from_reg()
# disable_cisco_vpn(reg_vpn_info[3], reg_vpn_info[0])
def disable_cisco_vpn(reg_type, reg_auto_start):
    # If control panel of Network Manager is open, close it.
    control_panel = wired_common.image_match_new('control_panel', 1)
    if control_panel is not None:
        pyautogui.click(control_panel)
        pyautogui.hotkey('ctrl', 'alt', 'f4')
        log.info("Close Control Panel successfully before disable cisco vpn.")
    if reg_type != "None":
        if wired_common.get_vpn_gui() is True:
            time.sleep(1)
            pyautogui.press('tab', presses=4, interval=0.25)
            time.sleep(1)
            if str(reg_auto_start) == "1":
                pyautogui.hotkey('space')
                time.sleep(1)
            pyautogui.press('tab')
            time.sleep(1)
            vpn_info_reg = get_value_from_reg()
            if vpn_info_reg[3] == "Cisco":
                pyautogui.hotkey('up')
            elif vpn_info_reg[3] == "PPTP":
                pyautogui.press('up', presses=2, interval=0.1)
            time.sleep(1)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.hotkey('space')
            time.sleep(10)
            if wired_common.image_match_new('control_panel', 1) is not None:
                pyautogui.hotkey('ctrl', 'alt', 'f4')
                log.info("Disable cisco vpn successfully.")
        else:
            log.info("Failed to locate at VPN page of Control Panel.")

