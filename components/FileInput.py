import os.path

from PySide6.QtCore import QUrl, QSize, QTimer, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QPushButton, QFileDialog

from constant.Types import Image, Video
from util.system import get_home_directory


class FileInput(QWidget):
    MIN_VIEW_SIZE = QSize(480, 270)

    # Videos
    media: QMediaPlayer
    audio: QAudioOutput

    # Images
    image: QLabel

    # Signals
    onChange = Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimumSize(self.MIN_VIEW_SIZE)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # type: ignore
        self.setAcceptDrops(True)

        self.media = QMediaPlayer()
        self.audio = QAudioOutput()
        self.media.setAudioOutput(self.audio)

        self.video = QVideoWidget()
        self.media.setVideoOutput(self.video)
        self.video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # type: ignore
        self.video.setMinimumSize(self.MIN_VIEW_SIZE)
        self.video.hide()

        self.image = QLabel()
        self.image.setScaledContents(True)
        self.image.setMinimumSize(self.MIN_VIEW_SIZE)
        self.image.hide()

        self.button = QPushButton("Open a file")
        self.button.clicked.connect(self.handleClick)
        self.label = QLabel("or\ndrag and drop a file here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        layout.setSpacing(16)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image)
        layout.addWidget(self.video)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def handleClick(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            get_home_directory(),
            "Video Files (*.mp4 *.mkv *.avi *.mov)",
        )
        self.onChange.emit(file_path if file_path else None)
        self.button.hide()
        self.label.hide()

        self._view(file_path)

    def _view(self, url: str | None):
        if not url:
            self.video.hide()
            self.image.hide()
            self.image.setPixmap(QPixmap())
            return

        folder, filename = os.path.split(url)
        _, ext = os.path.splitext(filename)
        ext = ext.lower().strip(".")

        if ext.upper() in [image.value for image in Image]:
            self.media.stop()
            self.video.hide()

            pixmap = QPixmap(url)
            self.image.setPixmap(pixmap)
            self.image.show()
        elif ext.upper() in [video.value for video in Video]:
            self.image.hide()
            self.image.setPixmap(QPixmap())

            self.media.setSource(QUrl.fromLocalFile(url))
            self.media.play()
            self.video.show()
        else:
            # TODO: Add warning message in a dialog perhaps..
            pass
