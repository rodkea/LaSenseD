from PyQt5.QtWidgets import QComboBox,  QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QFont
from Threads import CameraThread
import cv2
from Widgets import Button, SpinBox
import os
from configparser import ConfigParser
import time
class Camera(QWidget):

  brightness_changed = pyqtSignal(float)
  contrast_changed = pyqtSignal(float)
  gain_changed = pyqtSignal(float)
  sharpness_changed = pyqtSignal(float)


  def __init__(self, parent: QWidget | None = None):
    super().__init__(parent)
    # --- MAIN LAYOUT ---
    main_layout = QHBoxLayout()
    self.setLayout(main_layout)
    # --- MAIN CONTROLS ---
    main_controls_layout = QVBoxLayout()
    main_layout.addLayout(main_controls_layout)
    self._record_btn = Button(
      icon_path="Assets/svg/record.svg",
      icon_path_hover="Assets/svg/record-hover.svg",
      icon_path_disabled="Assets/svg/record-disabled.svg",
      height=30,
      width=30      
    )
    main_controls_layout.addWidget(self._record_btn, 0)
    # CONFIG
    self._config_btn = Button(
      icon_path="Assets/svg/config.svg",
      icon_path_hover="Assets/svg/config-hover.svg",
      icon_path_disabled="Assets/svg/config-disabled.svg",
      height=30,
      width=30  
    )
    self._config_btn.clicked.connect(self.show_config_controls)
    main_controls_layout.addWidget(self._config_btn, 0)

    # EXIT
    self._exit_btn = Button(
      icon_path="Assets/svg/exit.svg",
      icon_path_hover="Assets/svg/exit-hover.svg",
      icon_path_disabled="Assets/svg/exit-disabled.svg",
      height=30,
      width=30
    )
    self._exit_btn.clicked.connect((QApplication.instance().quit))
    main_controls_layout.addWidget(self._exit_btn, 0)
 

    
    
    self._lb_video = QLabel(self)
    self._lb_video.setStyleSheet("background-color: #333; border-radius: 5px;")
    self._lb_video.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(self._lb_video, 1)
    self._config = ConfigParser()
    self._config.read('user.config')
    self._default = ConfigParser()
    self._default.read('default.config')
    


    # --- CONTROLES ---
    self._controls_layout = QVBoxLayout()
    main_layout.addLayout(self._controls_layout)
    # ------ CAMERA SELECT -------
    cameras_layout = QHBoxLayout()
    self._controls_layout.addLayout(cameras_layout)
    self._controls_layout.setContentsMargins(0,20,0,0)
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
      min_value=0.0,
      max_value=1023.0,
      step=1,
      decimals=0,
      signal=self.brightness_changed,
      height=30,
      width=30           
    )
    self._controls_layout.addWidget(self._brightness_control)
    # ------ CONTRAST -------
    self._contrast_control = SpinBox(
      icon_path="Assets/svg/contrast.svg",
      tooltip="Contraste",
      signal=self.contrast_changed,      
      min_value=-10,
      max_value=30.0,
      step=1,
      decimals=0,
      height=23,
      width=23,        
    )
    self._controls_layout.addWidget(self._contrast_control)

    # ------ GAIN -------
    self._gain_control = SpinBox(
      icon_path="Assets/svg/iso.svg",
      tooltip="Ganancia",
      signal=self.gain_changed,      
      min_value=0,
      max_value=1956,
      step=1,
      decimals=0,
      height=30,
      width=30,        
    )
    self._controls_layout.addWidget(self._gain_control)

    # ------ SHARPNESS -------
    self._sharpness_control = SpinBox(
      icon_path="Assets/svg/sharpness.svg",
      tooltip="Nitidez",
      signal=self.sharpness_changed,      
      min_value=0,
      max_value=14,
      step=1,
      decimals=0,
      height=30,
      width=30,        
    )
    self._controls_layout.addWidget(self._sharpness_control)

        #------- DEFAULT ---------
    _default_layout = QHBoxLayout()
    self._controls_layout.addLayout(_default_layout)

    self._default_btn = Button(
      icon_path="Assets/svg/default.svg",
      icon_path_hover="Assets/svg/default-hover.svg",
      height=30,
      width=30
    )
    _lbl = QLabel("DEFAULT")
    font = QFont()
    font.setPointSize(11)   # tamaño más grande
    font.setBold(True)   
    _lbl.setFont(font)
    self._default_btn.clicked.connect(self.set_default_settings)
    _default_layout.addWidget(self._default_btn)
    _default_layout.addWidget(_lbl)
    _default_layout.setContentsMargins(10, 0, 0, 0)
    _default_layout.setAlignment(Qt.AlignLeft)

    self._controls_layout.setAlignment(Qt.AlignTop)

    self._thread = None
    self.detect_cameras()
    self.brightness_changed.connect(self.set_brightness)
    self.contrast_changed.connect(self.set_contrast)
    self.gain_changed.connect(self.set_gain)
    self.sharpness_changed.connect(self.set_sharpness)
    
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
    self._thread.start()
    time.sleep(0.2)
    self._brightness_control.setValue(self._config.getfloat('CameraSettings', 'brightness'))
    self.set_brightness(self._config.getfloat('CameraSettings', 'brightness'))
    self._contrast_control.setValue(self._config.getfloat('CameraSettings', 'contrast'))
    self.set_contrast(self._config.getfloat('CameraSettings', 'contrast'))    
    self._gain_control.setValue(self._config.getfloat('CameraSettings', 'gain'))
    self.set_gain(self._config.getfloat('CameraSettings', 'gain'))
    self._sharpness_control.setValue(self._config.getfloat('CameraSettings', 'sharpness'))
    self.set_sharpness(self._config.getfloat('CameraSettings', 'sharpness'))
    self._thread.change_pixmap_signal.connect(self.update_image)

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

  @pyqtSlot(QImage)
  def update_image(self, qt_image: QImage):
    pixmap = QPixmap.fromImage(qt_image)
    scaled_pixmap = pixmap.scaled(self._lb_video.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self._lb_video.setPixmap(scaled_pixmap)
  
  @pyqtSlot(float)
  def set_brightness(self, value: float):
    if self._thread and self._thread.isRunning():
      self._thread.set_brightness(value)
      self._save_setting('brightness', value)

  @pyqtSlot(float)
  def set_contrast(self, value: float):
    if self._thread and self._thread.isRunning():
      self._thread.set_contrast(value)
      self._save_setting('contrast', value)
  
  @pyqtSlot(float)
  def set_gain(self, value: float):
    if self._thread and self._thread.isRunning():
      self._thread.set_gain(value)
      self._save_setting('gain', value)


  @pyqtSlot(float)
  def set_sharpness(self, value: float):
    if self._thread and self._thread.isRunning():
      self._thread.set_sharpness(value)
      self._save_setting('sharpness', value)


  def closeEvent(self, event):
    if self._thread is not None:
      self._thread.stop()
    event.accept()

  def _save_setting(self, key: str, value):
      """Guarda una clave y valor en la sección [CameraSettings] de user.config."""
      self._config.set('CameraSettings', key, str(value))
      with open('user.config', 'w') as configfile:
        self._config.write(configfile)

  def set_default_settings(self):
    self._brightness_control.setValue(self._default.getfloat('CameraSettings', 'brightness'))
    self._contrast_control.setValue(self._default.getfloat('CameraSettings', 'contrast'))
    self._gain_control.setValue(self._default.getfloat('CameraSettings', 'gain'))
    self._sharpness_control.setValue(self._default.getfloat('CameraSettings', 'sharpness'))

  def show_config_controls(self):
    if self._contrast_control.isVisible():      
      self._controls_layout.show()
    else:
      self._controls_layout.hide()