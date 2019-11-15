import time
import pyautogui
import Test_Script.common_function as co
from Lib.thinpro_citrix import NewController
import Test_Script.Check_window as cw

log = co.logger()


def write_offset_to_printer_yml():
    add_printer_controller = NewController('desktop.png', ['printer_local.png'], 'WINDOW')
    add_printer_controller.click_position_tool('add_icon1.png')
    edit_dict = {'add_printer': add_printer_controller.relative_offset}
    add_printer_controller.dump_to_yaml(edit_dict)
    new_printer_controller = NewController('desktop.png', ['new_printer.png'], 'WINDOW')
    new_printer_controller.click_position_tool('HP_Laserjet_P2035.png')
    edit_dict['chose_printer'] = new_printer_controller.relative_offset
    new_printer_controller.click_position_tool('forward.png')
    edit_dict['confirm'] = new_printer_controller.relative_offset
    new_printer_controller.click_position_tool('apply.png')
    edit_dict['prepare_print'] = new_printer_controller.relative_offset
    new_printer_controller.dump_to_yaml(edit_dict)
    print_page_controller = NewController('desktop.png', ['print_page.png'], 'WINDOW')
    print_page_controller.click_position_tool('print_test_page.png')
    edit_dict['print_test_page'] = print_page_controller.relative_offset
    print_page_controller.dump_to_yaml(edit_dict)
    time.sleep(15)
    submit_controller = NewController('desktop.png', ['submited_ok.png'], 'WINDOW')
    submit_controller.click_position_tool('ok_copy.png')
    edit_dict['submit'] = submit_controller.relative_offset
    submit_controller.dump_to_yaml(edit_dict)
    printer_properties_controller = NewController('desktop.png', ['printer_properties.png',
                                                                  'printer_properties_italic.png', 
                                                                  'printer_properties_italic1.png'], 'WINDOW')
    printer_properties_controller.click_position_tool('ok_small.png')
    edit_dict['printer_properties'] = printer_properties_controller.relative_offset
    printer_properties_controller.dump_to_yaml(edit_dict)
    delete_printer_controller = NewController('desktop.png', ['printer_local.png'], 'WINDOW')
    delete_printer_controller.click_position_tool('printer.png')
    delete_printer_controller.rightclick_position_tool('printer.png')
    edit_dict['delete_printer'] = delete_printer_controller.relative_offset
    delete_printer_controller.dump_to_yaml(edit_dict)
    confirm_deletion_controller = NewController('desktop.png', ['confirm.png'], 'WINDOW')
    confirm_deletion_controller.click_position_tool('delete.png')
    edit_dict['confirm_deletion'] = confirm_deletion_controller.relative_offset
    confirm_deletion_controller.dump_to_yaml(edit_dict)
    cancel_usbupdate_contrller = NewController('desktop.png', ['USB_update.png'], 'WINDOW')
    cancel_usbupdate_contrller.click_position_tool('usb_cancel.png')
    edit_dict['USB_Update'] = cancel_usbupdate_contrller.relative_offset
    cancel_usbupdate_contrller.dump_to_yaml(edit_dict)


def open_window(name, picture):
    pyautogui.hotkey('ctrl', 'alt', 's')
    time.sleep(2)
    pyautogui.typewrite(name)
    time.sleep(2)
    pyautogui.press('enter')
    if cw.check_window("F", picture):
        return True
    else:
        return False


def false_return(button_name):
    msg = "The {} window was not found.".format(button_name)
    log.info(msg)


def add_printer():
    add_printer_controller = NewController('desktop.png', ['printer_local.png'], 'WINDOW')
    flag = add_printer_controller.click_position('add_printer')
    if flag:
        new_printer_controller = NewController('desktop.png', ['new_printer.png'], 'WINDOW')
        new_printer_controller.click_position('chose_printer')
        new_printer_controller.click_position('confirm')
        time.sleep(8)
        new_printer_controller.click_position('prepare_print')
        return True
    else:
        false_return('printer local')
        return False


def cancel_print_page():
    cancel = NewController('desktop.png', ['cancel.png'], 'ICON')
    cancel.click_position('')


def print_page():
    print_page_controller = NewController('desktop.png', ['print_page.png'], 'WINDOW')
    flag = print_page_controller.click_position('print_test_page')
    time.sleep(5)
    if flag:
        co.pass_report("Local_USB_printer_print_test_page")
        submit_controller = NewController('desktop.png', ['submited_ok.png'], 'WINDOW')
        flag = submit_controller.click_position('submit')
    else:
        false_return('print test page')
        co.fail_report("Not found print_test_page button.", "Local_USB_printer_print_test_page")
        return False
    if flag:
        printer_properties_controller = NewController('desktop.png', ['printer_properties.png',
                                                                      'printer_properties_italic.png',
                                                                      'printer_properties_italic1.png'], 'WINDOW')
        flag = printer_properties_controller.click_position('printer_properties')
    else:
        false_return('submit')
        return False
    if flag:
        return True
    else:
        false_return('printer properties')
        return False


def delete_printer():
    delete_printer_controller = NewController('desktop.png', ['printer_local.png'], 'WINDOW')
    flag = delete_printer_controller.rightclick_position('delete_printer')
    if flag:

        pyautogui.press(['down', 'down', 'down', 'down'])
        pyautogui.press('enter')
        confirm_deletion_controller = NewController('desktop.png', ['confirm.png'], 'WINDOW')
        confirm_deletion_controller.click_position( 'confirm_deletion')
    else:
        false_return('printer local')
        return False
    return True


def close_window(picture):
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'alt', 'f4')
    if cw.check_window("T", picture):
        return True
    else:
        return False


def close_usbupdate_window():
    cancel_usbupdate_contrller = NewController('desktop.png', ['USB_update.png'], 'WINDOW')
    if cancel_usbupdate_contrller.click_position('USB_Update'):
        return True
    else:
        return False


