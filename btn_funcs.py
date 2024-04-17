from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

def show_editBtn(self):
    pass

def hide_editBtn(self):
    pass

def editMode(self, currentvalue: int):
    self.slider = QSlider(Qt.Orientation.Horizontal, self)
    self.slider.setMinimum(1)
    self.slider.setMaximum(200)
    self.slider.setValue(currentvalue)
    self.slider.valueChanged(self.update)
    self.editBtn.setText(",,,")

def update(self):
    print("Update function called")