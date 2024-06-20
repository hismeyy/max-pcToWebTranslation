import webview


class Api:
    def __init__(self):
        pass  # 这里可以定义API的方法


class Win:
    def __init__(self, win_name, win_width, win_height, win_url):
        self.win_name = win_name
        self.win_width = win_width
        self.win_height = win_height
        self.win_url = win_url
        self.api = Api()

    def start_pc_win(self):
        try:
            win = webview.create_window(
                self.win_name,
                url=self.win_url,
                js_api=self.api,
                width=self.win_width,
                height=self.win_height
            )
            print("log:PC窗口启动成功")
            webview.start(debug=True)
            # webview.start()
        except Exception as e:
            print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    win = Win("My Window", 800, 600, "https://example.com")
    win.start_pc_win()
