import os  # Импортируем модуль os для работы с файловой системой

from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN

# Подключаем необходимые модули библиотеки PyQt5 для графического интерфейса
from PyQt5.QtCore import Qt  # Нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций

from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog,  # Основные классы приложения и виджетов
    QLabel, QPushButton, QListWidget,     # Метки, кнопки и список файлов
    QHBoxLayout, QVBoxLayout              # Горизонтальные и вертикальные компоновщики
)
from PyQt5.QtGui import (
    QPalette, QColor,   # Палитра цветов и класс цвета
    QPixmap # Оптимизированная для показа на экране картинка
)


# Константы
BACK = (19, 138, 66)       # Цвет фона окна (RGB значения зеленого оттенка)
workdir = ''                # Переменная для хранения пути выбранной папки

# Создание главного окна приложения
app = QApplication([])      # Создаем экземпляр приложения
win = QWidget()             # Основной виджет окна

"""Заливка фоном окна"""
palette = QPalette()        # Настройка палитры цветов окна
palette.setColor(QPalette.Window, QColor(*BACK))  # Устанавливаем фоновый цвет окна
win.setPalette(palette)     # Применяем палитру к окну
win.setAutoFillBackground(True)  # Включаем автоматическое заполнение фоном (True - обязательно!!!)

win.resize(700, 400)        # Размер окна
win.setWindowTitle('Easy Editor')  # Заголовок окна

# Элементы интерфейса
lb_image = QLabel('Картинка')           # Метка для отображения изображений
btn_dir = QPushButton('Папка')          # Кнопка выбора директории
lw_files = QListWidget()               # Список выбранных файлов

# Кнопки инструментов обработки изображений
btn_left = QPushButton('Лево')          # Поворот изображения влево
btn_right = QPushButton('Право')        # Поворот изображения вправо
btn_flip = QPushButton('Зеркало')      # Отражение изображения горизонтально
btn_sharp = QPushButton('Резкость')     # Повышение резкости изображения
btn_bw = QPushButton('Ч/Б')            # Преобразование в черно-белое изображение
btn_save = QPushButton('Сохранить')     # Сохранение изменений
btn_reset = QPushButton('Сбросить фильтры')  # Очистка всех примененных фильтров

# Индивидуализация стилей кнопок (CSS) <- CSS селекторы
btn_dir.setStyleSheet("background-color: green; color: white;")
btn_left.setStyleSheet("background-color: blue; color: yellow;")
btn_right.setStyleSheet("background-color: red; color: black;")
btn_flip.setStyleSheet("background-color: purple; color: pink;")
btn_sharp.setStyleSheet("background-color: orange; color: brown;")
btn_bw.setStyleSheet("background-color: gray; color: lightgray;")
btn_save.setStyleSheet("background-color: teal; color: darkblue;")
btn_reset.setStyleSheet("background-color: limegreen; color: maroon;")

# Компоновка элементов интерфейса
row = QHBoxLayout()                    # Горизонтальная компоновка
col1 = QVBoxLayout()                   # Левый столбец (вертикальное расположение)
col2 = QVBoxLayout()                   # Правый столбец (вертикальное расположение)

# Добавляем элементы в левый столбец
col1.addWidget(btn_dir)                 # Кнопка выбора папки
col1.addWidget(lw_files)                # Список файлов

# Добавляем метку изображения в правый столбец
col2.addWidget(lb_image, 95)            # Картинку располагаем на большую часть экрана

# Распределяем пространство между колонками (левая занимает 20%, правая — 80%)
row.addLayout(col1, 20)
row.addLayout(col2, 80)

# Панель инструментов с кнопками обработки изображений
row_tools = QHBoxLayout()              # Новая строка для размещения кнопок
row_tools.addWidget(btn_left)           # Добавление кнопки поворота влево
row_tools.addWidget(btn_right)          # Добавление кнопки поворота вправо
row_tools.addWidget(btn_flip)           # Добавление кнопки зеркального отражения
row_tools.addWidget(btn_sharp)          # Добавление кнопки повышения резкости
row_tools.addWidget(btn_bw)             # Добавление кнопки преобразования в Ч/Б
row_tools.addWidget(btn_save)           # Добавление кнопки сохранения
row_tools.addWidget(btn_reset)          # Добавление кнопки сброса фильтров

# Размещаем панель инструментов ниже изображения
col2.addLayout(row_tools)

# Назначаем основную компоновку окна
win.setLayout(row)

