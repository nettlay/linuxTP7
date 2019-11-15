import pyautogui
import time
import cv2
import os
import yaml
from Test_Script import common_function


log = common_function.logger()


# Description: Get the configuration.
# Parameters:
#            Input: path -- The folder path where the configuration file exits.
#                   file_name -- The name of the configuration file.
#                   element -- the item you want to read.
#            Output: The value for the given item.
# Example: vpn_reg = get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "vpn_reg")
def get_config(path, file_name, element):  # To be optimized
    path = path + file_name
    configuration = yaml.safe_load(open(path))
    return configuration[element]


# Description: Get the coordinate of the wired icon
# Parameters:
#            Input: image_path -- The path where the picture to be compared is stored.
#                   image_name -- The name of the picture to be compared.
#                   times -- Compared times.
#            Output: The coordinate of the wired icon.
# Example: image_match('./Test_Data/WiredNetwork/', 'wired_icon.png', 1)
def image_match(image_path, image_name, times):
    image_path = image_path + image_name
    img = cv2.imread(image_path)
    for i in range(times):
        pyautogui.screenshot('screen_shot.png')
        img2 = cv2.imread('screen_shot.png')
        comp_result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(comp_result)
        time.sleep(1)
        if max_val > 0.95:
            return max_loc
        elif i == times - 1:
            # print('max_val: ', max_val)
            return None


# Example: image_match_new('control_panel', 1)
def image_match_new(image_name, times):
    width, height = pyautogui.size()
    image_path = ''
    if width == 1920:
        wired_pictures = get_config('./Test_Data/WiredNetwork/', "wired_configuration.yml", 'wired_pictures')['1920x1200']
    elif width == 1366:
        wired_pictures = get_config('./Test_Data/WiredNetwork/', "wired_configuration.yml", 'wired_pictures')['1366x768']
    else:
        log.info('The display resolution is neither 1920 x * nor 1366 x *.')
        return None
    pictures = wired_pictures[image_name]
    for picture in pictures:
        if width == 1920:
            image_path = './Test_Data/WiredNetwork/1920x1200/' + picture + '.png'
        if width == 1366:
            image_path = './Test_Data/WiredNetwork/1366x768/' + picture + '.png'
        img = cv2.imread(image_path)
        for i in range(times):
            pyautogui.screenshot('screen_shot.png')
            img2 = cv2.imread('screen_shot.png')
            test = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(test)
            time.sleep(1)
            if max_val > 0.95:
                return max_loc
    return None


# Description: Get the times for pressing "Right" arrow according to whether the wireless exists or not.
# Parameters: Input: N/A
#             Output: times for pressing "Right" arrow
# Example: right_times = check_wlan_for_vpn_location()
def check_wlan_for_vpn_location():
    str_wlan = os.popen("ifconfig wlan0 &>/dev/null").readlines()[0].strip()
    if len(str_wlan) != 0:
        right_times = 4
    else:
        right_times = 3
    return right_times


