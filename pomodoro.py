from tkinter import E
from PyQt5.QtCore import QRect, QTime, QTimer, QUrl
from PyQt5.QtWidgets import QApplication, QLCDNumber, QWidget, QPushButton, QMessageBox
from PyQt5 import QtGui, QtMultimedia
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Pomodoro")
        self.setFixedSize(500, 500)
        self.player = QtMultimedia.QMediaPlayer()

        self.central_widget = QWidget(self)
        self.flag = 1
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeUpdate)

        self.pomoBtn = QPushButton(self.central_widget)
        self.pomoBtn.setGeometry(QRect(100, 50, 100, 50))
        self.pomoBtn.setText("Pomo")
        self.pomoClicked = 1
        self.pomoBtn.clicked.connect(self.pomo_btn_clicked)

        self.breakBtn = QPushButton(self.central_widget)
        self.breakBtn.setGeometry(QRect(300, 50, 100, 50))
        self.breakBtn.setText("Break")
        self.breakClicked = 1
        self.breakBtn.clicked.connect(self.break_btn_clicked)

        self.btn = QPushButton(self.central_widget)
        self.btn.setGeometry(QRect(200, 300, 100, 50))
        self.btn.setText("Start")
        self.btn.clicked.connect(self.btn_clicked)

        self.lcd_count = QLCDNumber(self.central_widget)
        self.lcd_count.setGeometry(QRect(100, 130, 300, 100))
        self.lcd_count.setDigitCount(5)
        self.btn_s = 0
        self.btn_m = 25
        self.btn_h = 0
        self.lcd_count.display(
            QTime(self.btn_h, self.btn_m, self.btn_s).toString())

    def timeUpdate(self):
        if self.flag == 0:
            if self.btn_s == 0:
                self.btn_s = 59
                self.btn_m -= 1
                if self.btn_m == 0:
                    QMessageBox.information(self, "Remind", "It's time to take a break!")
                    self.btn_s, self.btn_m, self.btn_h = 0, 0, 0
                    self.flag = 1
                    self.btn.setText("Start")
            else:
                self.btn_s -= 1
            self.lcd_count.display(
                QTime(self.btn_h, self.btn_m, self.btn_s).toString())
        else:
            self.lcd_count.display(
                QTime(self.btn_h, self.btn_m, self.btn_s).toString())

    def pomo_btn_clicked(self):
        if self.flag == 0:
            QMessageBox.information(self, "Remind", "It's running, please cancle first!")
            return
        if self.pomoClicked == 0:
            self.playAudioFile("button-press.wav")
            self.btn_s, self.btn_m, self.btn_h = 0, 25, 0
            self.pomoClicked = 1
            self.lcd_count.display(
                QTime(self.btn_h, self.btn_m, self.btn_s).toString())
        elif self.pomoClicked == 1:
            self.playAudioFile("button-press.wav")
            self.btn_s, self.btn_m, self.btn_h = 0, 50, 0
            self.pomoClicked = 0
            self.lcd_count.display(
                QTime(self.btn_h, self.btn_m, self.btn_s).toString())

    def break_btn_clicked(self):
        if self.flag == 0:
            QMessageBox.information(self, "Remind", "It's running, please cancle first!")
            return
        if self.breakClicked == 1:
            self.playAudioFile("button-press.wav")
            self.btn_s, self.btn_m, self.btn_h = 0, 5, 0
            self.breakClicked = 0
            self.lcd_count.display(
                QTime(self.btn_h, self.btn_m, self.btn_s).toString())
        elif self.breakClicked == 0:
            self.playAudioFile("button-press.wav")
            self.btn_s, self.btn_m, self.btn_h = 0, 15, 0
            self.breakClicked = 1
            self.lcd_count.display(
                QTime(self.btn_h, self.btn_m, self.btn_s).toString())

    def btn_clicked(self):
        if self.flag == 1:
            self.playAudioFile("button-press.wav")
            self.btn.setText("Cancle")
            self.flag = 0
        elif self.flag == 0:
            self.playAudioFile("complete.mp3")
            self.btn.setText("Start")
            self.btn_s, self.btn_m, self.btn_h = 0, 0, 0
            self.flag = 1

    def playAudioFile(self, filename):
        full_file_path = resource_path(filename)
        url = QUrl.fromLocalFile(full_file_path)
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget{font-size: 14pt;}")
    app.setWindowIcon(QtGui.QIcon(resource_path("icon.png")))
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
