import pyautogui
import time
import sys,os
import yaml
import Test_Script.common_function as co


log = co.logger()


def run():
    # path=os.path.dirname(os.getcwd())
    #load yaml
    log.info('load yaml')
    f = open(r'./Test_Data/config.yml')
    info = yaml.safe_load(f)
    server_address = info['ssh_server_address']
    user_name = info['ssh_user_name']
    pass_word = info['ssh_pass_word']
    #write log
    # f2 = open(path+r'/Test_Report/ssh_result.txt','w')
    #pyautogui setting
    log.info('default settings')
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = (0.5)
    #auto steps start
    log.info('auto steps start')
    screen_width, screen_height = pyautogui.size()
    pyautogui.hotkey('ctrlleft', 'alt', 's')
    time.sleep(1)
    pyautogui.typewrite('create ssh')
    pyautogui.hotkey('enter')
    time.sleep(1)
    pyautogui.click(0.5 * screen_width, 0.5 * screen_height, duration=1)
    #image locate on screen
    #address
    address_pos = pyautogui.locateOnScreen(r'./Test_Data/1920x1200/template_file/ssh_address.png')
    # time.sleep(1)
    if address_pos is None:
        address_pos = pyautogui.locateOnScreen(r'./Test_Data/1920x1200/template_file/ssh_address.png')
        print('failcode1')
        log.error('failcode1')
        # f2.write('fail1 ')
    pyautogui.click(address_pos.left+2 * address_pos.width, address_pos.top+0.5 * address_pos.height, duration=1)
    pyautogui.typewrite(server_address)
    # image locate on screen
    userName_pos = pyautogui.locateOnScreen(r'./Test_Data/1920x1200/template_file/ssh_user_name.png')
    # time.sleep(1)
    if userName_pos is None:
        userName_pos = pyautogui.locateOnScreen(r'./Test_Data/1920x1200/template_file/ssh_user_name.png')
        print('failcode2')
        log.error('failcode2')
        # f2.write('fail2 ')
    pyautogui.click(userName_pos.left + 2 * userName_pos.width, userName_pos.top + 0.5 * userName_pos.height, duration=1)
    pyautogui.typewrite(user_name)
    # image locate on screen
    finish_pos = pyautogui.locateCenterOnScreen(r'./Test_Data/1920x1200/template_file/ssh_telnet_finish.png')
    if finish_pos is None:
        finish_pos = pyautogui.locateCenterOnScreen(r'./Test_Data/1920x1200/template_file/ssh_telnet_finish.png')
        print('failcode3')
        log.error('failcode3')
        # f2.write('fail3 ')
    # time.sleep(1)
    pyautogui.click(finish_pos.x, finish_pos.y, duration=1)
    # time.sleep(1)
    pyautogui.hotkey('ctrlleft', 'alt', 's')
    time.sleep(1)
    pyautogui.typewrite('new ssh')
    time.sleep(0.5)
    pyautogui.hotkey('enter')
    time.sleep(20)
    pyautogui.click(0.5 * screen_width, 0.5 * screen_height)
    pyautogui.typewrite('yes')
    pyautogui.hotkey('enter')
    time.sleep(15)
    pyautogui.typewrite(pass_word)
    pyautogui.hotkey('enter')
    time.sleep(2)
    log.info('auto steps finish,checking result...please wait')
    is_pass = pyautogui.locateOnScreen(r'./Test_Data/1920x1200/template_file/ssh_telnet_pass.png')
    if is_pass is not None:
        # f2.write('pass')
        log.info('the resule is pass,please check the log file for detail')
        co.pass_report("Connect_to_SSH_Server")
        pyautogui.hotkey('ctrlleft','d')
        return
    else:
        # f2.write('didn\'t finish')
        log.error('didn\'t finish')
        co.fail_report("Didn't finish", "Connect_to_SSH_Server")
        pyautogui.hotkey('ctrlleft','d')
        return


