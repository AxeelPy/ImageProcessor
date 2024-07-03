from PyQt5.QtWidgets import QApplication
from dependencies.MainWindow import MyWindow

import os
import shutil
import atexit


def exitProcess():

    if os.path.exists("temp/"):

        shutil.rmtree("temp/")


if __name__ == "__main__":

    atexit.register(exitProcess)

    app = QApplication([])
    window = MyWindow()

    window.show()
    app.exec_()
