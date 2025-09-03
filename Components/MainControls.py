from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt
from Widgets import Button

class MainControls(QWidget):
    
    def __init__(self, parent=None):
      super().__init__(parent)
      _layout = QVBoxLayout(self)
      _layout.setSpacing(15)
      _layout.setAlignment(Qt.AlignCenter)
      self.setLayout(_layout)

      # -- RECORD --
      self._record_btn = Button(
        icon_path="Assets/svg/record.svg",
        icon_path_hover="Assets/svg/record-hover.svg",
        icon_path_disabled="Assets/svg/record-disabled.svg",
        height=30,
        width=30      
      )
      _layout.addWidget(self._record_btn, 0)
      # -- CONFIG --
      self._config_btn = Button(
        icon_path="Assets/svg/config.svg",
        icon_path_hover="Assets/svg/config-hover.svg",
        icon_path_disabled="Assets/svg/config-disabled.svg",
        height=30,
        width=30  
      )
      _layout.addWidget(self._config_btn, 0)
      self._exit_btn = Button(
        icon_path="Assets/svg/exit.svg",
        icon_path_hover="Assets/svg/exit-hover.svg",
        icon_path_disabled="Assets/svg/exit-disabled.svg",
        height=30,
        width=30
        )
      self._exit_btn.clicked.connect((QApplication.instance().quit))
      _layout.addWidget(self._exit_btn, 0)


    