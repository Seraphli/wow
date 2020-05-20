import pyautogui
import time
import pyperclip

# TARGET = ['血瓣花猛击者', '血瓣花鞭笞者', '翼手龙', '胶质软泥怪', '幼双帆龙', '双帆龙']
# TARGET = ['沙漠鞭尾蝎', '沙漠疾行蝎', '晶鳞蜥蜴', '晶鳞凝视者', '疱爪土狼', '火鹏', ]
# TARGET = ['森提帕尔异种蝎', '森提帕尔群居蝎', '森提帕尔沙行者', '森提帕尔毒刺蝎']
# TARGET = ['焦油兽王', '焦油潜伏者', ]
# TARGET = ['地缚图腾', '冬泉探路者', '冬泉图腾师', '冬泉巢穴守卫']
# TARGET = ['冬泉鸣枭', '冬泉巨枭', '碎齿暴熊', '老碎齿熊', '冰风破坏者', '冰风奇美拉', '月光枭兽', '狂暴枭兽',
#           '疯狂的枭兽', '痛苦的上层精灵', '受难的上层精灵']
TARGET = ['痛苦的上层精灵', '受难的上层精灵']

# TARGET = ['老双帆龙',  '狂怒的翼手龙', '粘稠的软泥怪', '血瓣花捕兽者']


class RANGE(object):
    R0005 = 0
    R0520 = 1
    R2030 = 2
    R3035 = 3
    ROOR = 4


