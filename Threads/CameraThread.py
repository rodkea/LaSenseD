from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
import cv2

class CameraThread(QThread):

  change_pixmap_signal = pyqtSignal(QImage)

  def __init__(self, camera_index: int, parent: QWidget | None = None):
    super().__init__(parent)
    self._camera_index = camera_index
    self._running = True
    self._cap = None

  def run(self):
    self._running = True
    cap = cv2.VideoCapture(self._camera_index, cv2.CAP_DSHOW)
    try:
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        cap.set(cv2.CAP_PROP_AUTO_WB, 0) 
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

        while self._running:
            ret, frame = cap.read()
            if ret:
                gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                h, w = gray_image.shape
                bytes_per_line = w
                qt_image = QImage(gray_image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
                self.change_pixmap_signal.emit(qt_image)
    finally:
        cap.release()

  def stop(self):
    self._running = False
    self.wait()