# Показываем окно
win.show()

# Вспомогательные функции

def filter_files(files: str, extensions: str) -> list:
    """Фильтрует файлы по указанным расширениям."""
    # Проходим по списку файлов / Проверяем расширение файла
    return [filename for filename in files if any(filename.endswith(ext) for ext in extensions)]
    # Аналогично этому:
        #    result = []
        #    for filename in files:
        #        for ext in extensions:
        #            if filename.endswith(ext):
        #                result.append(filename)
        #    return result
        
def choose_workdir():
    """Выбор рабочей директории с изображениями."""
    global workdir                  # Используем глобальную переменную workdir
    workdir = QFileDialog.getExistingDirectory()  # Открываем диалог выбора папки

def show_filenames():
    """Отображает имена файлов в списке."""
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # Расширения поддерживаемых форматов
    choose_workdir()                        # Выбираем директорию
    filenames = filter_files(os.listdir(workdir), extensions)  # Фильтруем файлы
    lw_files.clear()                         # Очищаем существующий список
    for filename in filenames:               # Заполняем список файлами
        lw_files.addItem(filename)

# Связывание события нажатия кнопки 'Папка' с функцией обновления списка файлов
btn_dir.clicked.connect(show_filenames)

"""Обработка изображений"""

class ImageProcessor():
    """
    Класс предназначен для загрузки, обработки и отображения изображений.
    Здесь реализованы методы для изменения изображения и сохранения обработанных версий.
    """    
    def __init__(self):
        """
        Конструктор класса ImageProcessor инициализирует внутренние поля:
        - self.image хранит загруженное изображение.
        - self.dir сохраняет путь к каталогу исходного изображения.
        - self.filename хранит название текущего обрабатываемого файла.
        - self.save_dir определяет директорию, куда будут сохраняться обработанные изображения.
        """
        self.image = None  # Объект изображения
        self.dir = None    # Каталог исходного изображения
        self.filename = None  # Имя файла изображения
        self.save_dir = 'Modified/'  # Папка для сохранения обработанных изображений
        self.original_image = None   # Исходное изображение, используется для сброса изменений
        
    def load_image(self, dir: str, filename: str) -> None:
        """
        Метод загружает изображение из указанного каталога и имени файла.
        Параметры:
        - dir: полный путь к каталогу изображения.
        - filename: имя файла изображения.
        
        Изображение открывается и сохраняется в виде объекта PIL.Image.
        Дополнительно сохраняются каталог и имя файла для дальнейшего использования.
        """
        self.dir = dir                     # Запоминаем путь к директории
        self.filename = filename           # Запоминаем имя файла
        image_path = os.path.join(dir, filename)  # Собираем полный путь к изображению
        self.image = Image.open(image_path)  # Открываем изображение с помощью библиотеки Pillow
        self.original_image = self.image.copy()  # Сохраняем копию оригинального изображения
    
    def show_image(self, path: str) -> None:
        """
        Метод показывает изображение в QLabel (метке).
        Принимает путь к изображению и выводит его в соответствующем размере.
        Если ширина или высота изображения превышают размеры QLabel, изображение масштабируется.
        """
        """QPixmap — это специальный класс в библиотеке PyQt5,
        предназначенный для хранения и отображения растровых изображений (bitmap images).
        Его основное предназначение — быстрая и эффективная работа с графикой,
        особенно в приложениях с большим количеством графики, анимаций или динамических изображений."""
        pixmapimage = QPixmap(path)  # Создаем пиксельную карту из изображения        
        label_width, label_height = lb_image.width(), lb_image.height()  # Получаем размеры QLabel
        """Метод scaled() принадлежит классу QPixmap и служит для изменения размера изображения
        с сохранением пропорций или без сохранения (в зависимости от переданного флага)."""
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)  # Масштабируем изображение
        lb_image.setPixmap(scaled_pixmap)  # Устанавливаем пиксельную карту в QLabel
        
        lb_image.setVisible(True)  # Делаем QLabel видимой
    
    def do_gray(self) -> None:
        """
        Метод превращает изображение в чёрно-белое.
        Затем сохраняет изменённое изображение и отображает его.
        """
        self.image = self.image.convert('L')  # Переводим изображение в режим L (чёрно-белое)
        self.save_image()                      # Сохраняем изменённое изображение
        image_path = os.path.join(self.dir, self.save_dir, self.filename)  # Формируем путь к новому изображению
        # Путь до папки с изображениями (dir) +/ modified (save_dir) +/ filename
        self.show_image(image_path)            # Показываем новое изображение
    
    def do_left(self) -> None:        
        """
        Поворачивает изображение налево на 90 градусов.
        """
        self.image = self.image.transpose(Image.ROTATE_90)  # Поворот изображения на 90° против часовой стрелки
        self.save_image()                                  # Сохраняем изменённое изображение
        image_path = os.path.join(workdir, self.save_dir, self.filename)  # Формируем путь к новому изображению
        self.show_image(image_path)                         # Показываем новое изображение
        
    def do_right(self) -> None:
        """
        Поворачивает изображение направо на 90 градусов.
        """
        self.image = self.image.transpose(Image.ROTATE_270)  # Поворот изображения на 90° по часовой стрелке
        self.save_image()                                   # Сохраняем изменённое изображение
        image_path = os.path.join(workdir, self.save_dir, self.filename)  # Формируем путь к новому изображению
        self.show_image(image_path)                          # Показываем новое изображение
        
    def do_flip(self) -> None:
        """
        Отражает изображение слева направо (горизонтальное отражение).
        """
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)  # Горизонтальное зеркальное отражение
        self.save_image()                                        # Сохраняем изменённое изображение
        image_path = os.path.join(workdir, self.save_dir, self.filename)  # Формируем путь к новому изображению
        self.show_image(image_path)                               # Показываем новое изображение
        
    def do_sharpen(self) -> None:
        """
        Применяет фильтр резкости к изображению.
        """
        self.image = self.image.filter(ImageFilter.SHARPEN)      # Применение фильтра резкости
        self.save_image()                                       # Сохраняем изменённое изображение
        image_path = os.path.join(workdir, self.save_dir, self.filename)  # Формируем путь к новому изображению
        self.show_image(image_path)                             # Показываем новое изображение
    
    def save_image(self) -> None:
        """
        Метод проверяет наличие директории для сохранения и создаёт её, если отсутствует.
        Затем сохраняет обработанное изображение в указанную директорию.
        """
        path = os.path.join(self.dir, self.save_dir)  # Определяем путь к папке Modified
        if not (os.path.exists(path) or os.path.isdir(path)):  # Проверяем существование папки
            os.mkdir(path)  # Создаём папку, если её ещё нет
        image_path = os.path.join(path, self.filename)  # Собираем полный путь к файлу
        self.image.save(image_path)  # Сохраняем изображение в указанный путь

    def reset_image(self) -> None:
        """
        Восстанавливает исходное состояние изображения, сбрасывая все применённые фильтры.
        """
        if self.original_image is None:
            return
        self.image = self.original_image.copy()  # Возвращаемся к оригинальной копии изображения
        image_path = os.path.join(workdir, self.filename)  # Формируем путь к оригиналу
        self.show_image(image_path)  # Показываем исходное изображение

