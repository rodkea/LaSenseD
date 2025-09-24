from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from Widgets import Button
from utils import ASSETS_DIR
import os
class MainControls(QWidget):
    
    config_pressed = pyqtSignal()
    exit_pressed = pyqtSignal()
    
    def __init__(self, parent=None):
      super().__init__(parent)
      _layout = QVBoxLayout(self)
      _layout.setSpacing(15)
      _layout.setAlignment(Qt.AlignCenter)
      self.setLayout(_layout)

      # -- RECORD --
      self.record_btn = Button(
        icon_path=os.path.join(ASSETS_DIR, "svg", "record.svg"),
        icon_path_hover=os.path.join(ASSETS_DIR, "svg", "record-hover.svg"),
        icon_path_disabled=os.path.join(ASSETS_DIR, "svg", "record-disabled.svg"),
        height=30,
        width=30      
      )      
      _layout.addWidget(self.record_btn, 0)
      # -- STOP --
      self.stop_btn = Button(
        icon_path=os.path.join(ASSETS_DIR, "svg", "stop.svg"),
        icon_path_hover=os.path.join(ASSETS_DIR, "svg", "stop-hover.svg"),
        height=30,
        width=30
      )
      self.stop_btn.hide()
      _layout.addWidget(self.stop_btn, 0)
      # -- ANALYZE --
      self.analyze_btn = Button(
        icon_path=os.path.join(ASSETS_DIR, "svg", "ml.svg"),
        icon_path_hover=os.path.join(ASSETS_DIR, "svg", "ml-hover.svg"),
        icon_path_disabled=os.path.join(ASSETS_DIR, "svg", "ml-disabled.svg"),
        height=30,
        width=30,        
      )
      _layout.addWidget(self.analyze_btn, 0)
      # -- CONFIG --
      self.config_btn = Button(
        icon_path=os.path.join(ASSETS_DIR, "svg", "config.svg"),
        icon_path_hover=os.path.join(ASSETS_DIR, "svg", "config-hover.svg"),
        icon_path_disabled=os.path.join(ASSETS_DIR, "svg", "config-disabled.svg"),
        height=30,
        width=30,
        signal=self.config_pressed
      )
      _layout.addWidget(self.config_btn, 0)
      self.exit_btn = Button(
        icon_path=os.path.join(ASSETS_DIR, "svg", "exit.svg"),
        icon_path_hover=os.path.join(ASSETS_DIR, "svg", "exit-hover.svg"),
        icon_path_disabled=os.path.join(ASSETS_DIR, "svg", "exit-disabled.svg"),
        height=30,
        width=30,
        signal=self.exit_pressed
        )
      
      _layout.addWidget(self.exit_btn, 0)


    