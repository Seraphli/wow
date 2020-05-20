import pyautogui
import time

pyautogui.FAILSAFE = True
time.sleep(10)
while True:
    pyautogui.rightClick()
    time.sleep(0.2)
