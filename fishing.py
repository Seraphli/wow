import mss
import mss.tools
import time
import cv2
import numpy as np
import pyautogui
import os
from send_email_script import send_mail, mailto_list

COUNT = 1000000


class Detector(object):
    def __init__(self):
        self.template = cv2.imread('buoy_label.png')
        self.click_list = self.read_list('./fishing/click_list')
        self.black_list = self.read_list('./fishing/black_list')
        self.method = cv2.TM_SQDIFF_NORMED
        self.sct = mss.mss()
        self.fish_region = (880, 300, 150, 150)
        self.label_region = {"left": 1739, "top": 919,
                             "width": 50, "height": 31}
        self.label_co = 0.9
        self.change_co = 1
        self.loc = None
        self.buoy_region = None
        self.buoy_template = None

    def reset_mss(self):
        self.sct.close()
        time.sleep(5)
        self.sct = mss.mss()

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

    def match_image(self, fn, img, template):
        res = cv2.matchTemplate(img, template, self.method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # print(fn, min_val, max_val)
        if min_val < 0.08:
            return True, min_loc
        return False, None

    def wrap_up(self):
        screen = np.array(self.sct.grab(self.sct.monitors[1]),
                          dtype=np.uint8)[:, :, :3]
        for fn, img in self.click_list:
            res = self.match_image(fn, screen, img)
            if res[0]:
                pyautogui.rightClick(res[1][0] + 10, res[1][1] + 10)
                time.sleep(1)

        for fn, img in self.black_list:
            res = self.match_image(fn, screen, img)
            if res[0]:
                pyautogui.leftClick(res[1][0] + 10, res[1][1] + 10)
                time.sleep(0.2)
                pyautogui.leftClick(1920 // 2, 1080 // 2 + 50)
                time.sleep(0.2)
                pyautogui.leftClick(877, 233)
                time.sleep(0.2)

    def close(self):
        self.sct.close()


def fishing():
    flag = False
    pyautogui.moveTo(1920 // 2, 1080 // 2 + 50)
    time.sleep(0.5)
    # 扔鱼竿
    pyautogui.hotkey('ctrl', '=')
    time.sleep(1)
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
        time.sleep(0.02)
    detector.change_co = max(threshold) + np.std(threshold)
    # 等鱼上钩
    st = time.time()
    while time.time() - st < 25:
        if detector.detect_buoy_change():
            pyautogui.rightClick(*loc)
            flag = True
            break
        else:
            time.sleep(0.02)
    time.sleep(2)
    detector.wrap_up()
    return flag


def logout_login():
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(5)
    pyautogui.click(960, 618)
    time.sleep(30)
    pyautogui.click(960, 988)
    time.sleep(30)
    pyautogui.press('b')
    time.sleep(1)


detector = Detector()
time.sleep(5)
c = 0
failed = 0
pyautogui.press('b')
time.sleep(1)
while c < COUNT:
    if fishing():
        c += 1
        failed = 0
    else:
        failed += 1
        if failed == 5:
            send_mail(mailto_list, "Fishing", "Failed 5 times!")
    if c % 50 == 0:
        detector.reset_mss()

detector.close()
