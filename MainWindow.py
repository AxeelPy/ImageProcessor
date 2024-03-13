from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap
from imgprocessor import imgprocessor
from PyQt5.QtCore import Qt
import os
import threading as th


class MyWindow(QMainWindow):

    # Starting process
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Resizable Text Areas")
        self.setGeometry(100, 100, 800, 600)

        self.label1 = QLabel(self)
        self.pixmap = QPixmap("images/rndm2.jpg")
        self.label1.setPixmap(self.pixmap)
        self.label1.ratio = self.pixmap.width() / self.pixmap.height()

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

        self.setFolderBtn = QPushButton(self)
        self.setFolderBtn.setStyleSheet("QPushButton {border-image: url(resources/explorer.jpeg);}")
        self.setFolderBtn.clicked.connect(self.BtnPath)

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

    # Choose folder path on separate window, instead of writing path
    def BtnPath(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if not file == "":
            self.text_area3.setText(file)

    # Registering key presses for accesibility functionalities 
    def keyPressEvent(self, event):
        
        # This is the enter key (16777220)
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

    # Default auto element size adjusting
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

        text_area3_width = int(window_width * 0.25)
        text_area3_height = int(window_height * 0.05)
        self.text_area3.resize(text_area3_width, text_area3_height)
        self.text_area3.move(window_width - text_area3_width - int(window_width * 0.05) - 10, 50 + text_area1_height + text_area2_height)

        self.setFolderBtn.resize(int(window_width * 0.05), int(window_height * 0.05))
        self.setFolderBtn.move(window_width - int(window_width * 0.05) -10, 50 + text_area1_height + text_area2_height)

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

    # Displays errors to client
    def errorMsg(self, message):
        self.errormsg.setText(message)

    # Loading the next before and after picture
    def NextPic(self):

        # Opposite button becomes enabled
        self.backBtn.setEnabled(True)

        self.index = self.index + 1

        # Checking if original image is cached in returnlist
        if not self.returnlist[self.index]["ofile"] is None:
            self.pixmap = self.returnlist[self.index]["ofile"]
            self.label1.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.returnlist[self.index]["path"] + "-original" + self.returnlist[self.index]["extension"])
            self.label1.setPixmap(self.pixmap)
            self.returnlist[self.index]["ofile"] = self.pixmap

        self.label1.ratio = self.pixmap.width() / self.pixmap.height()

        # Checking if edited image is cached in returnlist
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

        # Disabling button if at end of image list
        if self.index+1 == len(self.returnlist):
            self.nextBtn.setEnabled(False)

    # Loading one before and after picture ago
    def LastPic(self):

        # Enabling opposite button
        self.nextBtn.setEnabled(True)

        self.index = self.index - 1

        # Checking if original image is cached in returnlist
        if not self.returnlist[self.index]["ofile"] is None:
            self.pixmap = self.returnlist[self.index]["ofile"]
            self.label1.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.returnlist[self.index]["path"] + "-original" + self.returnlist[self.index]["extension"])
            self.label1.setPixmap(self.pixmap)
            self.returnlist[self.index]["ofile"] = self.pixmap

        self.label1.ratio = self.pixmap.width() / self.pixmap.height()

        # Checking if edited image is cached in returnlist
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

        # Disabling button if at end of list
        if self.index-1 < 0:
            self.backBtn.setEnabled(False)

    # Image processing thread
    def imgmp(self, file):
        
        # Main process, runs another module
        returnage = imgprocessor(self.tx3 + "/" + file, self.tx1, self.tx2)

        if returnage["error"] is False:

            # Returnlist for other functions being updated, along with the counter to calculate the %
            self.returnlist.append(returnage)
            self.done = self.done + 1
            self.imgnum.setText(str(self.index+1) + " of " + str(len(self.returnlist)))
            self.imgprc.setText(f"{self.done}/{self.fromlen}\n{int((self.done)/(self.fromlen)*100)}% Done")

            self.nextBtn.setEnabled(True)

        else:

            print("Error raised by imgprocessor. Ignoring that file")
            self.fromlen = self.fromlen - 1

    # Clears current images to avoid user confusion
    def loadingStage(self):
        self.label1.setPixmap(QPixmap())
        self.label2.setPixmap(QPixmap())
    
    # Pre error checking and handling
    def BtnErrorCheck(self):
        
        if os.path.exists(self.tx3):
            self.path = os.listdir(self.tx3)
        else:
            self.errorMsg("Path doesn't exist")
            return
        try:
            if not self.tx1 == "":
                self.tx1 = float(self.tx1)
            if not self.tx2 == "":
                self.tx2 = float(self.tx2)
        except Exception:
            self.errorMsg("Fields 1 and 2 have to be numbers")
            return

    # Main onclick run function
    def BtnFunction(self):

        # Take content of buttons
        self.errormsg.setText("")
        self.tx1 = self.text_area1.text()
        self.tx2 = self.text_area2.text()
        self.tx3 = self.text_area3.text()

        self.BtnErrorCheck()
        
        # Preconfig
        self.loadingStage()
        self.returnlist = []
        self.index = 1
        threads = []
        self.done = 0
        self.fromlen = len(self.path)

        # First image to load GUI with self.Lastpic()
        self.imgmp(self.path[0])
        self.path.pop(0)
        self.LastPic()
        self.imgnum.setText(str(str(self.index) + " of " + str(len(self.returnlist))))
        self.adjust_text_area_sizes("change")

        # Thread for all files in folder
        for file in self.path:
            t = th.Thread(target=self.imgmp, args=(file,))
            threads.append(t)
            t.start()