import Test_Script.rdp_logon as rdp_logon
import pyautogui as pg
import traceback
from Test_Script import common_function
from Test_Script import common_connection


# Example: run_single("RDP_Logon_SpecUser2")
def run_single(profile):
    pg.hotkey('ctrl', 'altleft', 'end')
    logon = rdp_logon.LogonTestSpec(profile)
    test_name = "FreeRDP_with_spec_" + profile
    try:
        result = logon.login_spec(profile, test_name)
        if result is True:
            return result
    except Exception as e:
        traceback.print_exc()
        print("Error", e)


def run():
    test_case_name = "FreeRDP_with_spec"
    # create list for specusers
    profile_list = [
        'RDP_Logon_SpecUser1',
        'RDP_Logon_SpecUser2',
        'RDP_Logon_SpecUser3',
        'RDP_Logon_SpecUser4',
        'RDP_Logon_SpecUser5',
        'RDP_Logon_SpecUser6'
    ]
    pass_box = 0
    for item in profile_list:
        common_connection.clear_connections('freerdp')  # Delete rdp connections if there exist.
        if run_single(item) is True:
            pass_box = pass_box + 1
    if pass_box == 6:
        common_function.pass_report(test_case_name)
    else:
        common_function.fail_report("RDP test for special user is failed.", test_case_name)

