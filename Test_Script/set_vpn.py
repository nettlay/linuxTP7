import time
import pyautogui
import Test_Script.addprinter as add
import Test_Script.common_function as co
from Lib.thinpro_citrix import NewController
import Test_Script.Check_window as cw

log = co.logger()


def write_offset_to_startup_yml():
    add.open_window('network', "./Test_Data/1920x1200/template_file/control_panel.png")
    time.sleep(2)
    switch_to_vpn = NewController('desktop.png', ['system.png'], 'WINDOW', 'control_panel.yml')
    switch_to_vpn.click_position_tool('vpn.png')
    edit_dict = {'switch_to_vpn': switch_to_vpn.relative_offset}
    switch_to_vpn.dump_to_yaml(edit_dict)
    enable_vpn = NewController('desktop.png', ['system.png'], 'WINDOW', 'control_panel.yml')
    enable_vpn.click_position_tool('auto_start.png')
    edit_dict['enable_auto_start'] = enable_vpn.relative_offset
    enable_vpn.dump_to_yaml(edit_dict)
    enable_vpn.click_position_tool('vpn_type.png')
    pyautogui.press('down')
    pyautogui.press('enter')
    pyautogui.press('tab')
    time.sleep(2)
    apply_vnc_change = NewController('desktop.png', ['control_panel.png'], 'WINDOW', 'control_panel.yml')
    apply_vnc_change.click_position_tool('control_panel_apply.png')
    edit_dict['apply_vpn_change'] = apply_vnc_change.relative_offset
    apply_vnc_change.dump_to_yaml(edit_dict)
    add.close_window("./Test_Data/1920x1200/template_file/control_panel.png")


def enable_vpn():
    switch_to_vpn = NewController('desktop.png', ['system.png'], 'WINDOW', 'config.yml')
    flag = switch_to_vpn.click_position('vpn.png')
    if flag:
        enable_vpn = NewController('desktop.png', ['system.png'], 'WINDOW', 'config.yml')
        flag = enable_vpn.click_position('auto_start.png')
    else:
        return False
    if flag:
        pyautogui.press('down')
        pyautogui.press('enter')
        pyautogui.press('tab')
        time.sleep(2)
        pyautogui.typewrite("15.83.244.9")
        pyautogui.press('tab')
        pyautogui.typewrite("vpnclient")
        pyautogui.press('tab')
        pyautogui.typewrite("neoware")
        pyautogui.press('tab')
        pyautogui.typewrite("neoware")
        pyautogui.press('tab')