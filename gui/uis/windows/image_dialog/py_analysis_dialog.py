from qt_core import *
from gui.widgets import *

class AnalysisDialog(QDialog):
    def __init__(self, images):
        super().__init__()
        self.setWindowTitle("Analysis Dialog")
        self.images = images
        self.point = None

        # Set the default arrow cursor for the dialog
        self.setCursor(Qt.ArrowCursor)

        # Create a layout for the dialog
        layout = QVBoxLayout(self)

        # Create the ImageWidget
        self.image_widget = ImageWidget(self.images)
        print(self.cursor().shape())
        # Set the cursor to a pointing hand when hovering over the ImageWidget
        print("image_widget", self.image_widget.cursor().shape())
        self.image_widget.setCursor(Qt.ArrowCursor)
        # self.image_widget.setCursor(QCursor(Qt.PointingHandCursor))

        layout.addWidget(self.image_widget)

        # Create a slider for changing images
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.images) - 1)
        self.slider.valueChanged.connect(self.change_image)
        layout.addWidget(self.slider)

        # Create a horizontal layout for the "Ok" button
        button_layout = QHBoxLayout()

        # Create the "Ok" button with fixed width
        self.ok_button = QPushButton("Ok")
        self.ok_button.setFixedWidth(100)  # Adjust the width as needed
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setEnabled(False)  # Disable the button initially
        button_layout.addWidget(self.ok_button, Qt.AlignCenter)

        layout.addLayout(button_layout)

        print("image_widget", self.image_widget.cursor().shape())

    def update_clicked_point_label(self, point):
        if point:
            self.point = point
            self.ok_button.setEnabled(True)  # Enable the button when a point is selected
        else:
            self.point = None
            self.ok_button.setEnabled(False)  # Disable the button when no point is selected

    def change_image(self, value):
        point = self.image_widget.clicked_point
        self.image_widget.clear_lines()
        self.image_widget.set_image_index(value)
        self.image_widget.clicked_point = point
        self.image_widget.draw_line()
        # self.update_clicked_point_label(None)

    def accept(self):
        # Custom logic to handle accepted dialog
        # For example, you can retrieve the drawn lines
        # by accessing self.image_widget.line_items
        del self.image_widget
        super().accept()

    def reject(self):
        self.image_widget.clear_lines()
        self.point = None
        super().reject()