# Description: Locate at the VPN tab in Network control panel.
# Parameters: N/A
# Example: get_vpn_gui()
def get_vpn_gui():
    # close control panel if it exists
    control_panel_toolbar = image_match_new('control_panel_toolbar', 1)
    if control_panel_toolbar is not None:
        pyautogui.click(control_panel_toolbar)
        pyautogui.hotkey('ctrl', 'alt', 'f4')
        max_loc_discard = image_match_new('discard_control_panel', 1)
        if max_loc_discard is not None:
            pyautogui.click(max_loc_discard)
    max_loc_start_menu = image_match_new('start_menu', 1)
    if max_loc_start_menu is not None:
        pyautogui.click(max_loc_start_menu)
        time.sleep(1)
        pyautogui.typewrite('Network', interval=0.25)
        time.sleep(1)
        pyautogui.hotkey('enter')
        time.sleep(1)
        # check window "controlGUI", if exists, do the following steps
        if image_match_new('control_panel', 1) is not None:
            # Locate at VPN tab.
            vpn_tab_in_control_panel = image_match_new('vpn_tab_in_control_panel', 1)
            if vpn_tab_in_control_panel is not None:
                pyautogui.click(vpn_tab_in_control_panel)
                if image_match_new('vpn_control_panel', 1) is not None:
                    log.info("Successfully locate at the VPN page of Control Panel.")
                    return True
            else:
                log.error("Failed to find VPN tab. Testing will stop.")
                # close control panel if it exists
                control_panel_toolbar = image_match_new('control_panel_toolbar', 1)
                if control_panel_toolbar is not None:
                    pyautogui.click(control_panel_toolbar)
                    pyautogui.hotkey('ctrl', 'alt', 'f4')
                return False
            # pyautogui.press('tab', presses=3, interval=0.25)
            # right_times = check_wlan_for_vpn_location()
            # pyautogui.press('right', presses=right_times, interval=0.25)
        else:
            log.error("Failed to launch Network Control Panel.")
            return None
    else:
        log.error("Failed to find Start menu.")
        return None


def disable_vpn():
    vpn_enable_flag = os.popen("mclient --quiet get root/Network/VPN/Type").readlines()[0].strip()
    if vpn_enable_flag != "None":
        log.info("VPN connection is established, we need to disable it before Ethernet test.")
        get_vpn_gui()
        # Locate at Connection Type field in VPN tab.
        pyautogui.press('tab', presses=5, interval=0.25)
        if vpn_enable_flag == 'Cisco':
            pyautogui.hotkey('up')
        elif vpn_enable_flag == 'PPTP':
            pyautogui.press('up', presses=2, interval=0.25)
        pyautogui.hotkey('tab')
        time.sleep(1)
        pyautogui.hotkey('space')
        time.sleep(40)
        control_panel = image_match_new('control_panel', 1)
        if control_panel is not None:
            pyautogui.click(control_panel)
            pyautogui.hotkey('ctrl', 'alt', 'f4')
        vpn_enable_flag = os.popen("mclient --quiet get root/Network/VPN/Type").readlines()[0].strip()
        if vpn_enable_flag == "None":
            log.info("PASS: VPN connection has been disabled.")
        else:
            log.error("FAIL: VPN connection has not been disabled.")
            # common_function.fail_report("FAIL: VPN connection has not been disabled.")
            return False


# Description: Get the network method from registry according to different network type.
# Parameters: network_type -- 'VPN' or 'Wired' or 'Wireless'
# Example: get_network_method('Wired')
def get_network_method(network_type):
    if network_type not in ['VPN', 'Wired', 'Wireless']:
        log.info("No such network type. Please check and re-enter.")
        return
    if network_type == 'VPN':
        network_method = os.popen("mclient --quiet get root/Network/VPN/Type").readlines()[0].strip()
        return network_method
    elif network_type == 'Wired':
        network_method = os.popen("mclient --quiet get root/Network/Wired/Method").readlines()[0].strip()
        return network_method
    elif network_type == 'Wireless':
        network_method = os.popen("mclient --quiet get root/Network/Wireless/Method").readlines()[0].strip()
        return network_method


