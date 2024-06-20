import asyncio
import threading
import websockets
import json


class Server:
    def __init__(self, port):
        self.port = port

    # 定义发送消息给客户端的函数向客户端发送消息
    async def send_message(self, websocket, path):
        message = json.dumps({"message": "Hello from the server!", "status": "成功连接"})
        await websocket.send(message)
        for i in range(10):
            await websocket.send(json.dumps({"message": str(i)}))
            print(f"已发送消息到客户端：{str(i)}")
            await asyncio.sleep(2)  # 每隔2秒发送一条消息

    # 异步函数：启动 WebSocket 服务器
    async def start_websocket_server(self):
        async with websockets.serve(self.send_message, "0.0.0.0", self.port):
            await asyncio.Future()  # 永久等待，直到服务器关闭

    # 多线程函数：在新的事件循环中运行 WebSocket 服务器
    def start_server_in_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start_websocket_server())

    def start_server(self):
        # 创建并启动线程
        thread = threading.Thread(target=self.start_server_in_thread)
        thread.daemon = True
        thread.start()
        print("log：Server启动成功")


# 示例用法
if __name__ == "__main__":
    server = Server(8765)
    server.start_server()
    # 保持主线程运行
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("log：Server已关闭")
