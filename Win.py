import webview


class Api:
    def __init__(self):
        pass  # 在这里可以定义 API 的方法


class Win:
    def __init__(self, win_name, win_width, win_height, win_url):
        self.win_name = win_name
        self.win_width = win_width
        self.win_height = win_height
        self.win_url = win_url
        self.api = Api()

    def start_pc_win(self):
        try:
            webview.create_window(
                self.win_name,
                url=self.win_url,
                js_api=self.api,
                width=self.win_width,
                height=self.win_height,
                resizable=False
            )
            print(f"日志：PC窗口 '{self.win_name}' 启动成功")
            # webview.start(debug=True)
            # 如果不需要调试模式，可以使用下面的代码
            webview.start()
        except Exception as e:
            print(f"错误：{e}")


# 示例用法
if __name__ == "__main__":
    win = Win("My Window", 800, 600, "https://example.com")
    win.start_pc_win()
