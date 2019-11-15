import os
import time
from Test_Script import common_function


# Example: change_view_sec_allow_all("root/ConnectionType/view/connections")
def change_view_sec_allow_all(reg_dir):
    log = common_function.logger()
    uuid = os.popen("mclient --quiet get \"" + reg_dir + "\"").readlines()
    length = len(uuid)
    if length == 0:
        log.error("no vmware connection created")
        return False
    uuid_vmware = uuid[0].strip()
    os.popen('mclient set %s/viewSecurityLevel "Allow all connections" && mclient --quiet commit' % uuid_vmware)
    time.sleep(1)
    get_sec_level = os.popen("mclient --quiet get %s/viewSecurityLevel" % uuid_vmware).readlines()[0].strip()
    return get_sec_level


# a = change_view_sec_allow_all("root/ConnectionType/view/connections")
# print(a)

