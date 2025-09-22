from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from utils import read_file
from descriptors import d_fuzzy
import numpy as np



class AnalyzeThread(QThread):

  finish = pyqtSignal(np.ndarray, float, float)


  def __init__(self, filepath: str, parent: QWidget | None = None):
    super().__init__(parent)
    self._filepath = filepath


  def run(self):
    data = read_file(self._filepath)
    print(data.shape)
    qt = d_fuzzy(data)
    mean = np.mean(qt)
    median = np.median(qt)
    self.finish.emit(qt, mean, median)
    




