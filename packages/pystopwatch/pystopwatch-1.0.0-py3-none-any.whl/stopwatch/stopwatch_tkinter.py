# -*- coding:utf-8 -*-

"""GUI StopWatch

表示形式
デフォルト: 00:00:00.000
単位：h:m:s.ms
ボタン：スタート、ラップ、クリア、（ストップ）
スタートを押すと、スタートボタンがストップボタンに変わる。
"""

import tkinter as tk 
import time


# ラベルを更新する間隔[ms]
INTERVAL = 10

# 計測開始時刻
start_time = 0

# 時間計測中フラグ
start_flag = False

stop_flag = False

# afterメソッドのID
after_id = 0

stop_elapsed_time = 0

# 時間更新関数
def update_time():
    global start_time
    global app, label
    global after_id

    # update_time関数を再度INTERVAL[ms]後に実行
    after_id = app.after(INTERVAL, update_time)

    # 現在の時刻を取得
    now_time = time.time()

    # 現在の時刻と計測開始時刻の差から計測時間計算
    elapsed_time = now_time - start_time

    # s to h
    eth = int(elapsed_time / 3600)
    eth_remainder = elapsed_time % 3600
    # s to m
    etm = int(eth_remainder / 60)
    ets = eth_remainder % 60

    # 表示したい形式に変換（小数点第２位までに変換）
    elapsed_time_str = "{0:0=2}:{1:0=2}:{2:0=6.3f}".format(eth, etm, ets)

    # 計測時間を表示
    label.config(text=elapsed_time_str)


# スタートボタンの処理
def start():
    global app
    global start_flag
    global start_time
    global after_id
    global stop_flag

    # 計測中でなければ時間計測開始
    if not start_flag:
        # 計測中フラグをON
        start_flag = True

        # 計測開始時刻を取得
        if stop_flag:
            start_time = time.time() - stop_elapsed_time
            stop_flag = False
        else:
            start_time = time.time()

        # update_timeをINTERVAL[ms] 後に実行
        after_id = app.after(INTERVAL, update_time)


# ストップボタンの処理
def stop():
    global start_flag
    global after_id
    global stop_flag
    global stop_elapsed_time

    # 計測中の場合は計測処理を停止
    if start_flag:

        # update_time関数の呼び出しをキャンセル
        app.after_cancel(after_id)

        # 計測中フラグをオフ
        start_flag = False

        now_time = time.time()
        stop_elapsed_time = now_time - start_time
        stop_flag = True

def clear():
    global start_flag
    global stop_flag
    global start_time
    global stop_elapsed_time

    if not stop_flag:
        stop()

    start_flag = False
    stop_flag = False
    start_time = 0
    stop_elapsed_time = 0
    label.config(text="00:00:00.000")

# メインウィンドウ作成
app = tk.Tk()
app.title("stop watch")
app.geometry("420x300")

# 時間計測結果表示ラベル
label = tk.Label(
    app,
    text="00:00:00.000",
    width=10,
    font=("", 50, "bold"),
)
label.grid(row=0, column=0, columnspan=3)

# ストップウォッチのスタートボタン
start_button = tk.Button(app, text="START", font=("", 25, "bold"), command=start)
start_button.grid(row=1, column=0)

# ストップウォッチのストップボタン
stop_button = tk.Button(app, text="STOP", font=("", 25, "bold"), command=stop)
stop_button.grid(row=1, column=1)

# ストップウォッチのクリアボタン
stop_button = tk.Button(app, text="CLEAR", font=("", 25, "bold"), command=clear)
stop_button.grid(row=1, column=2)

# メインループ
app.mainloop()
