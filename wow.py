import pyautogui
import time
from datetime import datetime
import random

# 做水和面包数量
nums = [0, 0, 2, 6]


def action(count):
    pyautogui.keyDown('w')
    time.sleep(1)
    pyautogui.keyUp('w')
    pyautogui.keyDown('w')
    time.sleep(1)
    pyautogui.keyUp('w')
    time.sleep(random.randint(1, 3))
    # 上Buff
    if random.random() < 0.5:
        pyautogui.hotkey('ctrl', '1')
        time.sleep(5)
    if random.random() < 0.5:
        pyautogui.hotkey('ctrl', '2')
        time.sleep(5)
    if random.random() < 0.5:
        pyautogui.hotkey('ctrl', '3')
        time.sleep(5)
    if random.random() < 0.5:
        # 做面包吃面包
        if nums[0] > 0:
            pyautogui.hotkey('ctrl', '7')
            nums[0] -= 1
        else:
            pyautogui.hotkey('ctrl', '5')
            nums[0] += nums[2]
        time.sleep(5)
        pyautogui.press('space')
        time.sleep(2)
    if random.random() < 0.5:
        # 做水喝水
        if nums[1] > 0:
            pyautogui.hotkey('ctrl', '8')
            nums[1] -= 1
        else:
            pyautogui.hotkey('ctrl', '6')
            nums[1] += nums[3]
        time.sleep(5)
        pyautogui.press('space')
        time.sleep(2)

    # 回头
    pyautogui.mouseDown(button='right')
    pyautogui.move(-50, 0, duration=0.75)
    pyautogui.mouseUp(button='right')
    pyautogui.mouseDown(button='right')
    pyautogui.move(-50, 0, duration=0.75)
    pyautogui.mouseUp(button='right')


time.sleep(5)
st = datetime.now()
count = 0
while True:
    action(count)
    count += 1
    time.sleep(60)