# Description: Set the network method according to network status.
# Parameters: network_status -- 'Automatic' or 'Static'
# Example: set_method_as('Static', static_ip, submask, static_gw)
#           set_method_as('Automatic')
def set_method_as(network_status, static_ip='', submask='', static_gw=''):
    pyautogui.hotkey('ctrl', 'alt', 's')
    # # Locate at the Start menu then click.
    # max_loc = image_match('./Test_Data/WiredNetwork/', 'start_menu.png', 1)
    # pyautogui.click(max_loc)
    time.sleep(1)
    pyautogui.typewrite('Network', interval=0.25)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    control_panel = image_match_new('control_panel', 1)
    if control_panel is not None:  # checkWindow "ControlGUI"
        pyautogui.click(control_panel)  # Click Control Panel dialog to activate it.
        pyautogui.press('tab', presses=6, interval=0.25)
        if network_status == "Automatic":  # Precondition: the network is Static. Change it to Automatic.
            pyautogui.hotkey('up')
            time.sleep(1)
            pyautogui.hotkey('tab')
            time.sleep(1)
        elif network_status == 'Static':  # Precondition: the network is Automatic. Change it to Static.
            pyautogui.hotkey('down')
            time.sleep(1)
            pyautogui.hotkey('tab')
            time.sleep(1)
            pyautogui.hotkey('tab')
            time.sleep(1)
            pyautogui.typewrite(static_ip, interval=0.25)
            time.sleep(1)
            pyautogui.hotkey('tab')
            time.sleep(1)
            pyautogui.typewrite(submask, interval=0.25)
            time.sleep(1)
            pyautogui.hotkey('tab')
            time.sleep(1)
            pyautogui.typewrite(static_gw)
            time.sleep(1)
        pyautogui.hotkey('tab')
        time.sleep(1)
        pyautogui.hotkey('tab')
        time.sleep(1)
        pyautogui.hotkey('space')
        time.sleep(10)
        con_panel = image_match_new('control_panel', 1)
        if con_panel is not None:  # checkWindow "ControlGUI"
            pyautogui.click(con_panel)
            pyautogui.hotkey('ctrl', 'alt', 'f4')
    # time.sleep(30)
    time.sleep(10)
    # if status == "Static":
    #     checkErrorWindow "It occurs error when set network method as static"


# # Description: Compare the three input values are equal or not.
# # Parameters: Input -- value1, value2, value3
# #             Output -- True or False
# def equal(value1, value2, value3):
#     if value1 == value2 and value2 == value3:
#         return True
#     else:
#         return False


# Description: Check the network setting result. If checking for Static, it compares the runtime ip, registry ip and
#              transferring ip.
# Parameters: network_status -- "Static" or "Automatic"
#             image_name -- The name of the picture to be compared.
# Example: setting_check_for('Automatic')
#          setting_check_for('Static', static_ip, submask, static_gw)
def setting_check_for(network_status, static_ip='', submask='', static_gw=''):
    my_method = get_network_method('Wired')
    if my_method == network_status:
        log.info("PASS: get IP address %s" % network_status)
    else:
        log.error("FAIL: Get IP address method is not %s" % network_status)
        # common_function.fail_report("Get IP address is not " + network_status)
        # summary
        # rename_log_file
        # sys.exit(1)
        return False
    if network_status == "Static":
        my_address = os.popen("ifconfig eth0 | grep -i 'inet addr' | awk '{print $2}' | cut -d':' -f \
        2").readlines()[0].strip()
        my_submask = os.popen("ifconfig eth0 | grep Mask | awk '{print $4}' | cut -d ':' -f2").readlines()[0].strip()
        my_gw = os.popen("route | grep -i default | awk '{print $2}'").readlines()[0].strip()
        reg_submask = os.popen("mclient --quiet get root/Network/Wired/SubnetMask").readlines()[0].strip()
        reg_address = os.popen("mclient --quiet get root/Network/Wired/IPAddress").readlines()[0].strip()
        reg_gw = os.popen("mclient --quiet get root/Network/Wired/DefaultGateway").readlines()[0].strip()
        if my_address == '':
            log.error("FAIL: Ethernet didn't get any address")
            # common_function.fail_report("Ethernet didn't get any address after set method as static.")
            # summary
            # renamelogfile
            # sys.exit(1)
            return False
        if my_address == static_ip and reg_address == static_ip and my_submask == submask and reg_submask == submask \
                and my_gw == static_gw and reg_gw == static_gw:  # To be optimized
            log.info("PASS: Static settings are correct, IP: " + static_ip + "Submask: " + submask + "Gateway: "
                     + static_gw)
            # result = "PASS: Static settings are correct, IP: " + static_ip + "Submask: " + submask + "Gateway: " + \
            #          static_gw
            # file = open((root + '/Test_Report/static_ip_report/report.txt'), 'w')
            # file.write(result)
            # file.close()
        else:
            log.error("FAIL: Static settings are not match, IP: " + static_ip + "Submask: " + submask + "Gateway: " +
                      static_gw)
            # common_function.fail_report("FAIL: Static IP address is not matching.")
            return False


