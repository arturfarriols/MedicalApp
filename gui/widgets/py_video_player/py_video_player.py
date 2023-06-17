from qt_core import *

class VideoPlayerView(QWidget):
    def __init__(self, frames):
        super().__init__()
        self.frames = frames
        self.current_frame = 0

        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(frames) - 1)
        self.slider.valueChanged.connect(self.update_frame)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)

    def update_frame(self, value):
        self.current_frame = value
        self.label.setPixmap(self.frames[value].scaledToWidth(400))