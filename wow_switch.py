import pyautogui
import time
import random
import win32gui


def handler(hwnd, windows):
    windows.append((hwnd, win32gui.GetWindowText(hwnd)))


all_windows = []
wow_windows = []
win32gui.EnumWindows(handler, all_windows)
for i in all_windows:
    if "魔兽世界" in i[1]:
        wow_windows.append(i[0])


def switch_to_window(hwnd):
    win32gui.ShowWindow(hwnd, 5)  # SW_SHOW
    win32gui.SetForegroundWindow(hwnd)


def logout_login():
    pyautogui.press('esc')
    time.sleep(5)
    pyautogui.click(960, 618)
    time.sleep(30)
    pyautogui.click(960, 988)
    time.sleep(30)


moves = [('w',), ('a',), ('s',), ('d',),
         ('w', 'a'), ('w', 'd'), ('s', 'a'), ('s', 'd')]


def random_move():
    for i in range(random.randint(5, 8)):
        pyautogui.hotkey(*random.choice(moves),
                         interval=(0.2 + random.random() * 0.5))


time.sleep(10)
while True:
    for i in wow_windows:
        switch_to_window(i)
        time.sleep(5)
        # random_move()
        logout_login()
    time.sleep(300 + random.randint(100, 200))
