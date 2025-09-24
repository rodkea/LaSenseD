from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from utils import read_file
from descriptors import d_fuzzy
import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap



class AnalyzeThread(QThread):

  finish = pyqtSignal(QPixmap, float, float)


  def __init__(self, filepath: str, parent: QWidget | None = None):
    super().__init__(parent)
    self._filepath = filepath


  def run(self):
    data = read_file(self._filepath)
    qt = d_fuzzy(data)
    mean = np.mean(qt)
    median = np.median(qt)
    normalized_qt = cv2.normalize(qt, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)
    heatmap_img_bgr = cv2.applyColorMap(normalized_qt, cv2.COLORMAP_JET)
    heatmap_img_rgb = cv2.cvtColor(heatmap_img_bgr, cv2.COLOR_BGR2RGB)
    h, w, ch = heatmap_img_rgb.shape
    bytes_per_line = ch * w
    qt_image = QImage(heatmap_img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qt_image)



    self.finish.emit(pixmap, mean, median)
    




