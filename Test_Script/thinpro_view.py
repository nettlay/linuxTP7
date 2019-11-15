import pyautogui as pag
import time
import cv2
from Test_Script import get_config as gc
from Test_Script import common_function
import os


class View:
    def __init__(self, server_name, username, password):
        self.server_name = server_name
        self.username = username
        self.password = password
        self.log = common_function.logger()

    def del_connection(self):
        for i in range(5):
            max_loc = self.image_match('view_icon', 1)
            time.sleep(1)
            if max_loc is not None:
                pag.rightClick(max_loc)
                time.sleep(1)
                pag.press('down', presses=5, interval=0.1)
                pag.press('enter')
                time.sleep(1)

    def create_connection(self):
        pag.rightClick((pag.size()[0], 0))
        time.sleep(1)
        pag.press('down')
        pag.press('right')
        time.sleep(1)
        pag.press('down', presses=2, interval=0.1)
        pag.press('enter')
        self.log.info('execute create connection')

    def edit_connection(self):
        lst = [self.server_name, 'view_server', self.username, self.password, 'domain']
        config = []
        for i in range(len(lst)):
            config.append(gc.get_config(lst[i]))
        time.sleep(2)
        max_loc1 = self.image_match('view_icon', 3)
        if max_loc1 is None:
            self.log.error('not find view icon to edit connection')
            return 'not find view icon to edit connection'
        pag.rightClick(max_loc1)
        pag.press('down', presses=2, interval=0.1)
        pag.press('enter')
        time.sleep(4)
        max_loc2 = self.image_match('view_edit', 3)
        if max_loc2 is None:
            self.log.error('not find view connection edit window')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find view connection edit window'
        self.log.info('open view edit window success')
        time.sleep(1)
        pag.click((max_loc2[0]+300, max_loc2[1]+100))
        pag.hotkey('ctrl', 'a')
        pag.typewrite(config[0], interval=0.1)
        pag.press('tab')
        pag.typewrite(config[1], interval=0.1)
        pag.click((max_loc2[0]+300, max_loc2[1]+285))
        for i in range(2, 5):
            pag.press('tab')
            pag.typewrite(config[i], interval=0.1)
        time.sleep(1)
        ok_button = self.image_match('ok', 3)
        if ok_button is None:
            self.log.error('not find ok button in edit window')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find ok button in edit window'
        pag.click(ok_button)
        self.log.info('enable edit connection')
        time.sleep(1)
        return config[2]

    def start_connection(self):
        icon = self.image_match('view_icon', 3)
        if icon is None:
            self.log.error('not find view icon when start connection')
            return False
        pag.rightClick(icon)
        pag.press('down')
        pag.press('enter')
        self.log.info('execute start connection')
        time.sleep(45)

    def log_on_desktop(self):
        desktop = gc.get_config(self.server_name)
        window = self.image_match('vm_window', 5)
        if window is None:
            self.log.error('not find vm_window after start connection')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find vm_window after start connection'
        pag.doubleClick(window)
        time.sleep(1)
        if pag.size()[1] != 1200:
            if self.server_name != 'blast_server_name':
                pag.press('down', presses=50)
        max_loc = self.image_match(desktop, 5)
        if max_loc is None:
            pag.hotkey('ctrl', 'alt', 'f4')
            self.log.error('not find %s desktop' % self.server_name)
            return 'not find %s desktop' % self.server_name
        pag.doubleClick(max_loc)
        close = self.image_match('connect_fail', 3)
        if close is not None:
            self.log.error('launch desktop fail,please confirm desktop available')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'launch desktop fail,please confirm desktop available'
        self.log.info('execute log_on_desktop success')
        return True

    def logon_fail(self):
        os.popen('pkill view')
        self.log.error('log off fail, window still opened')

    def check_logoff(self):
        time.sleep(75)
        window = self.image_match('vm_window', 5)
        if window is None:
            self.logon_fail()
            return False
        time.sleep(5)
        pag.click(window)
        pag.hotkey('alt', 'ctrl', 'f4')
        self.log.info('log off and close vm broker success')
        return True

    @staticmethod
    def image_match(image_name, times):
        width, height = pag.size()
        image_path = ''
        if width == 1920:
            view_pictures = gc.get_config('view_pictures')['1920x1200']
        # elif width == 1366 and height == 768:
        elif width == 1366:  # Modified by Lena, only judge width 1366.
            view_pictures = gc.get_config('view_pictures')['1366x768']
        else:
            return None
        pictures = view_pictures[image_name]
        for picture in pictures:
            if width == 1920:
                image_path = './Test_Data/1920x1200/VMware/' + picture + '.png'
            # if width == 1366 and height == 768:
            if width == 1366:  # Modified by Lena, only judge width 1366.
                image_path = './Test_Data/1366x768/VMware/' + picture + '.png'
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


