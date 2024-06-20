import threading

from flask import Flask, render_template
from flask_cors import CORS
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


class Web:
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__, template_folder='templates')
        self.sockets = Sockets(self.app)
        CORS(self.app)
        self.server = None
        self.server_thread = None
        self.define_routes()

    def define_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.sockets.route('/echo')
        def echo_socket(ws):
            while not ws.closed:
                message = ws.receive()
                if message:
                    print(f"从服务器接收到的消息：{message}")
                    ws.send(f"服务器响应：{message}")

    def run_server(self):
        self.server = pywsgi.WSGIServer(('0.0.0.0', self.port), self.app, handler_class=WebSocketHandler)
        try:
            print(f"Starting server on port {self.port}")  # 调试输出
            self.server.serve_forever()
        except Exception as e:
            print(f"Error occurred: {e}")

    def start_server(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True  # 确保线程在主程序退出时能够自动结束
        self.server_thread.start()
        print("log：web启动成功")

    def stop_server(self):
        if self.server:
            self.server.stop()
        if self.server_thread:
            self.server_thread.join()
            print("log：web停止成功")


# 测试用例
if __name__ == "__main__":
    web = Web(port=5000)
    web.start_server()
    input("Press Enter to stop the server...\n")  # Keep the server running
    web.stop_server()
