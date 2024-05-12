import numpy as np
import cv2
import serial
import time
import pyautogui

# 将128*64的二值化图像转换为OLED数组格式
def img2array(frame):

    array = np.zeros((8, 128), dtype='uint8')

    for j in range(64):
        for i in range(128):
            if frame[j][i] > 0:
                array[j // 8][i] = (array[j // 8][i]) | (0x01 << (j % 8))
    return array

# 打开串口
serial_port = serial.Serial('COM3', 921600)

# 设置预览窗口
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 128 * 4, 64 * 4)

# 记住开始时间
start_time = time.time()

while True:
    # 获取当前屏幕截图
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)

    # 帧图像处理
    img = cv2.resize(img, (128, 64))                         # 修改尺寸
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)              # 灰度化
    img = cv2.threshold(img, 170, 255, cv2.THRESH_BINARY)[1] # 二值化

    # 预览图像
    cv2.imshow('img', img)

    # 转换为数组并使用串口发送
    img_array = img2array(img)
    serial_port.write(img_array.tobytes())

    # 等待按键，按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cv2.destroyAllWindows()
serial_port.close()
