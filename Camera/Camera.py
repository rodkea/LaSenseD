from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage


class Camera(QWidget):

  

  def __init__(self, parent: QWidget | None = None):
    super().__init__(parent)
    # --- MAIN LAYOUT ---
    _layout = QHBoxLayout()
    self.setLayout(_layout)    
    self._lb_video = QLabel(self)
    self._lb_video.setStyleSheet("background-color: #333; border-radius: 5px;")
    self._lb_video.setAlignment(Qt.AlignCenter)
    _layout.addWidget(self._lb_video, 1)

  @pyqtSlot(QImage)
  def update_image(self, qt_image: QImage):
    pixmap = QPixmap.fromImage(qt_image)
    scaled_pixmap = pixmap.scaled(self._lb_video.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self._lb_video.setPixmap(scaled_pixmap)
