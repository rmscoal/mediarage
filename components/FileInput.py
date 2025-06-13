import os.path

from PySide6.QtCore import QUrl, QSize, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QPushButton, QFileDialog

from constant.File import File, Image, Video
from util.system import get_home_directory


class FileInput(QWidget):
    MIN_VIEW_SIZE = QSize(680, 380)
    MIN_PLAYER_SIZE = QSize(480, 270)

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
        self.video.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  # type: ignore
        self.video.setFixedSize(self.MIN_PLAYER_SIZE)
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
        if File.from_path(file_path) is None:
            # TODO: Handle if file type is not supported
            return

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

        _, filename = os.path.split(url)
        _, ext = os.path.splitext(filename)
        ext = ext.upper().strip(".")

        file_type = File.from_str(ext)
        if isinstance(file_type, Image):
            self.media.stop()
            self.video.hide()

            pixmap = QPixmap(url)
            self.image.setPixmap(pixmap)
            self.image.show()
        elif isinstance(file_type, Video):
            self.image.hide()
            self.image.setPixmap(QPixmap())

            self.media.setSource(QUrl.fromLocalFile(url))
            self.media.play()
            self.video.show()
        else:
            # TODO: Add warning dialog
            pass
