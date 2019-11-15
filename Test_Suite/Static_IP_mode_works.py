from Test_Script import common_function
from Test_Script import wired_common
from Test_Script import wired_static_ip
import time
import pyautogui


def run():
    test_case_name = "Static_IP_Mode_works"
    # Check current network status
    if common_function.check_network_status() is False:
        common_function.fail_report("Check current network status failed.", test_case_name)
        return
    # If vpn is set, disable it.
    if wired_common.disable_vpn() is False:
        common_function.fail_report("Disable vpn failed.", test_case_name)
        return
    # Check the network method, if it is Automatic, change the network to static and return the ip.
    ip = wired_static_ip.check_method_for_static("Wired")
    if ip is False:
        common_function.fail_report("Check method for static failed.", test_case_name)
        return
    time.sleep(5)
    # Check the network setting result. If checking for Static, it compares the runtime ip, registry ip and \
    # transferring ip.
    if wired_common.setting_check_for("Static", ip[0], ip[1], ip[2]) is False:
        common_function.fail_report("Setting check for static is failed.", test_case_name)
        return
    # Check current network status
    if common_function.check_network_status() is False:
        common_function.fail_report("Check network status failed after network setting.", test_case_name)
        return
    # Ping the default gateway.
    if wired_common.destination_ping_check("Normal", ip[2]) is False:
        common_function.fail_report("Ping default gateway failed.", test_case_name)
        return
    # Enable left click menu for wired icon from registry.
    wired_common.enable_left_click_nt()
    # Stop network from the wired tray icon at desktop
    if wired_common.stop_network() is False:
        common_function.fail_report("Stop Network failed.", test_case_name)
        return
    # Start network from the wired tray icon at desktop.
    if wired_common.start_network() is False:
        common_function.fail_report("Start network failed.", test_case_name)
        return
    time.sleep(5)
    # Check the network setting result after stopping then starting network.
    if wired_common.setting_check_for("Static", ip[0], ip[1], ip[2]) is False:
        common_function.fail_report("Setting check for static is failed after stopping then starting network.",
                                    test_case_name)
        return
    # Ping the default gateway after stopping and restarting network.
    if wired_common.destination_ping_check("Normal", ip[2]) is False:
        common_function.fail_report("Ping default gateway failed after stopping then starting network.", test_case_name)
        return
    # Restart network.
    if wired_common.restart_network() is False:
        common_function.fail_report("Restart network failed.", test_case_name)
    time.sleep(5)
    # Check the network setting result after restarting network.
    if wired_common.setting_check_for("Static", ip[0], ip[1], ip[2]) is False:
        common_function.fail_report("Setting check for static is failed after restarting network.",
                                    test_case_name)
        return
    # Ping the default gateway after restarting network.
    if wired_common.destination_ping_check("Normal", ip[2]) is False:
        common_function.fail_report("Ping default gateway failed after restarting network.", test_case_name)
        return
    # Restore to Auto network.
    wired_common.set_method_as("Automatic")
    # Restore the registry settings for network left click menu
    wired_common.disable_left_click_nt()
    # Print pass result
    common_function.pass_report(test_case_name)
