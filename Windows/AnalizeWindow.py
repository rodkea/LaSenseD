from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QMessageBox, QLabel
from PyQt5.QtCore import Qt
import os
from .VideoPlayerWindow import VideoPlayerWindow
import numpy as np
from Threads import AnalyzeThread


class AnalyzeWindow(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Analizar Videos")
    self.setModal(True)
    self.setLayout(QVBoxLayout())
    self._analyze_layout = QVBoxLayout()
    self._lb_video = QLabel()
    self._lb_video.setAlignment(Qt.AlignCenter)
    self._lb_video.setFixedHeight(200)
    self._lb_video.setStyleSheet("background-color: #333; border-radius: 5px;")
    self._lb_video.hide()
    self.layout().addWidget(self._lb_video)
    self.file_list = QListWidget()
    self.layout().addWidget(self.file_list)
    self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    self.populate_files()
    button_layout = QHBoxLayout()
    self.analyze_button = QPushButton("Analizar")
    self.delete_button = QPushButton("Borrar")
    self.exit_button = QPushButton("Salir")
    button_layout.addWidget(self.analyze_button)
    button_layout.addWidget(self.delete_button)
    self.layout().addLayout(button_layout)
    self._analyze_thread = None
    
    
    self.analyze_button.clicked.connect(self.analyze_video)
    self.delete_button.clicked.connect(self.delete_video)

  def populate_files(self):
    self.file_list.clear()
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
        self._analyze_thread = AnalyzeThread(filepath)
        self._analyze_thread.finish.connect(self._finish)
        self._analyze_thread.start()
        
  def _finish(self, qt: np.ndarray, mean: float, median: float):
    d_fuzzy = VideoPlayerWindow(mean, median, qt)
    d_fuzzy.exec_()
    self._analyze_thread = None



  def delete_video(self):
    selected_item = self.file_list.currentItem()
    if not selected_item:
        QMessageBox.warning(self, "Sin selección", "Por favor, selecciona un archivo para borrar.")
        return

    filename = selected_item.text()
    filepath = os.path.join(self.videos_dir, filename)

    reply = QMessageBox.question(self,
              'Confirmar borrado', f"¿Estás seguro de que quieres borrar {filename}?",
              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        try:
            os.remove(filepath)
            self.populate_files() # Recarga la lista de archivos
            QMessageBox.information(self, "Borrado", f"El archivo {filename} ha sido borrado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo borrar el archivo: {e}")