import sys
import random
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QTableWidget, \
    QTableWidgetItem, QHBoxLayout, QSpacerItem, QSizePolicy
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


class Frog:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = -1  # Начальное направление
        self.prev_x = x  # Предыдущая позиция по x
        self.prev_y = y  # Предыдущая позиция по y
        self.distance_traveled = 0
        self.jump_count = 0
        self.drowned_lilies = 0
        self.last_jump_distance = 0


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.lilies = []
        self.create_lilies(count_lilies)

        self.frogs = [Frog(0, 0)]  # Начинаем с одной лягушки

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(int(1000 / fps))

        self.is_paused = False

    def initUI(self):
        self.setWindowTitle('Лягушка прыгает по кувшинкам через реку')
        self.setGeometry(location[0], location[1], size[0], size[1])

        layout = QVBoxLayout()

        # Элементы управления
        control_layout = QVBoxLayout()

        # Метки
        self.speed_label = QLabel(f"Скорость течения: {speed}")  # Метка скорости
        control_layout.addWidget(self.speed_label)

        self.frequency_label = QLabel(f"Частота появления кувшинок: {count_lilies}")  # Метка частоты
        control_layout.addWidget(self.frequency_label)

        # Макет для слайдеров и кнопок
        slider_button_layout = QVBoxLayout()

        # Слайдеры
        self.speed_slider = QSlider()
        self.speed_slider.setOrientation(1)
        self.speed_slider.setRange(20, 100)
        self.speed_slider.setValue(speed)
        self.speed_slider.valueChanged.connect(self.change_speed)
        slider_button_layout.addWidget(self.speed_slider)

        self.frequency_slider = QSlider()
        self.frequency_slider.setOrientation(1)
        self.frequency_slider.setRange(5, 20)
        self.frequency_slider.setValue(count_lilies)
        self.frequency_slider.valueChanged.connect(self.change_frequency)
        slider_button_layout.addWidget(self.frequency_slider)

        # Кнопки
        self.add_frog_button = QPushButton("Добавить лягушку")  # Кнопка для добавления лягушек
        self.add_frog_button.clicked.connect(self.add_frog)
        slider_button_layout.addWidget(self.add_frog_button)

        self.pause_button = QPushButton("Пауза")  # Кнопка для паузы
        self.pause_button.clicked.connect(self.toggle_pause)
        slider_button_layout.addWidget(self.pause_button)

        control_layout.addLayout(slider_button_layout)

        # Добавляем спейсер
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        control_layout.addItem(spacer)

        layout.addLayout(control_layout)

        # Таблица с инф. о лягушках
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(
            ["Координаты", "Утонувшие кувшинки", "Расстояние", "Среднее расстояние", "Переправы"])

        # Устанавливаем фиксированную высоту таблицы
        self.table_widget.setFixedHeight(150)  # Установите нужную высоту

        # Уменьшаем размер шрифта таблицы
        font = QFont()
        font.setPointSize(10)  # Установите нужный размер шрифта
        self.table_widget.setFont(font)

        layout.addWidget(self.table_widget)

        self.setLayout(layout)

    def change_speed(self, value):
        global speed
        speed = value
        self.speed_label.setText(f"Скорость течения: {speed}")

    def change_frequency(self, value):
        global count_lilies
        count_lilies = value
        self.frequency_label.setText(f"Частота появления кувшинок: {count_lilies}")
        self.create_lilies(count_lilies)

    def add_frog(self):
        new_x = random.randint(0, size[0] - frog_size[0])
        new_y = random.randint(0, size[1] - frog_size[1])
        self.frogs.append(Frog(new_x, new_y))
        self.update()  # Обновляем вид, чтобы отобразить новую лягушку

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.setText("Продолжить")
        else:
            self.pause_button.setText("Пауза")

    def create_lilies(self, count):
        self.lilies.clear()
        for _ in range(count):
            x = random.randint(0, size[0] - lilies_size[0])
            y = random.randint(-1000, -lilies_size[1])
            self.lilies.append((x, y))

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(QColor(*lilies_color))  # Рисуем кувшинки
        for x, y in self.lilies:
            painter.drawEllipse(x, y, lilies_size[0], lilies_size[1])

        painter.setPen(QColor(*line_color))  # Рисуем следы лягушек
        for frog in self.frogs:
            painter.drawLine(frog.prev_x + frog_size[0] // 2, frog.prev_y + frog_size[1] // 2,
                             frog.x + frog_size[0] // 2, frog.y + frog_size[1] // 2)

        # Рисуем лягушек
        painter.setBrush(QColor(*frog_color))
        for frog in self.frogs:
            painter.drawEllipse(frog.x, frog.y, frog_size[0], frog_size[1])

    def update_position(self):
        if self.is_paused:
            return

        # Обновляем кувшинки
        for i in range(len(self.lilies)):
            x, y = self.lilies[i]
            y += speed
            if y > size[1]:
                x = random.randint(0, size[0] - lilies_size[0])
                y = random.randint(-1000, -lilies_size[1])
            self.lilies[i] = (x, y)

        # Обновляем лягушек
        for frog in self.frogs:
            # Сохраняем предыдущую позицию
            frog.prev_x = frog.x
            frog.prev_y = frog.y

            if frog.direction == -1:
                x_diffs = [(frog.x - self.lilies[k][0], k) for k in range(len(self.lilies))
                           if (self.lilies[k][1] > lilies_size[1] // 2) and (self.lilies[k][0] < frog.x)]
            elif frog.direction == 1:
                x_diffs = [(self.lilies[k][0] - frog.x, k) for k in range(len(self.lilies))
                           if self.lilies[k][1] > lilies_size[1] and self.lilies[k][0] > frog.x]

            if len(x_diffs) > 0:
                min_diff = min(x_diffs, key=lambda a: a[0])
                jump_distance = frog.x - self.lilies[min_diff[1]][0]
                frog.x = self.lilies[min_diff[1]][0]
                frog.y = self.lilies[min_diff[1]][1]
                new_x = random.randint(0, size[0] - lilies_size[0])
                new_y = random.randint(-1000, -lilies_size[1])
                self.lilies[min_diff[1]] = (new_x, new_y)

                # Обновим статистику лягушки
                frog.distance_traveled += abs(jump_distance)
                frog.last_jump_distance = abs(jump_distance)
                frog.jump_count += 1
                frog.drowned_lilies += 1  # Увеличиваем количество утонувших кувшинок
            else:
                if frog.direction == -1:
                    frog.x = 0
                elif frog.direction == 1:
                    frog.x = size[0] - frog_size[0]

            if frog.x <= 0 or frog.x >= size[0] - frog_size[0]:
                frog.direction *= -1

        self.update_table()
        self.update()  # Обновляем вид

    def update_table(self):
        self.table_widget.setRowCount(len(self.frogs))
        for row, frog in enumerate(self.frogs):
            self.table_widget.setItem(row, 0, QTableWidgetItem(f"({frog.x}, {frog.y})"))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(frog.drowned_lilies)))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(frog.distance_traveled)))
            if frog.jump_count > 0:
                average_jump = frog.distance_traveled / frog.jump_count
            else:
                average_jump = 0
            self.table_widget.setItem(row, 3, QTableWidgetItem(f"{average_jump:.2f}"))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(frog.jump_count)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
