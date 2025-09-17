from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from .VideoPlayerWindow import VideoPlayerWindow
import os

class AnalyzeWindow(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Analizar Videos")
    self.setModal(True)
    self.setLayout(QVBoxLayout())
    self.file_list = QListWidget()
    self.layout().addWidget(self.file_list)
    self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    self.populate_files()
    button_layout = QHBoxLayout()
    self.analyze_button = QPushButton("Analizar")
    self.exit_button = QPushButton("Salir")
    button_layout.addWidget(self.analyze_button)
    button_layout.addWidget(self.exit_button)
    self.layout().addLayout(button_layout)
    self.exit_button.clicked.connect(self.close)
    self.analyze_button.clicked.connect(self.analyze_video)

  def populate_files(self):
    self.videos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/videos"))
    if not os.path.exists(self.videos_dir):
      os.makedirs(self.videos_dir)
      
    for f in os.listdir(self.videos_dir):
      if f.endswith('.ls'):
        self.file_list.addItem(f)

  def analyze_video(self):
        selected_item = self.file_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No selection", "Please select a file to analyze.")
            return
            
        filename = selected_item.text()
        filepath = os.path.join(self.videos_dir, filename)
        
        self.accept() # Cierra la ventana actual con estado de "aceptado"
        self._video_player = VideoPlayerWindow(filepath, self.parent())
        self._video_player.exec_()