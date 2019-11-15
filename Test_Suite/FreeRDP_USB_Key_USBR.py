from Test_Script.rdp_smart_card_logon import *


def run():
    test = NormalLogonTest()
    test.edit_normal_connection("rfx_win10")
    log.info("set USBR mode")
    test.set_key_usbr()
    test.start_connection()
    time.sleep(8)
    test.upload_test_item_exe_location("//15.83.240.98//Automation//Linux//scripts//usbkey_redirection.exe")
    log.info("upload test_item.txt to FTP")
    test.click_accept_button()
    test_name = "FreeRDP_USB_Key_USBR"
    test.record_result(test_name)



