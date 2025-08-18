
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QMainWindow, QPushButton, QWidget
from Camera import Camera

class MainWindow(QMainWindow):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # --- CENTRAL WIDGET ---
    central_widget = QWidget(self)
    layout = QHBoxLayout()
    central_widget.setLayout(layout)
    self.setCentralWidget(central_widget)

    # --- WIDGETS ---
    self._camera = Camera(self)
    layout.addWidget(self._camera)
    
    # --- WINDOW SETUP ---
    self.setWindowTitle("La Sense")
