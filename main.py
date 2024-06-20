import asyncio
import os
import threading

import websockets
from flask import Flask, render_template
from flask_cors import CORS
from flask_sockets import Sockets

import Win

app = Flask(__name__)
server = None
sockets = Sockets(app)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


# WebSocket 处理程序，用于接收消息
@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        print(f"从服务器接收到的消息：{message}")


def run_server():
    global server
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    print("服务启动成功")
    server.serve_forever()


# 启动服务器的函数
def start_server():
    server_thread = threading.Thread(target=run_server)
    server_thread.start()


# 停止服务器的函数
def stop_server():
    global server
    server.stop()


# 定义发送消息给客户端的函数
# 异步函数：向客户端发送消息
async def send_message(websocket, path):
    message = "Hello from the server!", "成功连接"
    await websocket.send(message)
    for i in range(10):
        await websocket.send(str(i))
        print(f"已发送消息到客户端：{str(i)}")
        await asyncio.sleep(2)  # 每隔1秒发送一条消息


# 异步函数：启动 WebSocket 服务器
async def start_websocket_server():
    print("WebSocket 服务器启动成功...")
    async with websockets.serve(send_message, "0.0.0.0", 8765):
        await asyncio.Future()  # 永久等待，直到服务器关闭


# 多线程函数：在新的事件循环中运行 WebSocket 服务器
def start_server_in_thread():
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.run(start_websocket_server())


if __name__ == '__main__':
    # 创建并启动线程
    thread = threading.Thread(target=start_server_in_thread)
    thread.start()

    # 创建并启动 Flask 线程
    start_server()

    # 主线程创建桌面窗口
    # 构建HTML文件的路径
    html_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page/index.html')
    url = 'file://' + html_file_path

    win = Win("翻译", 900, 600, url)
    win.start_pc_win()

    stop_server()
