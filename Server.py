import asyncio
import logging
import queue
import threading
import time

import keyboard
import pyperclip
import websockets

logging.basicConfig(level=logging.INFO)


class Server:
    last_time = 0
    seed = True

    def __init__(self, port):
        self.port = port
        self.loop = None
        self.message_stack = queue.Queue()  # 使用queue.Queue代替列表

    def on_ctrl_c(self):
        current_time = time.time()

        # 检查两次Ctrl+C之间的时间间隔是否足够短
        if current_time - self.last_time < 0.5:  # 0.5秒内两次Ctrl+C
            clipboard_content = pyperclip.paste()
            self.message_stack.put(clipboard_content)  # 使用put方法将内容放入队列
            print(f"剪切板内容: {clipboard_content}")

        # 更新上一次按键时间
        self.last_time = current_time

    async def send_message(self, websocket, path):
        initial_message = "连接成功"
        await websocket.send(initial_message)
        while self.seed:
            try:
                message = self.message_stack.get_nowait()  # 使用get_nowait方法获取队列内容
                await websocket.send(message)
                logging.info(f"已发送消息到客户端：{message}")
            except queue.Empty:
                await asyncio.sleep(0.1)  # 等待一段时间再次尝试获取队列内容

    async def start_websocket_server(self):
        async with websockets.serve(self.send_message, "0.0.0.0", self.port):
            logging.info(f"Server 正在端口 {self.port} 上运行")
            await asyncio.Future()  # 永久等待，直到服务器关闭

    def start_server_in_thread(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.start_websocket_server())

    def start_server(self):
        thread = threading.Thread(target=self.start_server_in_thread)
        thread.daemon = True
        thread.start()
        logging.info("Server 启动成功")
        keyboard.add_hotkey('ctrl+c', self.on_ctrl_c)
        logging.info("开始监听按键 ctrl+c")

    def stop_server(self):
        self.seed = False
        keyboard.remove_hotkey('ctrl+c')
        logging.info("Server 停止成功")


if __name__ == "__main__":
    server = Server(8765)
    server.start_server()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("Server 已关闭")
