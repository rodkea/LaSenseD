from PyQt5.QtWidgets import QComboBox,  QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from Threads import CameraThread
import cv2
from Widgets import Button, SpinBox
import os

class Camera(QWidget):

  def __init__(self, parent: QWidget | None = None):
    super().__init__(parent)
    main_layout = QHBoxLayout()
    self.setLayout(main_layout)
    self._lb_video = QLabel(self)
    self._lb_video.setStyleSheet("background-color: #333; border-radius: 5px;")
    self._lb_video.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(self._lb_video, 1)

    # --- CONTROLES ---
    controls_layout = QVBoxLayout()
    main_layout.addLayout(controls_layout)
    # ------ CAMERA SELECT -------
    cameras_layout = QHBoxLayout()
    controls_layout.addLayout(cameras_layout)
    self._cb_cameras = QComboBox(self)
    self._btn = Button(
      icon_path="Assets/svg/camera-search.svg",
      icon_path_hover="Assets/svg/camera-search-hover.svg",
    )    
    self._btn.clicked.connect(self.detect_cameras)
    cameras_layout.addWidget(self._btn, alignment=Qt.AlignHCenter)  
    cameras_layout.addWidget(self._cb_cameras)
    
    # ------ BRIGHNETS -------
    self._brightness_control = SpinBox(
      icon_path="Assets/svg/brightness.svg",
      tooltip="Brillo",
      signal=None,
      min_value=-1.0,
      max_value=1.0,
      height=30,
      width=30
           
    )
    controls_layout.addWidget(self._brightness_control)
    # ------ CONTRAST -------
    self._contrast_control = SpinBox(
      icon_path="Assets/svg/contrast.svg",
      tooltip="Contraste",
      signal=None,
      min_value=-1.0,
      max_value=1.0,
      height=25,
      width=25
           
    )
    controls_layout.addWidget(self._contrast_control)

    controls_layout.setAlignment(Qt.AlignTop)

    self._thread = None
    self.detect_cameras()
    
  def detect_cameras(self):
    self.stop_camera()
    self._cb_cameras.clear()
    index = 0
    available_cameras = []

    while True:        
     
      cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)        
      if cap.isOpened():          
        camera_name = f"CAMARA {index}"
        available_cameras.append(camera_name)          
        cap.release()
        index += 1
      else:          
        cap.release()
        break
    
    if available_cameras:        
      self._cb_cameras.addItems(available_cameras)

    self._cb_cameras.blockSignals(False)
    self.start_camera_thread()

  def start_camera_thread(self):
    if self._thread is not None and self._thread.isRunning():
        self._thread.stop()
    
    camera_index = self._cb_cameras.currentIndex()
    if camera_index < 0:
        return
    self._thread = CameraThread(camera_index=camera_index, parent=self)
    self._thread.change_pixmap_signal.connect(self.update_image)
    self._thread.start()

  def stop_camera(self):
    if self._thread and self._thread.isRunning():
        try:
            self._thread.change_pixmap_signal.disconnect(self.update_image)
        except TypeError:
            pass  # ya estaba desconectada
        self._thread.stop()
        self._thread = None
        self._lb_video.clear()

  @pyqtSlot(QImage)
  def update_image(self, qt_image: QImage):
    pixmap = QPixmap.fromImage(qt_image)
    scaled_pixmap = pixmap.scaled(self._lb_video.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self._lb_video.setPixmap(scaled_pixmap)
  
  def closeEvent(self, event):
    if self._thread is not None:
      self._thread.stop()
    event.accept()
