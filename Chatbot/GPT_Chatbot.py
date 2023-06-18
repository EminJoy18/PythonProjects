import sys
# from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtWidgets import *
from backend_chatbot import Chatbot
import threading


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Chatbot')
        self.resize(500, 500)

        self.chat_area = QTextEdit(self)
        self.chat_area.setGeometry(20, 20, 460, 400)
        self.chat_area.setReadOnly(True)

        self.prompt_area = QLineEdit(self)
        self.prompt_area.setGeometry(20, 440, 460, 40)
        self.prompt_area.returnPressed.connect(self.user_prompt)  # to input by pressing Enter Key

        send = QPushButton(self)
        send.setText('Send')
        send.setGeometry(430, 440, 50, 40)
        send.clicked.connect(self.user_prompt)

    def user_prompt(self):
        prompt = self.prompt_area.text().strip()
        # print(prompt)
        self.chat_area.append(f"<p style='color:#333333'>Me: {prompt}</p>")
        self.prompt_area.clear()

        # Issue: The user prompt waits till bot reply is generated to be added to the chat area
        # can be solved using threading
        thread = threading.Thread(target=self.reply_from_bot, args=(prompt, ))
        thread.start()

    def reply_from_bot(self, prompt):
        bot_reply = Chatbot().get_response(prompt)
        self.chat_area.append(f"<p style='color:#333333; background-color:#E9E9E9'>Bot: {bot_reply}</p>")

        # to format the text appended on chat area we need to use html


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())
