from qt_core import *
from gui.widgets import *

class AnalysisDialog(QDialog):
    def __init__(self, images):
        super().__init__()
        self.setWindowTitle("Analysis Dialog")
        self.images = images
        self.point = None
        self.is_automatic = None

        # Create a layout for the dialog
        layout = QVBoxLayout(self)

        # Create the ImageWidget
        self.image_widget = ImageWidget(self.images)
        layout.addWidget(self.image_widget)

        # Create a label widget to display the clicked point
        self.clicked_point_label = QLabel()
        layout.addWidget(self.clicked_point_label)

        # Create the button layout
        button_layout = QHBoxLayout()

        # Create the "Ok" button
        self.ok_button = QPushButton("Ok")
        # self.ok_button.clicked.connect(self.accept(False))
        self.ok_button.clicked.connect(lambda: self.accept(False))
        # self.btn_3.clicked.connect(lambda: self.button_clicked(self.btn_3.id, [self.table_widget]))
        self.ok_button.setEnabled(False)  # Disable the button initially
        button_layout.addWidget(self.ok_button)

        # Create the "Automatic" button
        automatic_button = QPushButton("Automatic")
        automatic_button.clicked.connect(lambda: self.accept(True))
        button_layout.addWidget(automatic_button)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # Create a slider for changing images
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.images) - 1)
        self.slider.valueChanged.connect(self.change_image)
        layout.addWidget(self.slider)

    def update_clicked_point_label(self, point):
        if point:
            self.clicked_point_label.setText(f"Clicked Point: ({point.x()}, {point.y()})")
            self.point = point
            self.ok_button.setEnabled(True)  # Enable the button when a point is selected
        # else:
        #     self.clicked_point_label.setText("")
        #     # self.point = None
        #     # self.ok_button.setEnabled(False)  # Disable the button when no point is selected

    def change_image(self, value):
        point = self.image_widget.clicked_point
        self.image_widget.clear_lines()
        self.image_widget.set_image_index(value)
        self.image_widget.clicked_point = point
        self.image_widget.draw_line()
        self.update_clicked_point_label(None)

    def accept(self, is_automatic):
        # Custom logic to handle accepted dialog
        # For example, you can retrieve the drawn lines
        # by accessing self.image_widget.line_items
        self.is_automatic = is_automatic
        del self.image_widget
        super().accept()

    def reject(self):
        self.image_widget.clear_lines()
        super().reject()