def show_chosen_image() -> None:
    """
    Эта функция срабатывает при выборе нового изображения в списке.
    Она берёт выделенный файл и загружает его с помощью ImageProcessor.
    После загрузки отображается оригинальное изображение.
    """
    if lw_files.currentRow() >= 0:  # Проверяем, выбрано ли какое-то изображение
        filename = lw_files.currentItem().text()  # Берём имя выбранного файла
        workimage.load_image(workdir, filename)  # Загружаем изображение
        image_path = os.path.join(workimage.dir, workimage.filename)  # Формируем путь к изображению
        workimage.show_image(image_path)  # Показываем изображение в QLabel

# Текущая рабочая картинка для работы
workimage = ImageProcessor()  # Создаём экземпляр класса ImageProcessor

lw_files.currentRowChanged.connect(show_chosen_image)  # Соединяем изменение выборки с отображением изображения

# Подключаем кнопки к соответствующим методам
btn_bw.clicked.connect(workimage.do_gray)       # Кнопка "Ч/Б"
btn_left.clicked.connect(workimage.do_left)     # Кнопка поворота налево
btn_right.clicked.connect(workimage.do_right)   # Кнопка поворота направо
btn_sharp.clicked.connect(workimage.do_sharpen) # Кнопка повышения резкости
btn_flip.clicked.connect(workimage.do_flip)     # Кнопка отражения
btn_reset.clicked.connect(workimage.reset_image)# Кнопка восстановления исходного состояния


# Запуск основного цикла приложения
app.exec()