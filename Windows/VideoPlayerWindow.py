import numpy as np
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout
from Widgets import MplCanvas
from PyQt5.QtCore import Qt
import os

import numpy as np



class VideoPlayerWindow(QDialog):
    def __init__(self, medio: str, median: str, qt: np.ndarray, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DFUZZY ANALISIS")        
        self.setLayout(QVBoxLayout())
        self.resize(650, 500)
        self._canvas = MplCanvas()
        cax = self._canvas.axes.imshow(qt, cmap='viridis')
        self._canvas.cb = self._canvas.figure.colorbar(cax, ax=self._canvas .axes)
        self._canvas.draw()
        self._current_frame = 0
        self._num_frames = 0
        
        self.layout().addWidget(self._canvas)
        _stats_layout = QHBoxLayout()
        _mean_lb = QLabel(f"Media: {medio:.4f}")
        _median_lb = QLabel(f"Mediana: {median:.4f}")
        _stats_layout.addWidget(_mean_lb)
        _stats_layout.addWidget(_median_lb)
        self.layout().addLayout(_stats_layout)


        
                
