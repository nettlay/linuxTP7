import time
import os
import pyautogui as pag
import cv2
from Test_Script import common_function
from Test_Script import get_config as gc


class Cert:
    def __init__(self, cert_name='ROOTCA'):
        self.cert_name = cert_name
        self.log = common_function.logger()

    def check_cert(self):
        cer = os.popen('ls /usr/local/share/ca-certificates/').readlines()
        if self.cert_name + '.crt\n' in cer:
            self.log.info('check cert: certificates is exists')
            return True
        else:
            self.log.info('check cert: certificates is not exists')
            return False

    def import_cert(self):
        window = self.control_panel()
        if window is False:
            time.sleep(2)
            self.log.error('import cert not find control window')
            pag.hotkey('ctrl', 'alt', 'f4')
            return False
        insert = self.image_match('import_url', 3)
        if insert is None:
            self.log.error('import cert fail,not find add button')
            pag.hotkey('ctrl', 'alt', 'f4')
            return False
        pag.click(insert)
        time.sleep(2)
        pag.typewrite('ftp://ostestftp.sh.dto/Certs/' + self.cert_name + '.cer', interval=0.1)
        pag.press('enter')
        time.sleep(20)
        import_success = self.image_match('import_success', 5)
        if import_success is None:
            pag.screenshot('./Test_Report/import_cert_fail.png')
            self.log.error('import cert fail,not find import_success.png')
            pag.press('tab', presses=2, interval=0.1)
            pag.press('space')
            time.sleep(1)
            pag.hotkey('ctrl', 'alt', 'f4')
            return False
        time.sleep(1)
        pag.press('space')
        time.sleep(2)
        pag.press('tab', presses=2, interval=0.1)
        pag.press('space')
        cert = self.find_cert()
        pag.hotkey('ctrl', 'alt', 'f4')
        if cert is not None:
            self.log.info('import cert success')
            return True
        else:
            self.log.error('import cert fail, not find cert after import cert')
            return False

    def delete_cert(self):
        window = self.control_panel()
        if window is False:
            time.sleep(2)
            self.log.error('delete cert not find control window')
            pag.hotkey('ctrl', 'alt', 'f4')
            return False
        cert = self.find_cert()
        if cert is False:
            self.log.error('delete cert fail')
            pag.hotkey('ctrl', 'alt', 'f4')
            return False
        pag.click(cert)
        remove = self.image_match('remove', 3)
        if remove is None:
            self.log.error('not find remove button')
            pag.hotkey('ctrl', 'alt', 'f4')
            return False
        pag.click(remove)
        time.sleep(3)
        pag.press('left')
        pag.press('enter')
        time.sleep(10)
        cert = self.find_cert()
        pag.hotkey('ctrl', 'alt', 'f4')
        if cert is False:
            self.log.info('remove cert success')
            return True
        else:
            self.log.error('remove cert fail')
            return False

    def find_cert(self):
        cert = self.image_match(self.cert_name, 3)
        if cert is None:
            return False
        else:
            return cert

    def control_panel(self):
        pag.hotkey('ctrl', 'alt', 's')
        time.sleep(2)
        pag.typewrite('certificates', interval=0.1)
        pag.press('enter')
        max_loc = self.image_match('control_panel', 5)
        if max_loc is None:
            pag.hotkey('ctrl', 'alt', 'f4')
            self.log.error('not find control panel window')
            return False

    @staticmethod
    def image_match(image_name, times):
        width, height = pag.size()
        image_path = ''
        if width == 1920:
            cert_pictures = gc.get_config('cert_pictures')['1920x1200']
        elif width == 1366 and height == 768:
            cert_pictures = gc.get_config('cert_pictures')['1366x768']
        else:
            return None
        pictures = cert_pictures[image_name]
        for picture in pictures:
            if width == 1920:
                image_path = './Test_Data/1920x1200/cert/' + picture + '.png'
            if width == 1366 and height == 768:
                image_path = './Test_Data/1366x768/cert/' + picture + '.png'
            if image_path == '':
                return None
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
