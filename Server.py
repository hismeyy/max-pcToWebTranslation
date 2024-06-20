import asyncio
import json
import logging
import threading

import websockets

logging.basicConfig(level=logging.INFO)


class Server:
    def __init__(self, port):
        self.port = port

    async def send_message(self, websocket, path):
        initial_message = {"message": "Hello from the server!", "status": "成功连接"}
        await websocket.send(json.dumps(initial_message))
        for i in range(10):
            await websocket.send(json.dumps({"message": str(i)}))
            logging.info(f"已发送消息到客户端：{i}")
            await asyncio.sleep(2)  # 每隔2秒发送一条消息

    async def start_websocket_server(self):
        async with websockets.serve(self.send_message, "0.0.0.0", self.port):
            logging.info(f"Server 正在端口 {self.port} 上运行")
            await asyncio.Future()  # 永久等待，直到服务器关闭

    def start_server_in_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start_websocket_server())

    def start_server(self):
        thread = threading.Thread(target=self.start_server_in_thread)
        thread.daemon = True
        thread.start()
        logging.info("Server 启动成功")


if __name__ == "__main__":
    server = Server(8765)
    server.start_server()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("Server 已关闭")
