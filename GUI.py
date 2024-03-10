from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QPlainTextEdit, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from main import imgprocessor
import os
import threading as th


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

        self.imgnum = QLabel("placeholder", self)
        self.imgnum.move(10, int(int(self.width() * 0.3) / self.label2.ratio) + 20)

        self.resizeEvent = self.adjust_text_area_sizes

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            if self.backBtn.isEnabled():
                self.LastPic()
        elif event.key() == Qt.Key_Up:
            if self.nextBtn.isEnabled():
                self.NextPic()
        elif event.key() == 16777220:
            print("enter key")
            if self.text_area1.hasFocus():
                self.text_area2.focusNextChild()
            elif self.text_area2.hasFocus():
                self.text_area3.focusNextChild()
            elif self.text_area3.hasFocus():
                self.BtnFunction()

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
        self.nextBtn.move(int(window_width - self.runBtn.width() - 10), 90 + text_area1_height + text_area2_height +
                         text_area3_height + int(window_height * 0.05))

        self.backBtn.resize(int(window_width * 0.03), int(window_height * 0.05))
        self.backBtn.move(int(window_width - self.runBtn.width() - window_width * 0.03 - 10), 90 + text_area1_height +
                          text_area2_height + text_area3_height + int(window_height * 0.05))

        self.label1.setScaledContents(True)
        self.label1.move(0, 0)
        self.label1.resize(int(window_width * 0.3), int(int(window_width * 0.3) / self.label1.ratio))

        self.label2.setScaledContents(True)
        self.label2.move(int(window_width * 0.3), 0)
        self.label2.resize(int(window_width * 0.3), int(int(window_width * 0.3) / self.label2.ratio))

        self.imgnum.move(10, int(int(window_width * 0.3) / self.label1.ratio) + 20)

    def NextPic(self):
        self.backBtn.setEnabled(True)

        self.index = self.index + 1

        if not self.returnlist[self.index]["ofile"] is None:
            print("Already exists")
            self.pixmap = self.returnlist[self.index]["ofile"]
            self.label1.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.returnlist[self.index]["path"] + "-original" + self.returnlist[self.index]["extension"])
            self.label1.setPixmap(self.pixmap)
            self.returnlist[self.index]["ofile"] = self.pixmap
        self.label1.ratio = self.pixmap.width() / self.pixmap.height()

        if not self.returnlist[self.index]["efile"] is None:
            print("Already exists")
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
            print("Already exists")
            self.pixmap = self.returnlist[self.index]["ofile"]
            self.label1.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.returnlist[self.index]["path"] + "-original" + self.returnlist[self.index]["extension"])
            self.label1.setPixmap(self.pixmap)
            self.returnlist[self.index]["ofile"] = self.pixmap
        self.label1.ratio = self.pixmap.width() / self.pixmap.height()

        if not self.returnlist[self.index]["efile"] is None:
            print("Already exists")
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
            self.nextBtn.setEnabled(True)
        else:
            print("Error raised by imgprocessor. Ignoring that file")

    def BtnFunction(self):
        tx1 = self.text_area1.text()
        tx2 = self.text_area2.text()
        tx3 = self.text_area3.text()
        if os.path.exists(tx3):
            path = os.listdir(tx3)
        else:
            print("dir doesn't exist")
            return
        try:
            if not tx1 == "":
                tx1 = float(tx1)
            if not tx2 == "":
                tx2 = float(tx2)
        except Exception:
            print('not able to convert to float')
            return

        self.returnlist = []
        self.index = 0
        while True:
            firstresult = imgprocessor(tx3+"/"+path[0], tx1, tx2)
            if firstresult["error"] is False:
                self.returnlist.append(firstresult)
                if not self.returnlist[self.index]["ofile"] is None:
                    print("Already exists")
                    self.pixmap = self.returnlist[self.index]["ofile"]
                    self.label1.setPixmap(self.pixmap)
                else:
                    self.pixmap = QPixmap(
                        self.returnlist[self.index]["path"] + "-original" + self.returnlist[self.index]["extension"])
                    self.label1.setPixmap(self.pixmap)
                    self.returnlist[self.index]["ofile"] = self.pixmap
                self.label1.ratio = self.pixmap.width() / self.pixmap.height()

                if not self.returnlist[self.index]["efile"] is None:
                    print("Already exists")
                    self.pixmap = self.returnlist[self.index]["efile"]
                    self.label2.setPixmap(self.pixmap)
                else:
                    self.pixmap = QPixmap(
                        self.returnlist[self.index]["path"] + "-edited" + self.returnlist[self.index]["extension"])
                    self.label2.setPixmap(self.pixmap)
                    self.returnlist[self.index]["efile"] = self.pixmap
                self.label2.ratio = self.pixmap.width() / self.pixmap.height()
                self.nextBtn.setEnabled(True)
                path.pop(0)
                break
            else:
                print("Error in firstresult. Probably not an image")
                path.pop(0)
# C:\Users\axel\Pictures\Screenshots
        threads = []
        for file in path:
            t = th.Thread(target=self.imgmp, args=(file, tx1, tx2, tx3))
            threads.append(t)
            t.start()
        #for t in threads:
        #    t.join()
        #    print(f"thread {t.ident} has finished")

        self.imgnum.setText(str(str(self.index+1) + " of " + str(len(self.returnlist))))

        self.adjust_text_area_sizes("change")


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
