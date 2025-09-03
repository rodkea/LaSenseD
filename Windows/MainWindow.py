
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QMainWindow, QPushButton, QWidget
from Camera import Camera
from Components import CameraControls, MainControls
class MainWindow(QMainWindow):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # --- CENTRAL WIDGET ---
    central_widget = QWidget(self)
    layout = QHBoxLayout()
    central_widget.setLayout(layout)
    self.setCentralWidget(central_widget)

    # --- WIDGETS ---
    main_controls = MainControls(self)
    layout.addWidget(main_controls)

    self._camera = Camera(self)
    layout.addWidget(self._camera)
    
    camera_controls = CameraControls(self)
    layout.addWidget(camera_controls)

    # --- WINDOW SETUP ---
    self.setWindowTitle("LaSense Desktop")
    
