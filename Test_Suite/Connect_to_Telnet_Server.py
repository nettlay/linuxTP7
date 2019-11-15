import pyautogui
import time
import sys,os
import yaml
import Test_Script.common_function as co


log = co.logger()


def run():
    # path = os.path.dirname(os.getcwd())
    # load yaml
    log.info('load yaml')
    f = open(r'./Test_Data/config.yml')
    info = yaml.load(f)
    server_address = info['telnet_server_address']
    user_name = info['telnet_user_name']
    pass_word = info['telnet_pass_word']
    # write log
    # f2 = open(path+r'/Test_Report/telnet_result.txt','w')
    # pyautogui setting
    log.info('default settings')
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = (0.5)
    # auto steps start
    log.info('auto steps start')
    screen_width, screen_height = pyautogui.size()
    pyautogui.hotkey('ctrlleft', 'alt', 's')
    time.sleep(1)
    pyautogui.typewrite('create telnet')
    pyautogui.hotkey('enter')
    time.sleep(1)
    pyautogui.click(0.5 * screen_width, 0.5 * screen_height, duration=1)
    # image locate on screen
    #address
    address_pos = pyautogui.locateOnScreen(r'./Test_Data/1920x1200/template_file/telnet_address.png')
    # time.sleep(1)
    if address_pos is None:
        print('fail1 ')
        log.error('fail1')
        # f2.write('fail1 ')
    pyautogui.click(address_pos.left + 2 * address_pos.width, address_pos.top + 0.5 * address_pos.height, duration=1)
    pyautogui.typewrite(server_address)
    # image locate on screen
    #finish
    finish_pos = pyautogui.locateCenterOnScreen(r'./Test_Data/1920x1200/template_file/ssh_telnet_finish.png')
    # time.sleep(1)
    if finish_pos is None:
        print('fail2 ')
        log.error('fail2')
        # f2.write('fail2 ')
    pyautogui.click(finish_pos.x, finish_pos.y, duration=1)
    time.sleep(3)
    pyautogui.hotkey('ctrlleft', 'alt', 's')
    pyautogui.typewrite('new telnet')
    pyautogui.hotkey('enter')
    time.sleep(20)
    pyautogui.click(0.5 * screen_width, 0.5 * screen_height, duration=1)
    pyautogui.typewrite(user_name)
    pyautogui.hotkey('enter')
    time.sleep(1)
    pyautogui.typewrite(pass_word)
    pyautogui.hotkey('enter')
    time.sleep(2)
    log.info('auto steps finish,checking result...please wait')
    is_pass = pyautogui.locateOnScreen(r'./Test_Data/1920x1200/template_file/ssh_telnet_pass.png')
    if is_pass is not None:
        co.pass_report("Connect_to_Telnet_Server")
        log.info('the resule is pass,please check the log file for detail')
        # f2.write('pass ')
        pyautogui.hotkey('ctrlleft','d')
        return
    else:
        co.fail_report("Connect failed", "Connect_to_Telnet_Server")
        log.error('fail3')
        # f2.write('fail3 ')
        pyautogui.hotkey('ctrlleft','d')
        return

