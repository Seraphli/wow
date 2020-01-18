import mss
import mss.tools
import time
import cv2
import numpy as np
import pyautogui
import os
import win32gui
from send_email_script import send_mail, mailto_list

COUNT = 100000


class Detector(object):
    def __init__(self):
        self.template = cv2.imread('./fishing/buoy_label.png')
        self.backpack = cv2.imread('./fishing/backpack.png')
        self.click_list = self.read_list('./fishing/click_list')
        self.black_list = self.read_list('./fishing/black_list')
        self.error_list = self.read_list('./fishing/error_list')
        self.warn_list = self.read_list('./fishing/warn_list')
        self.method = cv2.TM_SQDIFF_NORMED
        self.sct = mss.mss()
        self.sct.__enter__()
        self.fish_region = (870, 300, 150, 150)
        self.label_region = {"left": 1739, "top": 919,
                             "width": 50, "height": 31}
        self.label_co = 0.75
        self.change_co = 1
        self.loc = None
        self.buoy_region = None
        self.buoy_template = None

    def reset_mss(self):
        self.sct.__exit__()
        time.sleep(5)
        self.sct = mss.mss()
        self.sct.__enter__()

    @staticmethod
    def read_list(path):
        image_list = []
        for fn in os.listdir(path):
            img = cv2.imread(os.path.join(path, fn))
            image_list.append((fn, img))
        return image_list

    def detect_label(self):
        img = np.array(self.sct.grab(self.label_region),
                       dtype=np.uint8)[:, :, :3]
        res = cv2.matchTemplate(img, self.template, self.method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # print(min_val, max_val)
        if min_val < 1 - self.label_co:
            return True
        return False

    def detect_buoy(self):
        for j in range(0, self.fish_region[3] + 1, 30):
            for i in range(0, self.fish_region[2] + 1, 30):
                x, y = i + self.fish_region[0], j + self.fish_region[1]
                pyautogui.moveTo(x, y)
                if self.detect_label():
                    self.loc = x, y
                    self.j = j // 30
                    pyautogui.moveTo(*self.loc)
                    self.buoy_region = {
                        "left": self.loc[0] - 20,
                        "top": self.loc[1] - 30,
                        "width": 50 - (self.fish_region[3] // 30 - self.j) * 2,
                        "height": 60 - (self.fish_region[3] // 30 - self.j) * 2
                    }
                    return self.loc
                else:
                    time.sleep(0.01)
        return None

    def save_buoy(self):
        img = np.array(self.sct.grab(self.buoy_region),
                       dtype=np.uint8)[:, :, :3]
        self.buoy_template = img

    def sample_threshold(self):
        img = np.array(self.sct.grab(self.buoy_region),
                       dtype=np.uint8)[:, :, :3]
        res = cv2.matchTemplate(img, self.buoy_template, self.method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return min_val

    def detect_buoy_change(self):
        img = np.array(self.sct.grab(self.buoy_region),
                       dtype=np.uint8)[:, :, :3]
        res = cv2.matchTemplate(img, self.buoy_template, self.method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # print(min_val)
        if min_val > self.change_co:
            return True
        return False

    def match_image(self, fn, _img, template, threshold=0.06):
        res = cv2.matchTemplate(_img, template, self.method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # print(fn, min_val, max_val)
        if min_val < threshold:
            return True, min_loc
        return False, None

    def pre_wrap_up(self):
        screen = np.array(self.sct.grab(self.sct.monitors[1]),
                          dtype=np.uint8)[:, :, :3]
        for fn, img in self.click_list:
            res = self.match_image(fn, screen, img)
            if res[0]:
                time.sleep(0.5)
                pyautogui.rightClick(res[1][0] + 10, res[1][1] + 10)

    def wrap_up(self):
        screen = np.array(self.sct.grab(self.sct.monitors[1]),
                          dtype=np.uint8)[:, :, :3]

        for fn, img in self.black_list:
            res = self.match_image(fn, screen, img)
            if res[0]:
                pyautogui.leftClick(res[1][0] + 10, res[1][1] + 10)
                time.sleep(0.2)
                pyautogui.leftClick(1920 // 2, 1080 // 2 + 50)
                time.sleep(0.2)
                pyautogui.leftClick(877, 233)
                time.sleep(0.2)

    def detect_gm(self):
        screen = np.array(self.sct.grab(self.sct.monitors[1]),
                          dtype=np.uint8)[:, :, :3]
        for fn, img in self.warn_list:
            res = self.match_image(fn, screen, img, threshold=0.1)
            if res[0]:
                send_mail(mailto_list, "Fishing", "GM Warning!")

    def detect_error(self):
        screen = np.array(self.sct.grab(self.sct.monitors[1]),
                          dtype=np.uint8)[:, :, :3]
        for fn, img in self.error_list:
            res = self.match_image(fn, screen, img)
            if res[0]:
                pyautogui.leftClick(res[1][0] + 10, res[1][1] + 10)
                time.sleep(1)
                pyautogui.leftClick(1805, 1010)
                time.sleep(15)
                break

        time.sleep(30)

        def handler(hwnd, windows):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        def switch_to_window(hwnd):
            win32gui.ShowWindow(hwnd, 5)  # SW_SHOW
            win32gui.SetForegroundWindow(hwnd)

        try:
            all_windows = []
            bn_windows = None
            win32gui.EnumWindows(handler, all_windows)
            for i in all_windows:
                if "暴雪战网" in i[1]:
                    bn_windows = i[0]

            switch_to_window(bn_windows)
        except:
            pass

        screen = np.array(self.sct.grab(self.sct.monitors[1]),
                          dtype=np.uint8)[:, :, :3]
        for fn, img in self.error_list:
            if fn == 'enter.png':
                res = self.match_image(fn, screen, img)
                if res[0]:
                    pyautogui.leftClick(res[1][0] + 10, res[1][1] + 10)
                    time.sleep(20)
                    pyautogui.click(960, 988)
                    time.sleep(30)

        return True

    def detect_backpack(self):
        screen = np.array(self.sct.grab(self.sct.monitors[1]),
                          dtype=np.uint8)[:, :, :3]
        res = cv2.matchTemplate(screen, self.backpack, self.method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if min_val > 0.04:
            pyautogui.press('b')
            time.sleep(1)

    def close(self):
        self.sct.__exit__()


def fishing():
    flag = False
    pyautogui.moveTo(1920 // 2, 1080 // 2 + 50)
    time.sleep(0.5)
    # 扔鱼竿
    pyautogui.hotkey('ctrl', '=')
    time.sleep(1.4)
    # 找浮标
    loc = detector.detect_buoy()
    if loc is None:
        return flag
    detector.save_buoy()
    # 检测鱼鳔处变化趋势
    threshold = []
    st = time.time()
    while time.time() - st < 2:
        threshold.append(detector.sample_threshold())
    detector.change_co = np.mean(threshold) + np.std(threshold) * 3
    # 等鱼上钩
    st = time.time()
    while time.time() - st < 23:
        if detector.detect_buoy_change():
            pyautogui.rightClick(*loc)
            flag = True
            break
        else:
            time.sleep(0.05)
    return flag


pyautogui.FAILSAFE = False
detector = Detector()
time.sleep(5)
c = 0
failed = 0
detector.detect_backpack()
while c < COUNT:
    res = fishing()
    if res:
        c += 1
        failed = 0
    else:
        failed += 1
        if failed > 2:
            if detector.detect_error():
                pyautogui.press('0')
                detector.detect_backpack()
        if failed == 5:
            print('Failed 5 times!')
            send_mail(mailto_list, "Fishing", "Failed 5 times!")

    detector.pre_wrap_up()
    if c % 20 == 0:
        time.sleep(2)
        detector.wrap_up()

    if c % 5 == 0:
        detector.detect_gm()

detector.close()