class FarmBot(object):
    def __init__(self):
        self.cur_tar = None
        self.count = 0

    def input_macro(self, macro):
        pyautogui.press('enter')
        pyperclip.copy(macro)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

    def clear_tar(self):
        self.input_macro('/cleartarget [dead][noharm]')

    def target(self, idx):
        self.input_macro(f'/target {TARGET[idx]}')
        time.sleep(0.2)
        self.clear_tar()
        return self.check_tar()

    def check_tar(self):
        if pyautogui.pixelMatchesColor(1315, 653, (0, 0, 0), 3):
            if pyautogui.pixelMatchesColor(1162, 620, (131, 134, 143), 3):
                self.clear_tar()
                return False
            if pyautogui.pixelMatchesColor(1162, 620, (79, 155, 81), 3):
                self.clear_tar()
                return False
            return True
        return False

    def check_pet_tar(self):
        if pyautogui.pixelMatchesColor(1315, 861, (0, 0, 0), 3):
            return True
        return False

    def check_autoshot(self):
        if pyautogui.pixelMatchesColor(950, 956, (102, 100, 101), 3):
            return True
        return False

    def check_in_fight(self):
        if pyautogui.pixelMatchesColor(1200, 960, (125, 107, 39), 3):
            return True
        return False

    def select_pet_tar(self):
        pyautogui.leftClick(1315, 861)

    def check_range(self):
        if pyautogui.pixelMatchesColor(960, 645, (236, 236, 236), 3):
            return RANGE.R0005
        if pyautogui.pixelMatchesColor(960, 645, (26, 230, 219), 3):
            return RANGE.R0520
        if pyautogui.pixelMatchesColor(960, 645, (19, 229, 0), 3):
            return RANGE.R2030
        if pyautogui.pixelMatchesColor(960, 645, (255, 219, 0), 3):
            return RANGE.R3035
        return RANGE.ROOR

    def check_attack_dis(self):
        _range = self.check_range()
        if pyautogui.pixelMatchesColor(939, 970, (194, 39, 37), 3):
            if _range is RANGE.ROOR:
                return 'far'
            if _range == RANGE.R0005 or _range == RANGE.R0520:
                return 'near'
        return 'good'

    def search_tar(self):
        tar_range = []
        for i in range(len(TARGET)):
            if self.target(i):
                tar_range.append((i, self.check_range()))
                self.input_macro('/cleartarget')
        if not tar_range:
            return False
        tar_range = sorted(tar_range, key=lambda x: x[1])
        self.target(tar_range[0][0])
        return True

    def adjust_dis(self, max_try=10000):
        try_c = 0
        while self.check_tar():
            try_c += 1
            if try_c > max_try:
                self.input_macro('/cleartarget')
                return False
            if self.check_attack_dis() == 'far':
                pyautogui.press('f6', interval=0.2)
                if try_c % 10 == 4:
                    pyautogui.keyDown('space')
                    pyautogui.keyDown('a')
                    time.sleep(1)
                    pyautogui.keyUp('a')
                    pyautogui.keyUp('space')
                elif try_c % 10 == 8:
                    pyautogui.keyDown('space')
                    pyautogui.keyDown('d')
                    time.sleep(1)
                    pyautogui.keyUp('d')
                    pyautogui.keyUp('space')
                pyautogui.press('f6', interval=0.2)
            elif self.check_attack_dis() == 'near':
                pyautogui.press('c')
                pyautogui.keyDown('s')
                pyautogui.keyDown('a')
                time.sleep(1)
                pyautogui.keyUp('a')
                pyautogui.keyUp('s')
            else:
                break
            time.sleep(0.5)

        return True

    def approach_tar(self):
        if self.check_in_fight():
            self.adjust_dis()
        else:
            if not self.adjust_dis(30):
                pyautogui.keyDown('s')
                time.sleep(6)
                pyautogui.keyUp('s')
                pyautogui.keyDown('left')
                time.sleep(0.2)
                pyautogui.keyUp('left')
                pyautogui.keyDown('s')
                time.sleep(6)
                pyautogui.keyUp('s')
                pyautogui.keyDown('right')
                time.sleep(0.2)
                pyautogui.keyUp('right')
                return False
        pyautogui.press('3')
        pyautogui.press('f6', interval=0.2)
        time.sleep(4)
        return True

    def attack(self):
        while not self.check_in_fight():
            time.sleep(1)
        self.input_macro('/petfollow')
        time.sleep(4)
        if self.count % 2 == 0:
            if not self.check_tar():
                return
            pyautogui.press('q')
            pyautogui.press('f6', interval=0.2)
            time.sleep(1.5)
        else:
            if not self.check_tar():
                return
            pyautogui.hotkey('shift', 'q')
            pyautogui.press('f6', interval=0.2)
            time.sleep(1.5)
        self.count += 1
        if not self.check_tar():
            return
        pyautogui.press('f6', interval=0.2)
        pyautogui.press('3')
        time.sleep(4)
        c = 0
        while self.check_tar():
            self.adjust_dis()
            if not self.check_autoshot():
                pyautogui.press('t', interval=0.2)
            if not self.check_autoshot():
                pyautogui.keyDown('left')
                time.sleep(0.2)
                pyautogui.keyUp('left')
                pyautogui.press('t', interval=0.2)
            pyautogui.press('f6', interval=0.2)
            pyautogui.press('3')
            time.sleep(6)
            if not self.check_autoshot():
                pyautogui.press('t', interval=0.2)
            c += 1
            if c > 10:
                break

    def collect(self):
        self.input_macro('/targetlasttarget')
        pyautogui.press('f6', interval=0.2)
        c = 0
        while self.check_tar() and c < 10:
            time.sleep(0.5)
            c += 1
        self.input_macro('/targetlasttarget')
        pyautogui.press('f6', interval=0.2)
        time.sleep(2)
        # pyautogui.rightClick(1920 / 2, 1080 / 2 + 50)
        # time.sleep(6)
        # pyautogui.rightClick(1920 / 2, 1080 / 2 + 50)
        # time.sleep(6)
        # self.clear_tar()
        self.clear_tar()

    def fallback(self):
        pyautogui.rightClick(1920 / 2, 1080 / 2 + 300)
        time.sleep(1)
        pyautogui.keyDown('w')
        time.sleep(2)
        pyautogui.keyUp('w')
        pyautogui.rightClick(1920 / 2, 1080 / 2 + 100)
        time.sleep(0.2)


def farm():
    pyautogui.FAILSAFE = True
    # pyautogui.PAUSE = 0.1
    bot = FarmBot()
    while True:
        if bot.check_pet_tar():
            bot.select_pet_tar()
        if not bot.check_tar():
            if not bot.search_tar():
                time.sleep(10)
        else:
            if bot.approach_tar():
                pyautogui.keyDown('space')
                time.sleep(0.5)
                pyautogui.keyUp('space')
                bot.attack()
                time.sleep(2)
                bot.collect()
                pyautogui.keyDown('space')
                time.sleep(0.5)
                pyautogui.keyUp('space')
                if bot.check_tar():
                    continue
                if bot.check_pet_tar():
                    bot.select_pet_tar()
                    continue
                # bot.fallback()
                time.sleep(6)


if __name__ == '__main__':
    time.sleep(5)
    farm()
