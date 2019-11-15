import pyautogui
import os
import sys
from Test_Script import wired_common
from Test_Script import common_function


log = common_function.logger()


# Description: Check the network method, if it is Automatic, return the ip address. If it is Static,
#              change the network to Auto then get the ip.
#              Used in the script auto_get_ip_by_dhcp.py.
# Parameters:
#           Input: network_type -- 'Wired'
#           Output: current ip address
# Example: check_method_for_auto('Wired')
def check_method_for_auto(network_type):
    # pyautogui.hotkey('ctrl', 'alt', 'end')
    network_method = wired_common.get_network_method(network_type)
    if network_method == 'Automatic':
        my_address = os.popen("ifconfig eth0 | grep -i 'inet addr' | awk '{print $2}' | cut -d':' -f \
        2").readlines()[0].strip()
        # my_vlan = os.popen("ifconfig eth0 | grep -i 'inet addr' | awk '{print $2}' | cut -d':' -f 2 | cut -d'.' \
        # -f3").readlines()[0].strip()
        return my_address
    elif network_method == 'Static':   # If the current network is static, change it to Auto, then get ip.
        wired_common.set_method_as('Automatic')
        check_method_for_auto(network_type)
    else:
        log.info("Fail: No such method " + network_method)
        # common_function.fail_report("Fail: No such method %s" % network_method)
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


# Description: Check the format of ip. Used for auto_get_ip_by_dhcp.py
# Parameters: N/A
def check_ip():
    my_ip_address = os.popen("ifconfig eth0 | grep -i 'inet addr' | awk '{print $2}' | cut -d':' -f \
        2").readlines()[0].strip()
    if len(my_ip_address) == 0:
        log.info("FAIL: Ethernet didn't get any address.")
        # common_function.fail_report("FAIL: Ethernet didn't get any address.")
        return False
    if wired_common.check_ip_format(my_ip_address) is True:
        log.info("PASS: My IP address is %s" % my_ip_address)
    else:
        log.info("FAIL: No such IP address format.")
        # common_function.fail_report("Get the IP address with incorrect format")
        return False

