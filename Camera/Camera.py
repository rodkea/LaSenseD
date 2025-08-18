from PyQt5.QtWidgets import QComboBox,  QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import cv2
from Widgets import Button

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
    self._cb_cameras = QComboBox(self)
    self._btn = Button(
      icon_path="Assets/svg/camera-search.svg",
      icon_path_hover="Assets/svg/camera-search-hover.svg",
    )    
    self._btn.clicked.connect(self.detect_cameras)
    controls_layout.addWidget(self._cb_cameras)
    controls_layout.addWidget(self._btn, alignment=Qt.AlignHCenter)  
    controls_layout.setAlignment(Qt.AlignTop)
    self.detect_cameras()
    
  def detect_cameras(self):
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
