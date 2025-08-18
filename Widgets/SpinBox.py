# Librerias de terceros
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import  QHBoxLayout, QWidget, QDoubleSpinBox

class SpinBox(QWidget):
  
  def __init__(self, icon_path: str, signal: pyqtSignal, tooltip: str = '', width: int = 35,
    height: int = 35, min_value: int = 0, step: float = 0.1, decimals: int = 1, max_value: int = 100, parent: QWidget | None = None):
    super().__init__(parent)
    # --- LAYOUT ---
    self._layout = QHBoxLayout()
    self.setLayout(self._layout)
    # --- SVG ---
    self._svg = QSvgWidget()
    self._svg.load(icon_path)
    self._svg.setFixedSize(width, height)
    self.setToolTip(tooltip)
    self._layout.addWidget(self._svg)
    # --- DOUBLESPINBOX ---
    self._dsp = QDoubleSpinBox()
    self._dsp.setRange(min_value, max_value)
    self._dsp.setDecimals(decimals)    
    self._dsp.setSingleStep(step)
    self._dsp.setAlignment(Qt.AlignRight)
    self._dsp.setFixedWidth(73)
    self._dsp.valueChanged.connect(self._value_changed)
    self._layout.addWidget(self._dsp)
    # --- SIGNAL    
    self._signal = signal
    
  def _value_changed(self):
    value = self._dsp.value()
    self._signal.emit(value)

  def setValue(self, value):
    self._dsp.setValue(value)