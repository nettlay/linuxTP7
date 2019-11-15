from Test_Script import wired_common
from Test_Script import wired_dhcp_ip
from Test_Script import common_function


def run():
    test_case_name = "Dynamic_IP_Mode"
    # Check current network status
    if common_function.check_network_status() is False:
        common_function.fail_report("Check current network status failed.", test_case_name)
        return
    # If vpn is set, disable it.
    if wired_common.disable_vpn() is False:
        common_function.fail_report("Disable vpn failed.", test_case_name)
        return
    # Check the network method, if it is Automatic, return the ip address. If it is Static, change the network to \
    # Auto then get the ip.
    if wired_dhcp_ip.check_method_for_auto('Wired') is False:
        common_function.fail_report("Check method for auto failed.", test_case_name)
        return
    # Check the format of ip, all the four address should be in [0, 255].
    if wired_dhcp_ip.check_ip() is False:
        common_function.fail_report("Check ip failed.", test_case_name)
        return
    # Check current network status in case of changing network to Automatic from Static.
    if common_function.check_network_status() is False:
        common_function.fail_report("Check network status is failed after checking method.", test_case_name)
        return
    # Check the network setting result.
    if wired_common.setting_check_for("Automatic") is False:
        common_function.fail_report("Setting check for Automatic failed.", test_case_name)
        return
    # Ping the destination.
    if wired_common.destination_ping_check("Normal", "15.83.240.98") is False:
        common_function.fail_report("Destination ping failed after network setting for preparation.", test_case_name)
        return
    # Enable left click menu for wired icon from registry.
    wired_common.enable_left_click_nt()
    # Stop network from the wired tray icon at desktop
    if wired_common.stop_network() is False:
        common_function.fail_report("Stop network failed.", test_case_name)
        return
    # Start network from the wired tray icon at desktop.
    if wired_common.start_network() is False:
        common_function.fail_report("Start network failed.", test_case_name)
    # Check the format of ip after regaining the dynamic IP, all the four address should be in [0, 255].
    if wired_dhcp_ip.check_ip() is False:
        common_function.fail_report("Check ip failed after starting network.", test_case_name)
        return
    # Ping the destination after stopping then starting network.
    if wired_common.destination_ping_check("Normal", "15.83.240.98") is False:
        common_function.fail_report("Destination ping failed after stopping then starting network.", test_case_name)
        return
    # Restart network from the wired tray icon at desktop
    if wired_common.restart_network() is False:
        common_function.fail_report("Restarting network fails.", test_case_name)
        return
    # Check the network setting result after restarting network.
    wired_common.setting_check_for("Automatic")
    # Check the format of ip after restarting network then get the ip, all the four address should be in [0, 255].
    if wired_dhcp_ip.check_ip() is False:
        common_function.fail_report("Check ip failed after restarting network.", test_case_name)
        return
    # Ping the destination after restarting network.
    if wired_common.destination_ping_check("Normal", "15.83.240.98") is False:
        common_function.fail_report("Destination ping failed after restarting network.", test_case_name)
        return
    # Restore the registry settings for network left click menu
    wired_common.disable_left_click_nt()
    # Print pass report
    common_function.pass_report(test_case_name)

