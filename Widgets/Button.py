from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor


class Button(QSvgWidget):

    """
    Button is a custom widget that displays an SVG icon and supports hover effects and click events.
    It can be enabled or disabled, and its appearance changes accordingly.

    Attributes:
    ----------
    _is_enabled : bool
        Indicates whether the button is currently enabled or disabled.
    _signal : pyqtSignal | None
        The signal to be emitted when the button is clicked, if provided.
    _icon_path : str
        The file path to the default SVG icon.
    _icon_path_hover : str
        The file path to the SVG icon displayed when the button is hovered.
    _icon_path_disabled : str
        The file path to the SVG icon displayed when the button is disabled.

    Methods:
    -------
    __init__(icon_path: str, icon_path_hover: str | None = None, icon_path_disabled: str | None = None,
             enabled: bool = True, width: int = 25, height: int = 25, signal: pyqtSignal | None = None,
             parent: QWidget | None = None):
        Initializes the Button with specified icon paths, size, and optional signal.

    is_enabled() -> bool:
        Returns whether the button is currently enabled.

    enterEvent(event):
        Changes the cursor and icon when the mouse enters the button.

    leaveEvent(event):
        Restores the cursor and icon when the mouse leaves the button.

    mousePressEvent(event):
        Emits the signal if the button is clicked and enabled.

    set_enabled():
        Enables the button and loads the default icon.

    set_disabled():
        Disables the button and loads the disabled icon, if provided.
    """

    clicked = pyqtSignal()

    def __init__(self, icon_path: str,
                 icon_path_hover: str | None = None,
                 icon_path_disabled: str | None = None,
                 enabled: bool = True,
                 width: int = 25, height: int = 25,
                 signal: pyqtSignal | None = None,                 
                 parent: QWidget | None = None):
        """Creates a Button with an SVG icon.
        Args:
            signal (Signal): _description_
            icon_path (str): Path to the default svg image            
            icon_path_hover (str | None, optional): Path to the hover svg image. Defaults to None.
            icon_path_disabled (str | None, optional): Path to the disabled svg image. Defaults to None.
            width (int, optional): width in pixels of the button. Defaults to 25.
            height (int, optional): heigh in pixels of the button. Defaults to 25.
            parent (QWidget | None, optional): Defaults to None.
        """
        super().__init__(parent)
        self.setFixedSize(width, height)
        self._is_enabled = enabled        
        self._signal = signal
        # ICON PATHS
        self._icon_path = icon_path
        if icon_path_hover:
            self._icon_path_hover = icon_path_hover
        else:
            self._icon_path_hover = icon_path
        if icon_path_disabled:
            self._icon_path_disabled = icon_path_disabled
        else:
            self._icon_path_disabled = icon_path
        # SET ICON
        if self.is_enabled:
            self.load(self._icon_path)
        else:
            self.load(self._icon_path_disabled)

    @property
    def is_enabled(self):
        return self._is_enabled

    def enterEvent(self, event):
        # Cambiar el cursor cuando el mouse entra al widget
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if self.is_enabled:
            self.load(self._icon_path_hover)  # CAMBIA EL SVG AL AZUL
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Restaurar el cursor cuando el mouse sale del widget
        self.setCursor(QCursor(Qt.ArrowCursor))
        if self.is_enabled:
            self.load(self._icon_path)  # CAMBIA EL SVG AL DEFAULT
        else:
            self.load(self._icon_path_disabled)
        super().leaveEvent(event)
        

    def mousePressEvent(self, event):
        # Manejar el evento de click
        if event.button() == Qt.LeftButton:
            if self.is_enabled:
                self._signal.emit()
        super().mousePressEvent(event)

    def set_enabled(self):
        self._is_enabled = True
        self.load(self._icon_path)

    def set_disabled(self):
        self._is_enabled = False
        if self._icon_path_disabled:
            self.load(self._icon_path_disabled)
        else:
            self.load(self._icon_path)