# Description: Check the ip format, all the four address should be in [0, 255].
# Parameters: my_ip_address -- ip address.
# Example: check_ip_format('15.83.240.98')
def check_ip_format(my_ip_address):
    i = 0
    list_ip = my_ip_address.split('.')
    for addr in list_ip:
        if int(addr) in range(0, 256):
            i = i + 1
    if i == 4:
        return True
    else:
        return False


# Description: Ping the destination.
# Parameters: type -- "VPN" or "Normal"
#             server_address -- The destination address.
# Example: destination_ping_check("Normal", "15.83.240.98")
def destination_ping_check(network_type, server_address):
    if check_ip_format(server_address) is False:
        log.error("FAIL: The ip format is not correct. Please check.")
        return False
    # ping_result = len(os.popen(ping_string).readlines()[1:-4])
    ping_result = len(os.popen("ping -c 3 %s &>/dev/null" % server_address).readlines())
    if ping_result == 0:
        log.error("FAIL: ping %s is failed. Network is unreachable." % server_address)  # To be confirmed.
        # common_function.fail_report("FAIL: ping " + server_address + " is failed. Network is unreachable.")
        if network_type == "VPN":
            disable_vpn()
        # summary
        # rename_logfile
        # sys.exit(1)
        return False
    else:
        log.info("PASS: ping %s is working." % server_address)  # To be confirmed.


# Description: Enable left click menu from registry.
# Parameters: N/A
# Example: enable_left_click_nt()
def enable_left_click_nt():
    # parameter reg_enable_left_click should be defined. To be optimized.
    reg_left_click = os.popen("mclient --quiet get root/Network/disableLeftClickMenu").readlines()[0].strip()
    if reg_left_click == "1":
        os.popen("mclient set root/Network/disableLeftClickMenu 0 && mclient commit")
        time.sleep(3)
        reg_left_click = os.popen("mclient --quiet get root/Network/disableLeftClickMenu").readlines()[0].strip()
        if reg_left_click == "0":
            log.info("Enable left click menu of network from registry successfully.")
        else:
            log.error('Failed to enable left click menu from registry. Current value in reg is %s.' % reg_left_click)
            return None
    elif reg_left_click == "0":
        log.info("Left click has already been enabled. No need to change.")


# Description: Disable left click menu from registry.
# Parameters: N/A
# Example: disable_left_click_nt()
def disable_left_click_nt():
    # parameter reg_enable_left_click should be defined. To be optimized.
    reg_left_click = os.popen("mclient --quiet get root/Network/disableLeftClickMenu").readlines()[0].strip()
    if reg_left_click == "0":
        os.popen("mclient set root/Network/disableLeftClickMenu 1 && mclient commit")
        time.sleep(3)
        reg_left_click = os.popen("mclient --quiet get root/Network/disableLeftClickMenu").readlines()[0].strip()
        if reg_left_click == "1":
            log.info("Disable left click menu of network from registry successfully.")
        else:
            log.error('Failed to disable left click menu from registry. Current value in reg is %s.' % reg_left_click)
            return None
    elif reg_left_click == "1":
        log.info("Left click has already been disabled. No need to change.")


