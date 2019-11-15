import pyautogui
import cv2
import os
import time
import ftplib


class RDPUtil:
    def __init__(self):
        pass

    def get_ftp(self, server, username, passwd):
        ftp = ftplib.FTP(server)
        ftp.login(username, passwd)
        return ftp

    def upload_ftp(self, ftp, filename):
        # ftp = self.get_ftp(server='1', username='2', passwd='3')
        ftp.storbinary('STOR {}'.format(filename), open(filename, 'rb'), 1024)

    def download_ftp(self, ftp, filename):
        # ftp = self.get_ftp(server='1', username='2', passwd='3')
        ftp.retrbinary('RETR {}'.format(filename), open(filename, 'wb').write, 1024)

    def get_screen_size(self):
        # return (width, height) of screen
        size = pyautogui.size()
        return (size[0], size[1])

    def get_icon_by_pic(self, name, offset=(0, 0)):
        """
        :param name: specific picture path
        :return: posision rect on screen
        file_name = address_test_5_5
        """
        if offset == (0, 0):
            full_name = name.split(".")[0]
            file_name = os.path.split(full_name)[1]
            off_x = int(file_name.split('_')[-2])
            off_y = int(file_name.split('_')[-1])
            offset = (off_x, off_y)
        pyautogui.screenshot('demo.png')
        t = cv2.matchTemplate(cv2.imread(name), cv2.imread('demo.png'), cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(t)
        print(max_loc, max_val)
        if max_val > 0.9:
            x = max_loc[0] + offset[0]
            y = max_loc[1] + offset[1]
            return (x, y)
        else:
            return None

    def wait_element(self, names, offset=(0, 0), wait_time=5):
        # names is a list, which contains many pictures, if one don't match, will find another one
        for i in range(wait_time):
            for name in names:
                if self.get_icon_by_pic(name, offset) is None:
                    time.sleep(1)
                    continue
                else:
                    return self.get_icon_by_pic(name, offset)
        # ----------should return Exception --------------
        print("Picture {} do not found in this screen".format(name))

    def rect_offset(self, rect, offset):
        if isinstance(offset, tuple):
            return (rect[0]+offset[0], rect[1]+offset[1])
        # elif isinstance(offset, str):



KEY_NAMES = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
             ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
             'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
             'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
             'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
             'browserback', 'browserfavorites', 'browserforward', 'browserhome',
             'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
             'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
             'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
             'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
             'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
             'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
             'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
             'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
             'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
             'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
             'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
             'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
             'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
             'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
             'command', 'option', 'optionleft', 'optionright']

