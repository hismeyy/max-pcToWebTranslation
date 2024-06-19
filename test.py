import keyboard
import pyperclip
import time

# 初始化全局变量以记录按键时间
last_time = 0


def on_ctrl_c():
    global last_time
    current_time = time.time()

    # 检查两次Ctrl+C之间的时间间隔是否足够短
    if current_time - last_time < 0.5:  # 0.5秒内两次Ctrl+C
        clipboard_content = pyperclip.paste()
        print(f"剪切板内容: {clipboard_content}")

    # 更新上一次按键时间
    last_time = current_time


# 监听Ctrl+C组合键
keyboard.add_hotkey('ctrl+c', on_ctrl_c)

# 保持程序运行
keyboard.wait('esc')  # 按下Esc键退出程序
