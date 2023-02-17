import webbrowser


class Page3(object):
    def __init__(self):
        pass

    def get_web(self):
        webbrowser.open("https://pdf.wps.cn/")


if __name__ == '__main__':
    Page3().get_web()