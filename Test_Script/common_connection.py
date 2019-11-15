import os
import time
import pyautogui
from Test_Script import common_function


# Description: Delete specified types of connections
# Parameters: connection_type -- "xen", "view", "freerdp" and so on, same with the values in \
# Registry root/ConnectionType.
# Example: clear_connections("view")
#          clear_connections("all") -- This is for clearing all types of connections.
def clear_connections(connection_type):
    log = common_function.logger()
    # If there are active connections, stop them.
    conn_type_list = ["custom", "firefox", "freerdp", "ssh", "telnet", "view", "xdmcp", "xen", "all"]
    for conn_type in conn_type_list:
        if conn_type == connection_type:
            if connection_type == "all":
                active_connections = os.popen("connection-mgr listActive | awk '{print $1}'").readlines()
            else:
                active_connections = os.popen("connection-mgr listActive | grep %s | awk '{print $1}'" %
                                              conn_type).readlines()
            length = len(active_connections)
            if length != 0:
                for conn in active_connections:
                    conn = conn.strip()
                    os.popen("connection-mgr stop %s" % conn)
            # Delete connections according to connection_type
            # If connection_type is "all", create a list for all connection types then delete
            if connection_type == "all":
                connection_types = os.popen("mclient --quiet get \"root/ConnectionType\"").readlines()
                print("connection types: ", connection_types)
                for var in connection_types:
                    var = var.strip()
                    connections = os.popen("mclient --quiet get %s/connections" % var).readlines()
                    if len(connections) != 0:
                        for conn_specified in connections:
                            conn_specified = conn_specified.strip()
                            os.popen("mclient --quiet delete %s && mclient commit" % conn_specified)
            else:
                connections = os.popen("mclient --quiet get root/ConnectionType/%s/connections" % conn_type).\
                    readlines()
                if len(connections) != 0:
                    for conn_specified in connections:
                        conn_specified = conn_specified.strip()
                        os.popen("mclient --quiet delete %s && mclient commit" % conn_specified)
        # else:
        #     log.error("The connection type %s doesn't exist." % connection_type)
        #     return False


def start_connection():
    # close the Connection Manager window
    pyautogui.hotkey('ctrl', 'alt', 's')
    pyautogui.typewrite('Connection Manager')
    pyautogui.hotkey('enter')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'alt', 'f4')
    time.sleep(2)
    # launch the latest created Browser connection
    pyautogui.hotkey('ctrl', 'alt', 's')
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(60)
    # time.sleep(5)
    # checkWindow "Mozilla Firefox"
    # checkWindow "It occurs error when start web browser"
    pyautogui.hotkey('ctrl', 'alt', 's')
    time.sleep(1)
    pyautogui.typewrite('X Terminal')
    # time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(1)
    # ps aux | grep -i "$test_name_key_word" | grep -v "grep" | grep -v "$myname" &>/dev/null
    check_process_string = "ps aux | grep -i \"" + test_name_key_word + "\" | grep -v \"grep\" | grep -v \"" + \
                           myname + "\" &>/dev/null"
    # print("check_process_string: ", check_process_string)
    pyautogui.typewrite(check_process_string)
    pyautogui.hotkey('enter')
    time.sleep(1)
    pyautogui.typewrite('echo $? >/tmp/exit_code.txt')
    pyautogui.hotkey('enter')
    time.sleep(1)
    # close X Terminal
    pyautogui.hotkey('ctrl', 'alt', 'f4')
    time.sleep(2)
    exit_code = os.popen('cat /tmp/exit_code.txt').readlines()
    flag = exit_code[0].strip()
    # print(flag)
    if flag != '0':
        print("FAIL : Connection start FAIL")
        # Summary
        # renameLogFile
        # clearCreatedConnection
        # failReport "Failed to start connection"
        exit(1)
    elif flag == '0':
        print("PASS : Connection starts PASS")
    # print("done")


# test_name_key_word = "firefox"
# myname = "auto_firefox"
# start_connection()
# clear_all_connections()


# active_connections = os.popen("connection-mgr listActive | awk '{print $1}'").readlines()
# print("active_connections: ", active_connections)
# connections = os.popen("mclient --quiet get root/ConnectionType/view/connections").readlines()
# clear_connections("freerdp")
