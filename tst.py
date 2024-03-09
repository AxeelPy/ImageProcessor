from main import imgprocessor
import threading as th
import os

class crass():
    def imgmp(self, path, tx1, tx2, tx3):
        for file in path:
            print("Sending file", tx3+"/"+file)
            returnage = imgprocessor(tx3+"/"+file, tx1, tx2)
            print("img function returned", returnage)
            print(returnage["path"]+returnage["extension"])

    def main(self):
        tx3 = "images"
        path = os.listdir(tx3)
        tx1 = ""
        tx2 = ""
        t = th.Thread(target=crass.imgmp, args=(self, path, tx1, tx2, tx3))
        t.start()

crass.main("he")