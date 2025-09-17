from PyQt5.QtWidgets import QHBoxLayout, QInputDialog, QMainWindow,  QWidget
from PyQt5.QtCore import pyqtSlot
from Camera import Camera
from Threads import CameraThread, RecordThread
from Components import CameraControls, MainControls
from configparser import ConfigParser
import os

class MainWindow(QMainWindow):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # --- CONFIGS ---
    self.user_config = ConfigParser()
    self.user_config.read('user.config')
    self.default_config = ConfigParser()
    self.default_config.read('default.config')

    # --- CENTRAL WIDGET ---
    
    central_widget = QWidget(self)
    layout = QHBoxLayout()
    central_widget.setLayout(layout)
    self.setCentralWidget(central_widget)

    # --- WIDGETS ---
    # ------ MAIN CONTROLS ------
    self._main_controls = MainControls(self)
    self._main_controls.config_pressed.connect(self._config_show_hide)
    self._main_controls.exit_pressed.connect(self._exit)
    self._main_controls.record_btn.clicked.connect(self._camera_record)
    self._main_controls.stop_btn.clicked.connect(self._camera_stop_record)
    layout.addWidget(self._main_controls)
    # ------ CAMERA ------
    self._camera = Camera(self)
    layout.addWidget(self._camera, 1)
    # ----- CAMERA CONTROLS ------
    self._camera_controls = CameraControls(self, user_defaults=self.default_config, user_config=self.user_config)
    self._camera_controls.detect_cameras_pressed.connect(self._stop_camera_thread)
    self._camera_controls.camera_selected_changed.connect(self.create_camera_thread)    
    self._camera_controls.hide()
    layout.addWidget(self._camera_controls)

    # --- THREAD ---
    self._camera_thread = None
    self._record_thread = None

        


    # --- WINDOW SETUP ---
    self.setWindowTitle("LaSense Desktop")
    try:
      self.create_camera_thread(0)
    except:
      pass

  @pyqtSlot()
  def _config_show_hide(self):
    if self._camera_controls.isVisible():
      self._main_controls.exit_btn.set_enabled()
      self._main_controls.record_btn.set_enabled()
      self._main_controls.analyze_btn.set_enabled()
      self._camera_controls.hide()
    else:
      self._camera_controls.show()
      self._main_controls.exit_btn.set_disabled()
      self._main_controls.record_btn.set_disabled()
      self._main_controls.analyze_btn.set_disabled()

  


  @pyqtSlot()
  def _exit(self):
    self.close()

  @pyqtSlot(int)
  def create_camera_thread(self, index : int):
    if self._camera_thread is not None:
      self._camera_thread.stop()
    self._camera_thread = CameraThread(index)
    self._camera_thread.change_pixmap_signal.connect(self._camera.update_image)
    self._camera_controls.brightness_changed.connect(self._camera_thread.set_brightness)
    self._camera_thread.set_brightness(self.user_config.getfloat('CameraSettings', 'brightness'))
    self._camera_controls.brightness_changed.connect(self._update_user_brightness)
    self._camera_controls.contrast_changed.connect(self._camera_thread.set_contrast)
    self._camera_thread.set_contrast(self.user_config.getfloat('CameraSettings', 'contrast'))
    self._camera_controls.contrast_changed.connect(self._update_user_contrast)
    self._camera_controls.gain_changed.connect(self._camera_thread.set_gain)
    self._camera_thread.set_gain(self.user_config.getfloat('CameraSettings', 'gain'))
    self._camera_controls.gain_changed.connect(self._update_user_gain)
    self._camera_controls.sharpness_changed.connect(self._camera_thread.set_sharpness)    
    self._camera_thread.set_sharpness(self.user_config.getfloat('CameraSettings', 'sharpness')) 
    self._camera_controls.sharpness_changed.connect(self._update_user_sharpness)
    self._camera_thread.start()

  @pyqtSlot()
  def _stop_camera_thread(self):
    if self._camera_thread is not None:
      self._camera_thread.stop()
    self._camera_controls.detect_cameras()

  def _update_user_brightness(self, value: float):
    self.user_config.set('CameraSettings', 'brightness', str(value))
    with open('user.config', 'w') as configfile:
      self.user_config.write(configfile)
  
  def _update_user_contrast(self, value: float):
    self.user_config.set('CameraSettings', 'contrast', str(value))
    with open('user.config', 'w') as configfile:
      self.user_config.write(configfile)
  
  def _update_user_gain(self, value: float):
    self.user_config.set('CameraSettings', 'gain', str(value))
    with open('user.config', 'w') as configfile:
      self.user_config.write(configfile)

  def _update_user_sharpness(self, value: float):
    self.user_config.set('CameraSettings', 'sharpness', str(value))
    with open('user.config', 'w') as configfile:
      self.user_config.write(configfile)

  def _camera_record(self):
    self._main_controls.config_btn.set_disabled()
    self._main_controls.exit_btn.set_disabled()
    self._main_controls.analyze_btn.set_disabled()
    if self._camera_thread and not self._record_thread:
      filename, ok = QInputDialog.getText(self, 'Nombre del archivo', 'Ingrese el nombre del archivo:')
      if ok and filename:
        self._camera_thread.record()
        try:
          root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
          data_dir = os.path.join(root_dir, 'data')
          os.makedirs(data_dir, exist_ok=True)
        except OSError as e:
          print(f"Error creando el directorio de datos '{data_dir}': {e}")
        self._record_thread = RecordThread(filename=filename, queue=self._camera_thread.queue, resolution=(480,640))
        self._record_thread.start()
      else:
          self._main_controls.config_btn.set_enabled()
          self._main_controls.exit_btn.set_enabled()
          self._main_controls.analyze_btn.set_enabled()
          self._main_controls.record_btn.show()
          self._main_controls.stop_btn.hide()






  def _camera_stop_record(self):
    if self._camera_thread and self._record_thread:
      self._camera_thread.stop_record()
      self._record_thread.stop()
    self._main_controls.config_btn.set_enabled()
    self._main_controls.exit_btn.set_enabled()
    self._main_controls.analyze_btn.set_enabled()