# Description: Stop network from the wired tray icon at desktop.
# Parameters: N/A
# Example: stop_network()
def stop_network():
    network_status = os.popen("mclient --quiet get tmp/network/status").readlines()[0].strip()
    if network_status == "1":
        max_loc = image_match_new('wired_icon', 1)
        if max_loc is not None:
            log.info("The location of wired_icon is found.")
            pyautogui.click(max_loc)
            time.sleep(1)
            # Judge the left click menu is enabled, then select Stop Network. TBD.
            pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(1)
            log.info("+ Stop Network")
        else:
            log.error("The location of wired_icon is not found.")
    else:
        log.error('FAIL: Network status is not at "Start", so can\'t stop or restart.')
        # common_function.fail_report('FAIL: Network status is not at "Start", so can\'t stop or restart.')
        return False
    time.sleep(5)
    network_status = os.popen("mclient --quiet get tmp/network/status").readlines()[0].strip()
    wired_icon_stop = image_match_new('wired_icon_stop', 1)
    if network_status == "1" and wired_icon_stop is None:
        log.error("+ FAIL: Failed to stop network. Network status is still available now.")
        # common_function.fail_report("Failed to stop network")
        return False
    elif network_status == "0" and wired_icon_stop is not None:
        log.info("+ PASS: Successfully stopped the network. Network status is not available now.")
    else:
        log.error("+ FAIL: Network status is abnormal.")
        # common_function.fail_report("FAIL: Network status is abnormal.")
        return False


# Description: Start network from the wired tray icon at desktop.
# Parameters: N/A
# Example: start_network()
def start_network():
    network_status = os.popen("mclient --quiet get tmp/network/status").readlines()[0].strip()
    if network_status == "0":
        max_loc = image_match_new('wired_icon_stop', 1)
        if max_loc is not None:
            pyautogui.click(max_loc)
            time.sleep(1)
            pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(1)
            log.info("+ Start Network")
    else:
        log.error('FAIL: Network status is not at "Stop", so can\'t start.')
        # common_function.fail_report('FAIL: Network status is not at "Stop", so can\'t start.')
        return False
    time.sleep(8)
    network_status = os.popen("mclient --quiet get tmp/network/status").readlines()[0].strip()
    wired_icon = image_match_new('wired_icon', 1)
    if network_status == "1" and wired_icon is not None:
        log.info("+ PASS: Successfully started the network. Network status is available now.")
    elif network_status == "0" and wired_icon is None:
        log.error("+ FAIL: Failed to start network. Network status is not available now.")
        # common_function.fail_report("Failed to start network")
        return False
    else:
        log.error("+ FAIL: Network status is abnormal.")
        # common_function.fail_report("After starting network, network status becomes abnormal.")
        return False


# Description: Restart network from the wired tray icon at desktop.
# Parameters: N/A
# Example: restart_network()
def restart_network():
    network_status = os.popen("mclient --quiet get tmp/network/status").readlines()[0].strip()
    if network_status == "1":
        max_loc = image_match_new('wired_icon', 1)
        if max_loc is not None:
            pyautogui.click(max_loc)
            time.sleep(1)
            pyautogui.press('down', presses=2, interval=0.1)
            pyautogui.press('enter')
            time.sleep(1)
            log.info("+ Restart Network")
    else:
        log.error('FAIL: Network status is not at "Start", so can\'t stop or restart.')
        # common_function.fail_report('FAIL: Network status is not at "Start", so can\'t stop or restart.')
        return False
    time.sleep(15)
    network_status = os.popen("mclient --quiet get tmp/network/status").readlines()[0].strip()
    wired_icon = image_match_new('wired_icon', 1)
    if network_status == "1" and wired_icon is not None:
        log.info("+ PASS: Successfully restarted the network. Network status is available now.")
    elif network_status == "0" and wired_icon is None:
        log.error("+ FAIL: Failed to restart network. Network status is not available now.")
        # common_function.fail_report("Network status is not available after restart network")
        return False
    else:
        log.error("+ FAIL: Network status is abnormal.")
        # common_function.fail_report("Network status is abnormal after restarting network.")
        return False
