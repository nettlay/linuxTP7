import pyautogui
import time
import os
from Test_Script import wired_common
from Test_Script import common_function


log = common_function.logger()


# Description: Check the network method, if it is Automatic, change the network to static and return the ip.
#              Used in the script auto_get_ip_by_static.py.
# Parameters:
#              Input: network_type -- 'Wired'
#              Output: static_ip, submask, static_gw
# Example: check_method_for_static('Wired')
def check_method_for_static(network_type):
    # pyautogui.hotkey('ctrl', 'alt', 'end')
    network_method = wired_common.get_network_method(network_type)
    if network_method == 'Automatic':
        # if method is Automatic, get the desired IP and set the static IP information
        # my_vlan = os.popen("ifconfig eth0 | grep -i 'inet addr' | awk '{print $2}' | cut -d':' -f 2 | cut -d'.' -f3")\
        #     .readlines()[0].strip()
        my_default_gateway = os.popen("ip route show | awk '/default/{print $3}'").readlines()[0].strip()
        submask = os.popen("ifconfig eth0 | awk -F':' '/Mask/{print $4}'").readlines()[0].strip()
        # my_default_gateway_list = list(my_default_gateway.split('.'))
        # my_static_ip = int(my_default_gateway_list[3]) + 7
        # static_ip = "15.83." + my_vlan + "." + str(my_static_ip)
        current_ip = os.popen("ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $ 1}' \
        | head -1").readlines()[0].strip()
        static_ip = current_ip
        static_gw = my_default_gateway
        wired_common.set_method_as("Static", static_ip, submask, static_gw)
        return static_ip, submask, static_gw
        # return desired_ip
    elif network_method == 'Static':
        wired_common.set_method_as("Automatic")  # Precondition: the network is static. Change it to auto.
        return check_method_for_static(network_type)
    else:
        log.error("FAIL: No such method, %s" % network_method)
        # failReport "No such method"
        return False

