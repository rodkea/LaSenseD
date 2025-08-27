from Config import ConfigType, read_config, write_config, USER_CONFIG_PATH, DEFAULT_CONFIG_PATH
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
    self._default_config = read_config(DEFAULT_CONFIG_PATH)
    self._user_config = read_config(USER_CONFIG_PATH)


  def run(self):
    self._running = True
    self._cap = cv2.VideoCapture(self._camera_index, cv2.CAP_DSHOW)
    try:
        self._cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self._cap.set(cv2.CAP_PROP_AUTO_WB, 0) 
        self._cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self._cap.set(cv2.CAP_PROP_BRIGHTNESS, self._user_config['Brightness'])
        self._cap.set(cv2.CAP_PROP_CONTRAST, self._user_config['Contrast'])
        self._cap.set(cv2.CAP_PROP_GAIN, self._user_config['ISO'])
        self._cap.set(cv2.CAP_PROP_SHARPNESS, self._user_config['Sharpness'])

        while self._running:
            ret, frame = self._cap.read()
            if ret:
                gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                h, w = gray_image.shape
                bytes_per_line = w
                qt_image = QImage(gray_image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
                self.change_pixmap_signal.emit(qt_image)
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