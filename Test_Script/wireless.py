import os
import pyautogui as pag
import time
import cv2
from Test_Script import get_config as gc
from Test_Script import common_function


class Wireless:
    def __init__(self, wireless_name, password):
        self.wireless_name = gc.get_config(wireless_name)
        self.password = gc.get_config(password)
        self.log = common_function.logger()

    def check_wireless(self):
        if len(os.popen('iwconfig wlan0').readlines()) == 0:
            self.log.error('not find wlan device')
            return 'not find wlan device'
        else:
            return True

    @staticmethod
    def clear_profiles():
        profiles = os.popen('mclient get root/Network/Wireless/Profiles').readlines()
        for i in profiles:
            os.popen('mclient delete %s && mclient commit' % i.strip('dir').strip())

    def delete_profiles(self):
        profile = self.image_match(self.wireless_name+'_connect', 3)
        if profile is None:
            self.log.error('not find profile when execute delete profile')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find profile when execute delete profile'
        pag.click(profile)
        delete = self.image_match('delete', 3)
        if delete is None:
            self.log.error('not find delete button or delete is gray')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find delete button or delete is gray'
        pag.click(delete)
        time.sleep(2)
        pag.press('space')
        apply = self.image_match('apply', 3)
        if apply is None:
            self.log.error('apply button is gray or unavailable')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'apply button is gray or unavailable'
        pag.click(apply)
        if self.image_match(self.wireless_name+'_connect', 3) is not None:
            self.log.error('delete profile fail')
            return 'delete profile fail'
        self.log.info('delete %s success' % self.wireless_name)
        return True

    @staticmethod
    def open_wireless():
        time.sleep(1)
        pag.hotkey('ctrl', 'alt', 's')
        time.sleep(1)
        pag.typewrite('network', interval=0.1)
        pag.press('enter')
        time.sleep(5)
        pag.press('tab', presses=3, interval=0.1)
        pag.press('right')

    def add_wireless(self):
        add = self.image_match('add', 10)
        if add is None:
            self.log.error('not find add button')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find add button'
        pag.click(add)
        scan_ap = self.image_match('scan_ap', 10)
        if scan_ap is None:
            self.log.error('not find scan ap button')
            pag.hotkey('ctrl', 'alt', 'f4')
            time.sleep(1)
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find scan ap button'
        for i in range(5):
            pag.click(scan_ap)
            if self.image_match('scanning', 3) is not None:
                break
            time.sleep(1)
            print('not find scanning')
            if i == 4:
                self.log.error('click scan ap have no response')
                pag.hotkey('ctrl', 'alt', 'f4')
                time.sleep(1)
                pag.hotkey('ctrl', 'alt', 'f4')
                return 'click scan ap have no response'
        self.log.info('scan ap success')
        time.sleep(8)
        pag.press('tab', presses=5, interval=0.1)
        i = 30
        while i:
            if self.image_match(self.wireless_name, 2) is not None:
                self.log.info('find wireless success')
                if i == 30:
                    pag.press('space')
                    pag.press('enter')
                return True
            pag.press('down')
            i -= 1
            if i == 0:
                pag.hotkey('ctrl', 'alt', 'f4')
                time.sleep(1)
                pag.hotkey('ctrl', 'alt', 'f4')
                return 'not find  wireless success'

    def connect_with_security(self, security='wpa2p'):
        pag.click(self.image_match('security', 3))
        i = 8
        while i:
            if security == 'wpa2p':
                security_option = security.upper()+'_security'
            else:
                return 'not find WPA/WPA2A security'
            if self.image_match(security_option, 2) is not None:
                self.log.info('choose security is WPA/WPA2A')
                break
            pag.press('down')
            i -= 1
            if i == 0:
                self.log.error('not find WPA/WPA2A security')
                pag.hotkey('ctrl', 'alt', 'f4')
                time.sleep(1)
                pag.hotkey('ctrl', 'alt', 'f4')
                return 'not find WPA/WPA2A security'
        pag.press('tab')
        if '<' in self.password:
            index = self.password.index('<')
            pag.typewrite(self.password[:index], interval=0.1)
            pag.hotkey('shift', ',')
            pag.typewrite(self.password[index + 1:], interval=0.1)
        else:
            pag.typewrite(self.password, interval=0.1)
        apply = self.apply_settings()
        if apply is not True:
            return apply
        self.log.info('connect to %s' % self.wireless_name)
        return True

    def apply_settings(self):
        ok = self.image_match('ok_button', 3)
        if ok is None:
            self.log.error('ok button is gray or unavailable')
            pag.hotkey('ctrl', 'alt', 'f4')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'ok button is gray or unavailable'
        pag.click(ok)
        time.sleep(1)
        apply = self.image_match('apply', 3)
        if apply is None:
            self.log.error('apply button is gray or unavailable')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'apply button is gray or unavailable'
        pag.click(apply)
        return True

    def check_profile(self):
        connect = self.image_match(self.wireless_name+'_connect', 3)
        if connect is not None:
            return True
        else:
            return False

    @staticmethod
    def disable_click_menu():
        os.popen('mclient set root/Network/disableLeftClickMenu 0 && mclient commit')

    def check_auto_connect(self):
        self.disable_click_menu()
        self.log.info('disable network click menu')
        time.sleep(3)
        network_icon = self.image_match('network_icon', 5)
        if network_icon is None:
            self.log.error('not find network icon')
            return 'not find network icon'
        pag.click(network_icon)
        time.sleep(1)
        pag.press('down')
        pag.press('enter')
        time.sleep(5)
        pag.click(network_icon)
        time.sleep(1)
        pag.press('down')
        pag.press('enter')
        time.sleep(30)
        if self.ping() is False:
            return 'click start network and ping to network fail'
        self.log.info('stop and start network,ping to network success')
        pag.click(network_icon)
        pag.press('down', presses=2, interval=0.1)
        pag.press('enter')
        time.sleep(30)
        if self.ping() is False:
            return 'click restart network and ping to network fail'
        self.log.info('restart network,ping to network success')
        return True

    def del_profile(self):
        pag.click(self.image_match(self.wireless_name + '_connect', 5))
        pag.press('tab', presses=3, interval=0.1)
        pag.press('space')
        time.sleep(3)
        pag.press('space')
        if self.check_profile():
            return False
        pag.click(self.image_match('apply', 3))
        self.log.info('delete profile success')
        return True

    def ping(self):
        if len(os.popen('ping 19.83.240.98 -c 5').readlines()) == 0:
            return False

    def switch_wired(self, times, wired='down'):
        value1 = os.popen('mclient get root/Network/Wired/Method').readlines()[0].\
            strip('default').strip('value').strip()
        value2 = os.popen('mclient get root/Network/WiredWirelessSwitch').readlines()[0].\
            strip('default').strip('value').strip()
        if wired == 'down':
            if value1 == 'Static' and value2 == '0':
                return True
            else:
                os.popen('mclient set root/Network/Wired/Method Static && mclient commit')
                os.popen('mclient set root/Network/WiredWirelessSwitch 0 && mclient commit')
                self.write_boot_time(times)
                self.reboot()
        if wired == 'up':
            if value1 == 'Automatic' and value2 == '1':
                return True
            else:
                os.popen('mclient set root/Network/Wired/Method Automatic && mclient commit')
                os.popen('mclient set root/Network/WiredWirelessSwitch 1 && mclient commit')
                self.write_boot_time(times)
                if times == 'remove':
                    os.remove('boot_times.txt')
                    self.clear_profiles()
                self.reboot()

    @staticmethod
    def reboot():
        os.popen('reboot')
        time.sleep(30)

    @staticmethod
    def image_match(image_name, times):
        width, height = pag.size()
        image_path = ''
        if width == 1920:
            view_pictures = gc.get_config('wireless_pictures')['1920x1200']
        elif width == 1366 and height == 768:
            view_pictures = gc.get_config('wireless_pictures')['1366x768']
        else:
            return None
        pictures = view_pictures[image_name]
        for picture in pictures:
            if width == 1920:
                image_path = './Test_Data/1920x1200/wireless/' + picture + '.png'
            if width == 1366 and height == 768:
                image_path = './Test_Data/1366x768/wireless/' + picture + '.png'
            img = cv2.imread(image_path)
            for i in range(times):
                pag.screenshot('screen_shot.png')
                img2 = cv2.imread('screen_shot.png')
                test = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(test)
                time.sleep(1)
                if max_val > 0.95:
                    return max_loc
        return None

    @staticmethod
    def read_boot_time():
        try:
            with open('boot_times.txt', 'r') as file:
                return file.readlines()[0]
        except:
            return False

    @staticmethod
    def write_boot_time(content):
        with open('boot_times.txt', 'w') as file:
            file.write(content)

    def connect_hidden_wireless(self):
        add = self.image_match('add', 10)
        if add is None:
            self.log.error('not find add button')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find add button'
        pag.click(add)
        time.sleep(2)
        pag.press('tab')
        pag.typewrite('%s' % self.wireless_name)
        pag.press('tab', presses=2, interval=0.1)
        pag.press('space')
        connect = self.connect_with_security()
        if connect is not True:
            return connect
        return True

    @staticmethod
    def get_ip():
        sub_mask = os.popen("ifconfig wlan0 | awk -F':' '/Mask/{print$4}'").readlines()[0].strip()
        default_getway = os.popen("ip route show | awk '/default/{print $3}'").readlines()[0].strip()
        ip_address = os.popen("ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $ 1}' | "
                              "head -1").readlines()[0].strip()
        return sub_mask, default_getway, ip_address

    def static_method(self):
        if self.ping() is False:
            return 'ping to network fail'
        sub_mask, default_getway, ip_address = self.get_ip()
        self.log.info('get sub_mask, default_getway, ip_address success')
        pag.click(self.image_match(self.wireless_name+'_connect', 3))
        edit = self.image_match('edit', 3)
        if edit is None:
            self.log.error('not find edit button')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find edit button'
        pag.click(edit)
        ipv4 = self.image_match('IPv4', 3)
        if ipv4 is None:
            pag.hotkey('ctrl', 'alt', 'f4')
            time.sleep(1)
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find ipv4 option'
        pag.click(ipv4)
        pag.press('tab', presses=2, interval=0.1)
        pag.press('down')
        time.sleep(1)
        pag.press('tab')
        pag.typewrite(ip_address, interval=0.1)
        pag.press('tab')
        pag.typewrite(sub_mask, interval=0.1)
        pag.press('tab')
        pag.typewrite(default_getway, interval=0.1)
        apply = self.apply_settings()
        if apply is not True:
            return apply
        return True

    @staticmethod
    def switch_root():
        pag.rightClick((pag.size()[0], 0))
        time.sleep(1)
        pag.press('down', presses=3)
        pag.press('enter')
        time.sleep(2)
        pag.typewrite('1')
        pag.press('enter')
        time.sleep(2)
