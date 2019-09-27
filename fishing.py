import mss
import mss.tools
import time
import cv2
import numpy as np
import pyautogui

COUNT = 1000000


class Detector(object):
    def __init__(self):
        self.template = cv2.imread('buoy_label.png')
        self.method = cv2.TM_SQDIFF_NORMED
        self.sct = mss.mss()
        self.fish_region = (880, 300, 150, 150)
        self.label_region = {"left": 1789, "top": 914,
                             "width": 60, "height": 40}
        self.label_co = 0.9
        self.change_co = 0.96
        self.loc = None
        self.buoy_region = None
        self.buoy_template = None

    def detect_label(self):
        img = np.array(self.sct.grab(self.label_region),
                       dtype=np.uint8)[:, :, :3]
        res = cv2.matchTemplate(img, self.template, self.method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
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
                    pyautogui.moveTo(*self.loc)
                    self.buoy_region = {"left": self.loc[0] - 20,
                                        "top": self.loc[1] - 40,
                                        "width": 60, "height": 80}
                    return self.loc
        return None

    def save_buoy(self):
        img = np.array(self.sct.grab(self.buoy_region),
                       dtype=np.uint8)[:, :, :3]
        self.buoy_template = img

    def detect_buoy_change(self):
        img = np.array(self.sct.grab(self.buoy_region),
                       dtype=np.uint8)[:, :, :3]
        res = cv2.matchTemplate(img, self.buoy_template, self.method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # print(min_val)
        if min_val > 1 - self.change_co:
            return True
        return False

    def close(self):
        self.sct.close()


def fishing():
    flag = False
    pyautogui.moveTo(1920 // 2, 1080 // 2 + 50)
    time.sleep(2)
    # 扔鱼竿
    pyautogui.hotkey('alt', '0')
    time.sleep(1)
    # 找浮标
    loc = detector.detect_buoy()
    if loc is None:
        return flag
    detector.save_buoy()
    # 等鱼上钩
    st = time.time()
    while time.time() - st < 25:
        if detector.detect_buoy_change():
            pyautogui.rightClick(*loc)
            flag = True

            break
        else:
            time.sleep(0.02)
    return flag


detector = Detector()
time.sleep(5)
c = 0
while c < COUNT:
    if fishing():
        c += 1
    time.sleep(2)

detector.close()
