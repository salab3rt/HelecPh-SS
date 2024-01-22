import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsOpacityEffect, QLabel, QWidget
from PyQt6.QtCore import Qt, QRect

class CaptureCoords(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Overlay")
        available_geometry = app.primaryScreen().availableGeometry()
        self.setGeometry(available_geometry)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        # Set semi-transparent background
        #self.opacity_effect = QGraphicsOpacityEffect(self)
        #self.opacity_effect.setOpacity(0.5)

        self.overlay_label = QWidget(self)
        self.overlay_label.setGeometry(0, 0, self.width(), self.height())
        self.overlay_label.setStyleSheet("background-color: rgba(0, 0, 0, 128);")
        #self.overlay_label.setGraphicsEffect(self.opacity_effect)

        self.initial_point = None
        self.final_point = None
        self.rect_coords = []
        self.coords = {}

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            
            self.initial_point = event.pos()
            
        if event.button() == Qt.MouseButton.RightButton:

            if len(self.rect_coords) > 0:
                last_drawn_label = self.findChildren(QLabel)
                for label in last_drawn_label[1:]:
                    label.deleteLater()

                self.rect_coords.pop()
                
        self.show_drawn_rectangles()
        
        event.accept()  # Indicate that the event was handled

    def mouseMoveEvent(self, event):
        if event.button() != Qt.MouseButton.RightButton:
            # Update the final point on mouse move
            if self.initial_point:
                self.final_point = event.pos()
                # Draw the rectangle as the cursor moves
                self.draw_rectangle()
        

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Set the final point on mouse release
            self.final_point = event.pos()
            if self.initial_point != self.final_point:
                self.rect_coords.append([self.initial_point, self.final_point])
                self.draw_rectangle()
                self.show_drawn_rectangles()
                
            self.initial_point = None
            self.final_point = None

    def draw_rectangle(self):
        # Clear any existing rectangles
        for label in self.findChildren(QLabel, name='current_rect')[1:]:
            label.deleteLater()
                
        if self.initial_point and self.final_point :
            rect = QRect(self.initial_point, self.final_point)
            # Draw the rectangle using a QLabel
            label = QLabel(self)
            label.setObjectName('current_rect')
            label.setGeometry(rect)
            label.setStyleSheet("border: 2px solid red; background-color: rgba(0, 0, 0, 0);")
            
            label.show()
            
    def show_drawn_rectangles(self):
        #print(self.rect_coords)
        if len(self.rect_coords) > 0:
            for rect in self.rect_coords:
                drawn_rect = QRect(rect[0], rect[1])
                drawn_rect_label = QLabel(self)
                drawn_rect_label.setObjectName('drawn_rects')
                drawn_rect_label.setGeometry(drawn_rect)
                drawn_rect_label.setStyleSheet("border: 2px solid red;")
                drawn_rect_label.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = CaptureCoords()
    overlay.show()
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt and Exception as e:
        if e:
            print(f"Exception: {e}")
    finally:
        app.closeAllWindows()
        sys.exit(app.exit())
