from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QPlainTextEdit, QLineEdit
from PyQt5.QtGui import QPixmap
from main import imgprocessor
from PyQt5.QtCore import Qt
import os
import shutil
import threading as th
import atexit


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Resizable Text Areas")
        self.setGeometry(100, 100, 800, 600)

        self.label1 = QLabel(self)
        self.pixmap = QPixmap("images/rndm2.jpg")
        print(self.pixmap.width())
        self.label1.setPixmap(self.pixmap)
        self.label1.ratio = self.pixmap.width() / self.pixmap.height()
        print("ratio start", self.label1.ratio, self.pixmap.width(), self.pixmap.height())

        self.label2 = QLabel(self)
        self.pixmap = QPixmap("images/62iupl.jpg")
        self.label2.setPixmap(self.pixmap)
        self.label2.ratio = self.pixmap.width() / self.pixmap.height()

        self.text_area1 = QLineEdit(self)
        self.text_area1.setPlaceholderText("Target brightness (optional) (default 100)")

        self.text_area2 = QLineEdit(self)
        self.text_area2.setPlaceholderText("Precision (optional) (default 0.5)")

        self.text_area3 = QLineEdit(self)
        self.text_area3.setPlaceholderText("Path (required)")

        self.runBtn = QPushButton("Run", self)
        self.runBtn.clicked.connect(self.BtnFunction)

        self.nextBtn = QPushButton("+", self)
        self.nextBtn.clicked.connect(self.NextPic)
        self.nextBtn.setEnabled(False)

        self.backBtn = QPushButton("-", self)
        self.backBtn.clicked.connect(self.LastPic)
        self.backBtn.setEnabled(False)

        self.imgnum = QLabel("", self)
        self.imgnum.move(10, int(int(self.width() * 0.3) / self.label2.ratio) + 20)

        self.imgprc = QLabel("", self)
        self.imgprc.move(10, int(int(self.width() * 0.3) / self.label2.ratio) + 20)

        self.errormsg = QLabel("", self)
        self.errormsg.setStyleSheet("color:red;")

        self.resizeEvent = self.adjust_text_area_sizes

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == 16777220:
            if self.text_area1.hasFocus():
                self.text_area2.focusNextChild()
            elif self.text_area2.hasFocus():
                self.text_area3.focusNextChild()
            elif self.text_area3.hasFocus():
                self.BtnFunction()
        elif event.key() == Qt.Key_Up:
            if self.index + 1 < len(self.returnlist):
                self.NextPic()
        elif event.key() == Qt.Key_Down:
            if not self.index - 1 < 0:
                self.LastPic()

    def adjust_text_area_sizes(self, event):
        window_width, window_height = self.width(), self.height()
        text_area1_width = int(window_width * 0.3)
        text_area1_height = int(window_height * 0.05)
        self.text_area1.resize(text_area1_width, text_area1_height)
        self.text_area1.move(window_width - text_area1_width - 10, 10)
        text_area2_width = int(window_width * 0.3)
        text_area2_height = int(window_height * 0.05)
        self.text_area2.resize(text_area2_width, text_area2_height)
        self.text_area2.move(window_width - text_area2_width - 10, 30 + text_area1_height)

        text_area3_width = int(window_width * 0.3)
        text_area3_height = int(window_height * 0.05)
        self.text_area3.resize(text_area3_width, text_area3_height)
        self.text_area3.move(window_width - text_area3_width - 10, 50 + text_area1_height + text_area2_height)

        self.runBtn.resize(int(window_width * 0.3), int(window_height * 0.05))
        self.runBtn.move(int(window_width - self.runBtn.width() - 10), 70 + text_area1_height + text_area2_height +
                         text_area3_height)

        self.nextBtn.resize(int(window_width * 0.03), int(window_height * 0.05))
        self.nextBtn.move(int(window_width - self.nextBtn.width() - 10), 90 + text_area1_height + text_area2_height +
                         text_area3_height + int(window_height * 0.05))

        self.backBtn.resize(int(window_width * 0.03), int(window_height * 0.05))
        self.backBtn.move(int(window_width - self.nextBtn.width() - self.backBtn.width() - 10), 90 + text_area1_height +
                          text_area2_height + text_area3_height + int(window_height * 0.05))

        self.label1.setScaledContents(True)
        self.label1.move(0, 0)
        self.label1.resize(int(window_width * 0.3), int(int(window_width * 0.3) / self.label1.ratio))

        self.label2.setScaledContents(True)
        self.label2.move(int(window_width * 0.3), 0)
        self.label2.resize(int(window_width * 0.3), int(int(window_width * 0.3) / self.label2.ratio))

        self.imgnum.move(10, int(int(window_width * 0.3) / self.label1.ratio) + 20)
        self.imgprc.move(10, int(int(window_width * 0.3) / self.label1.ratio) + self.imgnum.height() + 20)

        self.errormsg.resize(int(window_width * 0.3), 25)
        self.errormsg.move(int(window_width - self.runBtn.width()), 100 + text_area1_height +
                          text_area2_height + text_area3_height)

    def errorMsg(self, message):
        self.errormsg.setText(message)

    def NextPic(self):
        self.backBtn.setEnabled(True)

        self.index = self.index + 1

        if not self.returnlist[self.index]["ofile"] is None:
            self.pixmap = self.returnlist[self.index]["ofile"]
            self.label1.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.returnlist[self.index]["path"] + "-original" + self.returnlist[self.index]["extension"])
            self.label1.setPixmap(self.pixmap)
            self.returnlist[self.index]["ofile"] = self.pixmap
        self.label1.ratio = self.pixmap.width() / self.pixmap.height()

        if not self.returnlist[self.index]["efile"] is None:
            self.pixmap = self.returnlist[self.index]["efile"]
            self.label2.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.returnlist[self.index]["path"] + "-edited" + self.returnlist[self.index]["extension"])
            self.label2.setPixmap(self.pixmap)
            self.returnlist[self.index]["efile"] = self.pixmap
        self.label2.ratio = self.pixmap.width() / self.pixmap.height()

        self.imgnum.setText(str(str(self.index+1) + " of " + str(len(self.returnlist))))

        self.adjust_text_area_sizes("change")

        if self.index + 1 == len(self.returnlist):
            self.nextBtn.setEnabled(False)

    def LastPic(self):
        self.nextBtn.setEnabled(True)

        self.index = self.index - 1

        if not self.returnlist[self.index]["ofile"] is None:
            self.pixmap = self.returnlist[self.index]["ofile"]
            self.label1.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.returnlist[self.index]["path"] + "-original" + self.returnlist[self.index]["extension"])
            self.label1.setPixmap(self.pixmap)
            self.returnlist[self.index]["ofile"] = self.pixmap
        self.label1.ratio = self.pixmap.width() / self.pixmap.height()

        if not self.returnlist[self.index]["efile"] is None:
            self.pixmap = self.returnlist[self.index]["efile"]
            self.label2.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.returnlist[self.index]["path"] + "-edited" + self.returnlist[self.index]["extension"])
            self.label2.setPixmap(self.pixmap)
            self.returnlist[self.index]["efile"] = self.pixmap
        self.label2.ratio = self.pixmap.width() / self.pixmap.height()

        self.adjust_text_area_sizes("change")

        self.imgnum.setText(str(str(self.index+1) + " of " + str(len(self.returnlist))))

        if self.index - 1 < 0:
            self.backBtn.setEnabled(False)

    def imgmp(self, file, tx1, tx2, tx3):
        print('dos')
        print("Sending file", tx3 + "/" + file)
        returnage = imgprocessor(tx3 + "/" + file, tx1, tx2)
        print("img function returned", returnage)
        print(returnage["path"] + returnage["extension"])
        if returnage["error"] is False:
            self.returnlist.append(returnage)
            self.imgnum.setText(str(self.index + 1) + " of " + str(len(self.returnlist)))
            self.done = self.done + 1
            self.imgprc.setText(f"{self.done+1}/{self.fromlen+1}\n{int((self.done)/(self.fromlen)*100)}% Done")
            self.nextBtn.setEnabled(True)
        else:
            print("Error raised by imgprocessor. Ignoring that file")
            self.fromlen = self.fromlen - 1

    def BtnFunction(self):
        self.errormsg.setText("")
        print("btn function")
        tx1 = self.text_area1.text()
        tx2 = self.text_area2.text()
        tx3 = self.text_area3.text()
        print("yes")
        print(tx1, tx2, tx3)
        if os.path.exists(tx3):
            path = os.listdir(tx3)
        else:
            self.errorMsg("Path doesn't exist")
            return
        try:
            if not tx1 == "":
                tx1 = float(tx1)
            if not tx2 == "":
                tx2 = float(tx2)
        except Exception:
            self.errorMsg("Fields 1 and 2 have to be numbers")
            return

        self.returnlist = []
        self.index = 0

        while True:
            firstresult = imgprocessor(tx3+"/"+path[0], tx1, tx2)
            if firstresult["error"] is False:
                self.returnlist.append(firstresult)
                if not self.returnlist[self.index]["ofile"] is None:
                    self.pixmap = self.returnlist[self.index]["ofile"]
                    self.label1.setPixmap(self.pixmap)
                else:
                    self.pixmap = QPixmap(
                        self.returnlist[self.index]["path"] + "-original" + self.returnlist[self.index]["extension"])
                    self.label1.setPixmap(self.pixmap)
                    self.returnlist[self.index]["ofile"] = self.pixmap
                self.label1.ratio = self.pixmap.width() / self.pixmap.height()

                if not self.returnlist[self.index]["efile"] is None:
                    self.pixmap = self.returnlist[self.index]["efile"]
                    self.label2.setPixmap(self.pixmap)
                else:
                    self.pixmap = QPixmap(
                        self.returnlist[self.index]["path"] + "-edited" + self.returnlist[self.index]["extension"])
                    self.label2.setPixmap(self.pixmap)
                    self.returnlist[self.index]["efile"] = self.pixmap
                self.label2.ratio = self.pixmap.width() / self.pixmap.height()
                self.nextBtn.setEnabled(True)
                break
            else:
                print("Error in firstresult. Probably not an image")
                path.pop(0)
                if len(path) == 1:
                    self.imgnum.setText("")
                    self.imgprc.setText("")
                    self.errorMsg("Folder doesn't have any images")
                    break
        path.pop(0)
# C:\Users\axel\Pictures\Screenshots
        threads = []
        self.done = 0
        self.fromlen = len(path)
        for file in path:
            t = th.Thread(target=self.imgmp, args=(file, tx1, tx2, tx3))
            threads.append(t)
            t.start()
        #for t in threads:
        #    t.join()
        #    print(f"thread {t.ident} has finished")

        self.imgnum.setText(str(str(self.index+1) + " of " + str(len(self.returnlist))))

        self.adjust_text_area_sizes("change")


def exitProcess():
    if os.path.exists("temp/"):
        shutil.rmtree("temp/")


if __name__ == "__main__":
    atexit.register(exitProcess)
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
