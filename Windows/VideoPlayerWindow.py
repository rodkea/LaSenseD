import numpy as np
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import os
import re
from descriptors import d_fuzzy

class VideoPlayerWindow(QDialog):
    def __init__(self, filepath, parent=None):
        super().__init__(parent)
        self.setWindowTitle(os.path.basename(filepath))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setLayout(QVBoxLayout())
        self.resize(800, 600)

        self._video_data = None
        self._current_frame = 0
        self._num_frames = 0
        
        self.exit_button = QPushButton("Exit")
        self.layout().addWidget(self.exit_button)
        self.exit_button.clicked.connect(self.close)

        self.load_video(filepath)     

    def load_video(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                header_line = f.readline().decode('utf-8')
                
                resolution_match = re.search(r"Resolution:\s*\((\d+),\s*(\d+)\)", header_line)
                frames_match = re.search(r"NumberOfFrames:\s*(\d+)", header_line)

                if not resolution_match or not frames_match:
                    print(f"Error: Invalid header format in {filepath}")
                    return

                height = int(resolution_match.group(1))
                width = int(resolution_match.group(2))
                self._num_frames = int(frames_match.group(1))

                raw_data = f.read()
                
                expected_bytes = self._num_frames * height * width
                if len(raw_data) < expected_bytes:
                    self._num_frames = len(raw_data) // (height * width)

                self._video_data = np.frombuffer(raw_data, dtype=np.uint8).reshape((self._num_frames, height, width))
                print(self._video_data.shape)
                qt = d_fuzzy(self._video_data)
                print(f"media {np.mean(qt)}")
        except Exception as e:
            print(f"Failed to load video file: {e}")