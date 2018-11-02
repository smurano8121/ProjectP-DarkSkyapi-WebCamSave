# coding: utf-8
# APIReqに使用
import requests
import json
# webカメラの映像取得に使用
import cv2
import numpy as np
import sys
# 動画撮影時間管理のために使用
import time
from datetime import datetime

# 定数定義
ESC_KEY = 27     # Escキー
INTERVAL= 33     # 待ち時間
FRAME_RATE = 6  # fps
size = (3840, 2160)
ORG_WINDOW_NAME = "MP4（H.264）"
ORG_FILE_NAME = "weather"
Codec = ".mp4"
fmt = cv2.VideoWriter_fourcc(*'H264')
Pass = "stockvideo/"
exitjudge = 0
nowTime = 0

# darkskyapiから天気情報を取得
def darkskyapi_Request():
    # GETパラメータはparams引数に辞書で指定する
    headers = {"content-type": "application/json"}
    url = 'https://api.darksky.net/forecast/579137f0816593c1d256911bc1c62f0f/34.8031949,135.7787311'
    response = requests.get(url,headers=headers)
    data = response.json()
    weather = data["currently"]["icon"]
    return weather

# webカメラの動画を撮影
def Webcam(get_weather):
    # 現在の時刻管理
    now = datetime.now()

    ORG_FILE_NAME = Pass + str(now.hour) + str(now.minute) + get_weather + Codec
    cap = cv2.VideoCapture(0)

    # 保存ビデオファイルの準備
    rec = cv2.VideoWriter(ORG_FILE_NAME, fmt, FRAME_RATE, size)

    # webカメラが認識されているか判断
    if cap.isOpened() is False:
        print ("can not open camera")
        sys.exit()

    # webカメラの映像を保存し続ける
    while True:
        # 現在の時刻管理
        now = datetime.now()

        end_flag, c_frame = cap.read()
        c_frame = cv2.resize(c_frame, size)
        cv2.namedWindow(ORG_WINDOW_NAME)
        cv2.imshow(ORG_WINDOW_NAME, c_frame)
        # 保存
        rec.write(c_frame)
        if end_flag is False:
            exitjudge = 0
            break
        if cv2.waitKey(1) == ESC_KEY:
            exitjudge = 1
            break
        if now.minute % 2 == 0 and now.second == 0:
            exitjudge = 0
            break

    # 保存
    cap.release()
    rec.release()
    cv2.destroyAllWindows()
    return exitjudge # Escキー入力でプログラムが終了する


num = 0
while(num < 1):
    response_weather = darkskyapi_Request()
    get_exitjudge = Webcam(response_weather)

    #Escキー入力でプログラムが終了する
    if get_exitjudge == 1:
        break
