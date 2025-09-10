from PyQt5.QtWidgets import QHBoxLayout, QMainWindow,  QWidget
from PyQt5.QtCore import pyqtSlot, QThread
from Camera import Camera
from Threads import CameraWorker
from Components import CameraControls, MainControls
from time import sleep
class MainWindow(QMainWindow):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
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
    layout.addWidget(self._main_controls)
    # ------ CAMERA ------
    self._camera = Camera(self)
    layout.addWidget(self._camera)
    # ----- CAMERA CONTROLS ------
    self._camera_controls = CameraControls(self)
    
    layout.addWidget(self._camera_controls)

    # --- THREAD ---
    self._thread = QThread()
    

    # --- WORKER ---
    self._camera_worker = CameraWorker(0)
    self._camera_worker.moveToThread(self._thread)
    self._camera_worker.change_pixmap_signal.connect(self._camera.update_image)
    self._thread.started.connect(self._camera_worker.run_camera)
    self._thread.start()
    sleep(0.2)
    self._camera_controls.brightness_changed.connect(self._camera_worker.set_brightness)
    self._camera_controls.brightness_changed.connect(self.test)
    self._camera_controls.brightness_changed.connect(self._camera_worker.test)
    self._camera_controls.contrast_changed.connect(self._camera_worker.set_contrast)
    self._camera_controls.gain_changed.connect(self._camera_worker.set_gain)
    self._camera_controls.sharpness_changed.connect(self._camera_worker.set_sharpness)


    # --- WINDOW SETUP ---
    self.setWindowTitle("LaSense Desktop")
    

  @pyqtSlot()
  def _config_show_hide(self):
    if self._camera_controls.isVisible():
      self._main_controls.exit_btn.set_disabled()
      self._main_controls.record_btn.set_disabled()
      self._camera_controls.hide()
    else:
      self._camera_controls.show()
      self._main_controls.exit_btn.set_enabled()
      self._main_controls.record_btn.set_enabled()


  @pyqtSlot()
  def _exit(self):
    self.close()

  def test(self):
    print("AA")

