from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
import cv2
import time
from queue import Queue

class CameraThread(QThread):

  change_pixmap_signal = pyqtSignal(QImage)

  def __init__(self, camera_index: int, parent: QWidget | None = None):
    super().__init__(parent)  
    self.queue = Queue()    
    self._running = True
    self._recording = False    
    self._cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW) 
    time.sleep(0.2)
    

  def run(self):
    try:        
      self._cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
      self._cap.set(cv2.CAP_PROP_AUTO_WB, 0) 
      self._cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)        

      while self._running:
        ret, frame = self._cap.read()        
        if ret:
          gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          h, w = gray_image.shape
          bytes_per_line = w
          qt_image = QImage(gray_image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
          self.change_pixmap_signal.emit(qt_image)
          if self._recording:
            self.queue.put(gray_image)

    finally:
      self._cap.release()

  
  def stop(self):
    self._running = False
    self.wait()

  def set_brightness(self, value: float):    
    self._cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

  def set_contrast(self, value: float):    
    self._cap.set(cv2.CAP_PROP_CONTRAST, value)

  def set_gain(self, value: float):
    self._cap.set(cv2.CAP_PROP_GAIN, value)

  def set_sharpness(self, value: float):
    self._cap.set(cv2.CAP_PROP_SHARPNESS, value)

  def record(self):
    self._recording = True

  def stop_record(self):
    self._recording = False

  
  