import cv2
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtWidgets import QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from Widgets import Button, SpinBox
from configparser import ConfigParser

class CameraControls(QWidget):

  
  brightness_changed = pyqtSignal(float)
  contrast_changed = pyqtSignal(float)
  gain_changed = pyqtSignal(float)
  sharpness_changed = pyqtSignal(float)
  default_pressed = pyqtSignal()
  detect_cameras_pressed = pyqtSignal()
  camera_selected_changed = pyqtSignal(int)
  
  def __init__(self, parent: QWidget | None = None, user_config : ConfigParser | None = None, user_defaults : ConfigParser | None = None):
    super().__init__(parent)
    # LAYOUT
    _layout = QVBoxLayout()
    self.setLayout(_layout)
    _layout.setContentsMargins(0, 20, 0, 0)
    _layout.setSpacing(2)
    _layout.setAlignment(Qt.AlignCenter)
    # DEFAULTS
    self._user_defaults = user_defaults 
    # CAMERA CONTROLS
    # -- CAMERA SELECT --
    _camera_select_layout = QHBoxLayout()
    _camera_select_layout.setContentsMargins(0, 0, 0, 0)
    _camera_select_layout.setSpacing(5)
    _camera_select_layout.setAlignment(Qt.AlignCenter)

    self._cb_cameras = QComboBox()
    self._cb_cameras.setFixedWidth(80)  # 🔹 ancho fijo para que no empuje
    self._cb_cameras.currentIndexChanged.connect(self.camera_selected)
    self._btn_search = Button(
      icon_path="Assets/svg/camera-search.svg",
      icon_path_hover="Assets/svg/camera-search-hover.svg",
      signal=self.detect_cameras_pressed      
    )    

    _camera_select_layout.addWidget(self._btn_search, alignment=Qt.AlignCenter)
    _camera_select_layout.addWidget(self._cb_cameras, alignment=Qt.AlignCenter)

    _layout.addLayout(_camera_select_layout)
    # -- BRIGHTNESS --
    self._brightness_control = SpinBox(
      icon_path="Assets/svg/brightness.svg",
      tooltip="Brillo",
      min_value=0.0,
      max_value=1023.0,
      step=1,
      decimals=0,
      initial_value=user_config.getfloat('CameraSettings', 'brightness'),
      signal=self.brightness_changed,
      height=30,
      width=30
    )
    _layout.addWidget(self._brightness_control)

    # -- CONTRAST --
    self._contrast_control = SpinBox(
      icon_path="Assets/svg/contrast.svg",
      tooltip="Contraste",
      signal=self.contrast_changed,
      min_value=-10.0,
      max_value=30.0,
      step=1,
      initial_value=user_config.getfloat('CameraSettings', 'contrast'),
      decimals=0,
      height=23,
      width=23
    )
    _layout.addWidget(self._contrast_control)

    # -- GAIN --
    self._gain_control = SpinBox(
      icon_path="Assets/svg/iso.svg",
      tooltip="Ganancia",
      signal=self.gain_changed,
      min_value=0.0,
      max_value=1956,
      step=1,
      initial_value=user_config.getfloat('CameraSettings', 'gain'),
      decimals=0,
      height= 30,
      width=30 
    )
    _layout.addWidget(self._gain_control)

    # -- SHARPNESS --
    self._sharpness_control = SpinBox(
      icon_path="Assets/svg/sharpness.svg",
      tooltip="Contraste",
      signal=self.sharpness_changed,
      min_value=0,
      max_value=14.0,
      step=1,
      initial_value=user_config.getfloat('CameraSettings', 'sharpness'),
      decimals=0,
      height=30,
      width=30
    )
    _layout.addWidget(self._sharpness_control)

    # -- DEFAULT --
    _default_layout = QHBoxLayout()
    _layout.addLayout(_default_layout)

    self._default_btn = Button(
      icon_path="Assets/svg/default.svg",
      icon_path_hover="Assets/svg/default-hover.svg",
      height=30,
      width=30
    )
    self._default_btn.clicked.connect(self._set_defaults)
    _lbl = QLabel("DEFAULT")
    font = QFont()
    font.setPointSize(11)   # tamaño más grande
    font.setBold(True)   
    _lbl.setFont(font)
    _default_layout.addWidget(self._default_btn)
    _default_layout.addWidget(_lbl)
    _default_layout.setContentsMargins(10, 0, 0, 0)
    _default_layout.setAlignment(Qt.AlignLeft)

  def detect_cameras(self):
    print("Detectando cámaras...")
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

  def camera_selected(self):
    selected_camera = self._cb_cameras.currentIndex()
    self.camera_selected_changed.emit(selected_camera)
    
  @pyqtSlot()
  def _set_defaults(self):
    self._brightness_control.setValue(self._user_defaults.getfloat('CameraSettings', 'brightness'))
    self._contrast_control.setValue(self._user_defaults.getfloat('CameraSettings', 'contrast'))
    self._sharpness_control.setValue(self._user_defaults.getfloat('CameraSettings', 'sharpness'))
    self._gain_control.setValue(self._user_defaults.getfloat('CameraSettings', 'gain'))


  