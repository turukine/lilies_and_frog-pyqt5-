import sys
import random
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter , QColor
from PyQt5.QtWidgets import QApplication, QWidget
import json


with open("data1.json", "r") as f:
    data_loaded = json.load(f)

window_data = data_loaded["window"]
location = window_data[0]["location"]
size = window_data[1]["size"]

color_data = data_loaded["color"]
lilies_color = color_data[0]["lilies"]
frog_color = color_data[1]["frog"]
line_color = color_data[2]["line"]

size_data = data_loaded["size"]
lilies_size = size_data[0]["lilies"]
frog_size = size_data[1]["frog"]

fps = data_loaded["fps"]
speed = data_loaded["speed"]
count_lilies = data_loaded["count_lilies"]

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.lilies = []
        for _ in range(count_lilies): #кол-во кувшинок
            x = random.randint(0, size[0]-lilies_size[0])
            y = random.randint(-1000, -lilies_size[1])
            self.lilies.append((x, y))

        self.x1 = 0
        self.y1 = 0
        self.direction = -1

        self.pred_x1 = self.x1
        self.pred_y1 = self.y1


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(int(1000/fps))


    def initUI(self):
        self.setWindowTitle('Лягушка прыгает по кувшинкам через реку')
        self.setGeometry(location[0], location[1], size[0], size[1])


    def paintEvent(self, event):
        painter_lilies = QPainter(self)
        painter_lilies.setBrush(QColor(*lilies_color))

        for x, y in self.lilies:
            painter_lilies.drawEllipse(x, y, lilies_size[0], lilies_size[1]) #размер кувшинки

        painter_line = QPainter(self)
        painter_line.setBrush(QColor(*line_color))
        painter_line.drawLine(self.pred_x1 + 15, self.pred_y1 + 15, self.x1 + 15, self.y1 + 15)

        painter_frog = QPainter(self)
        painter_frog.setBrush(QColor(*frog_color))
        painter_frog.drawEllipse(self.x1, self.y1, frog_size[0], frog_size[1]) #размер лягушки


    def update_position(self):

        self.pred_x1 = self.x1
        self.pred_y1 = self.y1

        # апдейт лилий
        for i in range(len(self.lilies)):
            x, y = self.lilies[i]
            y += speed
            if y > size[1]:
                x = random.randint(0, size[0]-lilies_size[0])
                y = random.randint(-1000, -lilies_size[1])
            self.lilies[i] = (x, y)

        # апдейт лягушки  + возобновление лилий
        if self.direction == -1:
            x_diffs = [(self.x1 - self.lilies[k][0],k) for k in range(len(self.lilies))
                       if (self.lilies[k][1] > lilies_size[1] // 2) and (self.lilies[k][0] < self.x1)]
        elif self.direction == 1:
            x_diffs = [(self.lilies[k][0] - self.x1, k) for k in range(len(self.lilies))
                        if self.lilies[k][1] > lilies_size[1] and self.lilies[k][0] > self.x1]

        if len(x_diffs) > 0:
            min_diff = min(x_diffs, key=lambda a: a[0])
            self.x1 = self.lilies[min_diff[1]][0]
            self.y1 = self.lilies[min_diff[1]][1]
            new_x = random.randint(0, size[0]-lilies_size[0])
            new_y = random.randint(-1000, -lilies_size[1])
            self.lilies[min_diff[1]] = (new_x, new_y) # удаляем и возобновляем кувшинку
        else:
            if self.direction == -1:
                self.x1 = 0
            elif self.direction == 1:
                self.x1 = size[0]-frog_size[0]

        if self.x1 <= 0 or self.x1 >= size[0]-frog_size[0]:
            self.direction *= -1  # меняем направление

        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())



