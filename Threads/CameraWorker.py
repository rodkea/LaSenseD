from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QImage
import cv2

class CameraWorker(QObject):

  change_pixmap_signal = pyqtSignal(QImage)
  finished = pyqtSignal()

  def __init__(self, camera_index: int):    
    super().__init__()    
    self._running = False
    self._cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not self._cap.isOpened():
      print(f"Error: No se pudo abrir la cámara {self._camera_index}")
      self.finished.emit()
    try:
        self._cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self._cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        self._cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)        
    except Exception as e:
        print(f"Error al configurar la cámara: {e}")

  def test(self):
     print("BB")

  def run_camera(self):
    self._running = True    

    while self._running:
      ret, frame = self._cap.read()
      if ret:
          gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          h, w = gray_image.shape
          bytes_per_line = w
          qt_image = QImage(gray_image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
          self.change_pixmap_signal.emit(qt_image)
    
    if self._cap:
        self._cap.release()
    self.finished.emit()

    
  @pyqtSlot()
  def stop(self):
      self._running = False

  @pyqtSlot(float)
  def set_brightness(self, value: float):
      print("BRIGH")
      if self._cap:
          self._cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

  @pyqtSlot(float)
  def set_contrast(self, value: float):
      if self._cap:
          self._cap.set(cv2.CAP_PROP_CONTRAST, value)

  @pyqtSlot(float)
  def set_gain(self, value: float):
      if self._cap:
          self._cap.set(cv2.CAP_PROP_GAIN, value)

  @pyqtSlot(float)
  def set_sharpness(self, value: float):
      if self._cap:
          self._cap.set(cv2.CAP_PROP_SHARPNESS, value)
    

