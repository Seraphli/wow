import pyautogui
import time


def craft_loop():
    try:
        x, y = pyautogui.locateCenterOnScreen('craft.png', confidence=0.9)
    except:
        return 0
    pyautogui.click(x, y)
    time.sleep(32)
    try:
        x, y = pyautogui.locateCenterOnScreen('mask.png', confidence=0.9)
    except:
        pass
    try:
        x, y = pyautogui.locateCenterOnScreen('mask.png', confidence=0.9)
    except:
        return 0
    pyautogui.press('J')
    pyautogui.click(x, y)
    time.sleep(5)
    return 1


def main():
    time.sleep(5)
    pyautogui.PAUSE = 0.2
    while craft_loop():
        time.sleep(0.5)


if __name__ == '__main__':
    main()
