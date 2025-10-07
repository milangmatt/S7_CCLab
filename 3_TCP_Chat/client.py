import sys
import socket
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QInputDialog
)
from PyQt5.QtCore import pyqtSignal, QObject

HOST = '127.0.0.1'
PORT = 65433

class MessageSignal(QObject):
    message_received = pyqtSignal(str)

class ChatClient(QWidget):
    def __init__(self, nickname):
        super().__init__()
        self.nickname = nickname

        self.setWindowTitle(f"Chat - {self.nickname}")
        self.resize(400, 550)

        # Chat area
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ddd;
                font-size: 12pt;
                padding: 5px;
            }
        """)

        # Input field
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type a message...")
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: #fff;
                padding: 8px;
                border-radius: 5px;
            }
        """)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 8px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_box)
        layout.addLayout(input_layout)
        self.setLayout(layout)

        # Socket connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        # Signal for thread-safe UI update
        self.signal = MessageSignal()
        self.signal.message_received.connect(self.display_message)

        # Start receiving thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        text = self.input_box.text().strip()
        if text:
            message = f"<{self.nickname}> {text}"
            try:
                self.sock.sendall(message.encode())
            except:
                self.chat_box.append("<System> Connection lost.")
            self.display_message(message, local=True)  # Show immediately
            self.input_box.clear()

    def receive_messages(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                if msg:
                    self.signal.message_received.emit(msg)
                else:
                    break
            except:
                break

    def display_message(self, raw_text, local=False):
        # Parse sender and message
        if raw_text.startswith("<") and ">" in raw_text:
            end = raw_text.find(">")
            sender = raw_text[1:end]
            text = raw_text[end + 2:]
        else:
            sender = "Unknown"
            text = raw_text

        # Determine if the message is from me
        is_self = local or (sender == self.nickname)
        display_name = "You" if is_self else sender

        # Alignment and colors
        if is_self:
            alignment = "right"
            bubble_color = "#6100d7"
        else:
            alignment = "left"
            bubble_color = "#333"

        # Create HTML with name above the bubble
        html = f"""
        <table width="100%" cellpadding="2">
            <tr>
                <td align="{alignment}">
                    <div style="color:#aaa; font-size:10pt; margin-bottom:2px;">{display_name}</div>
                    <div style="
                        background:{bubble_color};
                        color:white;
                        padding:8px;
                        border-radius:12px;
                        max-width:66%;
                        display:inline-block;
                        word-wrap: break-word;
                    ">
                        {text}
                    </div>
                </td>
            </tr>
        </table>
        """

        # Append to chat box
        self.chat_box.moveCursor(self.chat_box.textCursor().End)
        self.chat_box.insertHtml(html)
        self.chat_box.insertHtml("<br>")
        self.chat_box.verticalScrollBar().setValue(self.chat_box.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Get nickname before window creation
    nickname, ok = QInputDialog.getText(None, "Nickname", "Enter your nickname:")
    if not ok or not nickname.strip():
        sys.exit()
    nickname = nickname.strip()

    client = ChatClient(nickname)
    client.show()
    sys.exit(app.exec_())