# Added by Lena
class ViewSpec(View):

    def __init__(self, server_name, username, password):
        View.__init__(self, server_name, username, password)

    def edit_connection_spec2(self):
        lst = [self.server_name, 'view_server', 'spec_username2', 'domain']
        config = []
        for i in range(len(lst)):
            config.append(gc.get_config(lst[i]))
        max_loc1 = self.image_match('view_icon', 3)
        if max_loc1 is None:
            self.log.error('not find view icon to edit connection')
            return 'not find view icon to edit connection'
        pag.rightClick(max_loc1)
        pag.press('down', presses=2, interval=0.1)
        pag.press('enter')
        max_loc2 = self.image_match('view_edit', 10)
        if max_loc2 is None:
            self.log.error('not find view connection edit window')
            pag.hotkey('ctrl', 'alt', 'f4')
            return 'not find view connection edit window'
        time.sleep(1)
        pag.click((max_loc2[0] + 300, max_loc2[1] + 100))
        pag.hotkey('ctrl', 'a')
        pag.typewrite(config[0], interval=0.1)  # Input spec_server_name
        pag.press('tab')
        pag.typewrite(config[1], interval=0.1)  # Input view_server
        pag.click((max_loc2[0] + 300, max_loc2[1] + 285))  # Click the radio button before using predefined user name\
        # and password
        pag.press('tab')
        pag.typewrite(config[2], interval=0.1)  # Input spec_username2
        pag.press('tab')
        # Input spec password for spec user 2
        pag.typewrite('+=_,-?', interval=0.1)
        pag.hotkey('shift', ',')  # Input '<'
        pag.typewrite('>~', interval=0.1)
        pag.press('tab')
        pag.typewrite(config[3], interval=0.1)  # Input domain
        time.sleep(1)
        pag.click(self.image_match('ok', 3))
        time.sleep(1)
        return config[2]

    def log_on_desktop_spec(self):
        desktop = gc.get_config(self.server_name)
        desktop = desktop[:desktop.rfind('_')]  # Remove the index number of spec_server_name
        window = self.image_match('vm_window', 20)
        pag.doubleClick(window)
        time.sleep(1)
        max_loc = self.image_match(desktop, 6)
        if max_loc is None:
            pag.hotkey('ctrl', 'alt', 'f4')
            self.log.error('not find %s desktop' % self.server_name)
            return 'not find %s desktop' % self.server_name
        pag.doubleClick(max_loc)
        close = self.image_match('connect_fail', 3)
        # If launch desktop is failed for the first time, close the prompt then try again.
        if close is not None:
            # fail_max_loc = self.image_match('connect_fail', 6)
            # if fail_max_loc is None:
            #     pag.hotkey('ctrl', 'alt', 'f4')
            #     self.log.error('Fail prompt not found.')
            #     return 'Fail prompt not found.'
            pag.click(close)  # Close the fail prompt message
            time.sleep(5)
            pag.doubleClick(max_loc)  # Launch the desktop again
            close_second = self.image_match('connect_fail', 3)
            if close_second is not None:
                self.log.error('launch desktop fail, please confirm desktop available')
                pag.hotkey('ctrl', 'alt', 'f4')
                # return 'launch desktop fail, please confirm desktop available'
                return 'desktop_unavailable'
        return True

    def del_vmware_in_task_bar(self):
        for i in range(6):
            max_loc = self.image_match('vmware_in_task_bar', 1)
            time.sleep(1)
            if max_loc is not None:
                pag.rightClick(max_loc)
                time.sleep(1)
                pag.press('down', presses=2, interval=0.1)
                pag.press('enter')
                time.sleep(1)
                continue
            else:
                break
