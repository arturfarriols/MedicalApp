from qt_core import *
import numpy as np

class ImageWidget(QGraphicsView):
    def __init__(self, images):
        super().__init__()
        self.images = images
        self.image_index = 0
        self.clicked_point = None
        self.line_items = []
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setInteractive(True)
        self.zoom_factor = 1.0
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.load_image()

    def load_image(self):
        image = self.images[self.image_index]
        print(type(image))
        image = np.ascontiguousarray(image)
        height, width, channels = image.shape
        bytes_per_line = channels * width
        image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.scene.addPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked_point = event.pos()
            self.draw_line()
            self.parent().update_clicked_point_label(self.clicked_point)

    def draw_line(self):
        self.clear_lines()
        pen = QPen(QColor("yellow"))
        pen.setStyle(Qt.DotLine)
        pos = self.mapToScene(self.clicked_point)
        x = pos.x()
        line = QGraphicsLineItem(x, 0, x, self.height())
        line.setPen(pen)
        self.scene.addItem(line)
        self.line_items.append(line)

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        # Check if zooming out will make the image smaller than the view
        if self.zoom_factor * zoom_factor < 0.9 or self.zoom_factor * zoom_factor > 2.5:
            return

        self.zoom_factor *= zoom_factor
        self.scale(zoom_factor, zoom_factor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
            self.zoom_in()
        elif event.key() == Qt.Key_Minus or event.key() == Qt.Key_Underscore:
            self.zoom_out()

    def zoom_in(self):
        self.zoom_factor *= 1.25
        self.scale(1.25, 1.25)

    def zoom_out(self):
        self.zoom_factor *= 0.8
        self.scale(0.8, 0.8)

    def set_image_index(self, index):
        self.image_index = index
        self.scene.clear()
        self.load_image()
        self.clicked_point = None

    def clear_lines(self):
        print(len(self.line_items))
        for line in self.line_items:
            print('deleting')
            self.scene.removeItem(line)
            print('deleted')
        self.line_items.clear()