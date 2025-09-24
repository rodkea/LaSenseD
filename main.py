import sys
from Windows import MainWindow
from PyQt5.QtWidgets import QApplication,  QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from utils import ROOT_DIR

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
  app = QApplication(sys.argv)
  
  img_path = os.path.join(ROOT_DIR, "Assets", "jpg", "LaSense.jpg")
  splash_pix = QPixmap(img_path)
  splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
  splash.show()
  w = MainWindow()
  splash.finish(w)
  w.showMaximized()
  sys.exit(app.exec_())