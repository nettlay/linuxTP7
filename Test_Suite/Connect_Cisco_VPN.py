from Test_Script import common_function
from Test_Script import wired_common
from Test_Script import wired_vpn
import time


def run():
    test_case_name = "Connect_Cisco_VPN"
    # Read VPN configuration from yaml -- To be optimized
    vpn_cisco_gw = wired_common.get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "vpn_cisco_gw")
    vpn_cisco_gn = wired_common.get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "vpn_cisco_gn")
    vpn_cisco_gp = wired_common.get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "vpn_cisco_gp")
    vpn_cisco_un = wired_common.get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "vpn_cisco_un")
    vpn_cisco_up = wired_common.get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "vpn_cisco_up")
    target_type = wired_common.get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "target_type")
    vpn_auto_start = wired_common.get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "vpn_auto_start")
    vpn_destination = wired_common.get_config("./Test_Data/WiredNetwork/", "wired_configuration.yml", "vpn_destination")
    # Check current network status.
    if common_function.check_network_status() is False:
        common_function.fail_report("Failed to check network status.", test_case_name)
        return
    # Set VPN as Cisco.
    if wired_vpn.set_vpn_as_cisco(target_type, vpn_cisco_gw, vpn_cisco_gn, vpn_cisco_gp, vpn_cisco_un, vpn_cisco_up) \
            is not True:
        common_function.fail_report("Failed to set vpn settings as cisco", test_case_name)
        return
    # Wait some while for vpn settings taking effect
    time.sleep(60)
    # Check vpn settings
    if wired_vpn.check_cisco_settings(target_type, vpn_auto_start, vpn_cisco_gw, vpn_cisco_gn, vpn_cisco_un) is False:
        common_function.fail_report("Fail to check cisco settings.", test_case_name)
        return
    # Ping
    if wired_common.destination_ping_check("VPN", vpn_destination) is False:
        common_function.fail_report("Fail to ping destination.", test_case_name)
        return
    # Disable Cisco VPN setings to restore the testing environment
    vpn_info_reg = wired_vpn.get_value_from_reg()
    if vpn_info_reg is not False:
        wired_vpn.disable_cisco_vpn(vpn_info_reg[3], vpn_info_reg[0])
    # else:
    #     return
    # Print pass report
    common_function.pass_report(test_case_name)

