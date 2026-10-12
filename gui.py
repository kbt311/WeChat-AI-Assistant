import sys
from screenshot import capture_screen
from ocr import recognize_chat
from ai import analyze_chat
from PySide6.QtCore import (
    QFile,
    QIODevice,
    QTimer,
    QThread,
    Signal,
    QObject,
    Slot
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)

#发送信号
class OCRWorker(QThread):

    result_ready = Signal(list)
    error_occurred = Signal(str)

    def __init__(self, roi):
        super().__init__()
        self.roi = roi.copy()

    def run(self):
        try:
            messages = recognize_chat(self.roi)
            self.result_ready.emit(messages)

        except Exception as e:
            self.error_occurred.emit(str(e))

class AIWorker(QThread):

    result_ready = Signal(dict)
    error_occurred = Signal(str)

    def __init__(self, chat_text):
        super().__init__()
        self.chat_text = chat_text

    def run(self):
        try:
            analysis = analyze_chat(self.chat_text)

            self.result_ready.emit(analysis)

        except Exception as e:
            self.error_occurred.emit(str(e))

# 创建应用程序
app = QApplication(sys.argv)

# 加载ui文件
ui_file = QFile("main.ui")
if not ui_file.open(QIODevice.ReadOnly):
    print("打开失败")
    sys.exit(-1)

# 创建UI加载器
loader = QUiLoader()

# 加载UI文件并实例化为窗口对象
window = loader.load(ui_file)

# 关闭UI文件
ui_file.close()

#调用截图
roi = None
count = 5
timer = QTimer()


def start_capture_timer():

    global count

    count = 5

    timer.start(1000)


def count_down():

    global count

    count -= 1

    window.resultTextEdit.setText(
        f"请切换微信窗口\n{count}秒后截图"
    )

    if count == 0:
        timer.stop()
        do_capture()

timer.timeout.connect(count_down)

def capture():

    window.resultTextEdit.setText(
        "请切换微信窗口\n5秒后截图"
    )
    start_capture_timer()

def do_capture():

    global roi
    roi = capture_screen()

    if roi is not None:
        window.resultTextEdit.setText(
            "截图成功"
        )
    else:
        window.resultTextEdit.setText(
            "截图失败"
        )
# 转换文字
def format_chat(messages):

    text = ""

    for msg in messages:
        text += f'{msg["sender"]}：{msg["text"]}\n'

    return text
# 按键测试
def analyze_ocr():

    global worker

    if roi is None:
        window.resultTextEdit.setText("请先截取聊天")
        return

    window.resultTextEdit.setText(
        "正在识别聊天内容..."
    )

    worker = OCRWorker(roi)

    worker.result_ready.connect(
        receiver.show_messages
    )

    worker.error_occurred.connect(
        receiver.show_error
    )
    worker.start()
#接受信号
class OCRReceiver(QObject):

    @Slot(list)
    def show_messages(self, messages):
        chat_text = format_chat(messages)

        window.chatTextEdit.setPlainText(chat_text)

        window.resultTextEdit.setPlainText(
            "OCR识别完成，正在进行AI分析..."
        )

        # 创建AI工作线程
        self.ai_worker = AIWorker(chat_text)

        # 连接信号
        self.ai_worker.result_ready.connect(
            ai_receiver.show_analysis
        )

        self.ai_worker.error_occurred.connect(
            ai_receiver.show_error
        )

        # 启动线程
        self.ai_worker.start()

    @Slot(str)
    def show_error(self, error):
        window.resultTextEdit.setPlainText(
            f"OCR识别失败：{error}"
        )

class AIReceiver(QObject):

    @Slot(dict)
    def show_analysis(self, analysis):

        text = (
            f"情绪：{analysis['emotion']}\n"
            f"可信程度：{analysis['confidence']}\n"
            f"原因：{analysis['reason']}\n\n"
            "回复建议：\n"
        )

        for i, suggestion in enumerate(
            analysis["suggestions"], start=1
        ):
            text += f"{i}. {suggestion}\n"

        window.resultTextEdit.setPlainText(text)

    @Slot(str)
    def show_error(self, error):
        window.resultTextEdit.setPlainText(
            f"AI分析失败：{error}"
        )

receiver = OCRReceiver()
ai_receiver = AIReceiver()
window.analyzeButton.clicked.connect(analyze_ocr)
window.captureButton.clicked.connect(capture)
# 显示窗口
window.show()

# 运行应用程序
app.exec()