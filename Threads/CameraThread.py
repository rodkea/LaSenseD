from PyQt5.QtCore import QThread

class CameraThread(QThread):
  def __init__(self, parent = ...):
    super().__init__(parent)