# <center> Проект Easy Editor
Данный пример демонстрирует создание простого графического редактора изображений с использованием библиотек PyQt5 и стандартных модулей Python. Давайте рассмотрим пошагово, как создать аналогичный проект.

## Шаг 1: Установка необходимых пакетов
(Если работаете в своем редакторе, а не в Algo VsCode)
Для начала убедитесь, что у вас установлены следующие пакеты:
+ Python: Установите последнюю версию Python (рекомендуемая версия 3.x).
+ PyQt5: Библиотека для разработки GUI-приложений на Python. Её можно установить командой:

```pip install pyqt5```

## Шаг 2: Импортирование нужных модулей

Первым делом импортируйте необходимые модули и классы:
```python
import os  # Импортируем модуль os для работы с файловой системой

# Подключаем необходимые модули библиотеки PyQt5 для графического интерфейса
from PyQt5.QtCore import Qt  
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog,  # Основные классы приложения и виджетов
    QLabel, QPushButton, QListWidget,     # Метки, кнопки и список файлов
    QHBoxLayout, QVBoxLayout              # Горизонтальные и вертикальные компоновщики
)
```
*Для добавления цвета фона и кнопок*
```python
from PyQt5.QtGui import QPalette, QColor   # Палитра цветов и класс цвета
```

## Шаг 3: Определение констант и инициализация переменных

Определим некоторые важные переменные и константы:

```python
BACK = (19, 138, 66)  # RGB-значение зелёного цвета фона
workdir = ''  # Переменная для хранения выбранного пути к папке
```

## Шаг 4: Создание окна приложения
Создадим главное окно приложения:

```python
app = QApplication([])  # Экземпляр приложения
win = QWidget()         # Главный виджет окна
```

Далее настроим оформление окна, включив цвет фона и заголовок:
```python
palette = QPalette()        # Настройка палитры цветов окна
palette.setColor(QPalette.Window, QColor(*BACK))  # Устанавливаем фоновый цвет окна
win.setPalette(palette)     # Применяем палитру к окну
win.setAutoFillBackground(True)  # Включаем автоматическое заполнение фоном (True - обязательно!!!)
win.resize(700, 400)        # Размер окна
win.setWindowTitle('Easy Editor')  # Заголовок окна
```

```*BACK``` -> распаковка кортежа из переменной BACK. Кортеж (19, 138, 66) с помощью * автоматически разделяется на самостоятельные значения. Это нужно потому что, в QColor нужно передать 3 отдельных параметра, а не целый кортеж.

## Шаг 5: Создание элементов интерфейса
Теперь создадим различные элементы интерфейса нашего приложения:

### 1. Метка для отображения изображения:
```python
lb_image = QLabel('Картинка')  # Метка, куда будем выводить картинку
```
### 2. Кнопка для выбора папки с изображениями:
```python
btn_dir = QPushButton('Папка')  # Кнопка открытия папки
```
### 3. Список файлов:
```python
lw_files = QListWidget()  # Список файлов в выбранной папке
```
### 4. Инструменты редактирования:

+ ```btn_left = QPushButton('Лево')  # Поворот влево```
+ ```btn_right = QPushButton('Право')  # Поворот вправо```
+ ```btn_flip = QPushButton('Зеркало')  # Отразить горизонтально```
+ ```btn_sharp = QPushButton('Резкость')  # Увеличить резкость```
+ ```btn_bw = QPushButton('Ч/Б')  # Перевести в чёрно-белый режим```
+ ```btn_save = QPushButton('Сохранить')  # Сохранить изменения```
+ ```btn_reset = QPushButton('Сбросить фильтры')  # Вернуть исходное состояние```

Затем задаём уникальные стили каждой кнопке: (ПО ЖЕЛАНИЮ!!!)

Чтобы каждому элементу интерфейса назначить уникальный цвет,
мы можем воспользоваться методом setStyleSheet, который позволяет применять стили CSS прямо к виджетам.
Метод .setStyleSheet() принимает строку с правилами CSS, аналогично стилю HTML/CSS.
Эти правила определяют внешний вид конкретного виджета,
включая такие аспекты, как цвет фона, цвет шрифта, размер шрифта, границы и другие декоративные эффекты.
Свойство background-color - определяет цвет фона кнопки.
Свойство color - устанавливает цвет текста на кнопке.

+ ```btn_dir.setStyleSheet("background-color: green; color: white;")```
+ ```btn_left.setStyleSheet("background-color: blue; color: yellow;")```
+ ```btn_right.setStyleSheet("background-color: red; color: black;")```
+ ```btn_flip.setStyleSheet("background-color: purple; color: pink;")```
+ ```btn_shrap.setStyleSheet("background-color: orange; color: brown;")```
+ ```btn_bw.setStyleSheet("background-color: gray; color: lightgray;")```
+ ```btn_save.setStyleSheet("background-color: teal; color: darkblue;")```
+ ```btn_reset.setStyleSheet("background-color: limegreen; color: maroon;")```

### Шаг 6: Организация компоновки окон

Используя макеты компоновщиков, расположим элементы на экране:
```python
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
row_tools.addWidget(btn_shrap)          # Добавление кнопки повышения резкости
row_tools.addWidget(btn_bw)             # Добавление кнопки преобразования в Ч/Б
row_tools.addWidget(btn_save)           # Добавление кнопки сохранения
row_tools.addWidget(btn_reset)          # Добавление кнопки сброса фильтров

## Но можно и вот так! 
# for btn in [btn_left, btn_right, btn_flip, btn_sharp, btn_bw, btn_save, btn_reset]:
#    row_tools.addWidget(btn)

# Размещаем панель инструментов ниже изображения
col2.addLayout(row_tools)

# Назначаем основную компоновку окна
win.setLayout(row)

# Показываем окно
win.show()
```

## Шаг 6: Создание вспомогательных функций

### Функция filter_files

Эта функция фильтрует файлы по указанному набору расширений.

```python
def filter_files(files, extensions):
    """
    Функция предназначена для фильтрации списка файлов по указанным расширениям.

    Параметры:
    ----------
    files : list of str
        Список имен файлов (полных путей или только имен файлов).
    
    extensions : list of str
        Список расширений, по которым осуществляется фильтрация.

    Возвращаемое значение:
    ---------------------
    list of str
        Список файлов, соответствующих заданному набору расширений.
    """

    result = []                   # Инициализируем пустой список для хранения подходящих файлов.

    for filename in files:        # Перебираем все файлы из переданного списка.
        for ext in extensions:     # Для каждого файла проверяем каждое возможное расширение.
            if filename.endswith(ext):  # Проверяем, совпадает ли конец имени файла с текущим расширением.
                result.append(filename)  # Если совпадение найдено, добавляем файл в результирующий список.

    return result             
```
*Но можно и так* 

```python
return [filename for filename in files if any(filename.endswith(ext) for ext in extensions)]
```

Хотя списки включений внешне выглядят сложнее, они часто работают быстрее традиционных циклов. Причина заключается в том, что компилятор оптимизирует выполнение выражений, применяя различные внутренние оптимизации. Конечно, разница заметна больше всего при обработке больших объемов данных, однако даже для небольших коллекций такая форма записи экономит ресурсы и улучшает производительность.

List comprehensions делают ваш код лаконичным, эффективным и простым для чтения. Они идеально подходят для случаев, когда вам нужно быстро создать новый список путем фильтрации и трансформации исходного набора данных. Однако важно помнить о балансе между простотой и ясностью: если включение получается слишком громоздким, лучше вернуться к традиционным конструкциям.

### Функция choose_workdir() 

Фуекция служит для интерактивного выбора рабочего каталога, где находятся изображения. Полученный путь сохраняется в глобальной переменной workdir, доступной всему приложению.

Объявление глобальной переменной:  
``` python 
global workdir
``` 

Ключевое слово ```global``` объявляет переменную workdir (строка 37) как глобальную. Это означает, что любые изменения, произведённые внутри функции, сохраняются и влияют на переменную за пределами самой функции. Без объявления переменная была бы локальной и исчезала бы после выхода из функции.

**Зачем нужна глобальная переменная workdir?**

+ Хранение состояния программы:Переменная workdir хранит выбранную пользователем рабочую директорию, содержащую изображения. Чтобы другие части программы могли обратиться к этой директории (например, для загрузки изображений, анализа или других действий), информация должна быть доступна вне контекста конкретной функции. Глобальная переменная решает эту проблему, делая путь доступным всей программе.
+ Простота передачи данных:Использование глобальной переменной упрощает передачу данных между разными частями программы. Альтернативой было бы передавать выбранную директорию через аргументы функций или использовать специальные классы и объекты для сохранения состояний. Но такие подходы усложняют структуру кода и требуют дополнительной организации. Глобальная переменная — самый быстрый и простой способ обеспечить доступ к значимому состоянию.
+ Минимизация числа аргументов: Передавать рабочий каталог через аргументы различных функций означало бы необходимость постоянно держать цепочку передач и обеспечивать корректность передаваемых значений. Использование глобальной переменной сокращает количество передаваемых аргументов и уменьшает вероятность ошибок, связанных с неправильной передачей данных.
+ Уменьшение дублирования:Хранение информации о рабочем каталоге в глобальной переменной предотвращает повторное открытие диалогового окна для повторного выбора директории при каждом обращении к изображениям. Один раз выбрав директорию, вы можете повторно обращаться к ней из любой точки программы.

Получение выбранного пути:  
```python
workdir = QFileDialog.getExistingDirectory()
```
Данный оператор вызывает стандартное диалоговое окно выбор директорий, предоставляемое библиотекой PyQt. Пользователь выбирает нужную директорию, и её путь записывается в переменную workdir. Если пользователь отменил операцию выбора (закрыл диалог без выбора), функция вернёт пустую строку или None, в зависимости от настроек.

### Функция show_filenames()

Функция show_filenames() реализует механизм взаимодействия с пользователем для выбора папки с изображениями, фильтрации нужных файлов по заданным расширениям и последующего отображения полученных файлов в графическом интерфейсе. Такой подход удобен и эффективен для приложений, работающих с медиафайлами, такими как просмотрщики изображений или редакторы фотографий.

1. Определение поддерживаемых расширений:
```python
extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
```
Здесь создаётся список возможных расширений файлов изображений, которые наша программа поддерживает. Любые файлы, не попадающие под эти расширения, игнорируются при дальнейшей работе.

2. Выбор рабочей директории:
```python
choose_workdir()
```
Эта команда открывает диалоговое окно для выбора папки, где хранятся изображения. Диалог даёт пользователю возможность выбрать директорию вручную, а выбранный путь сохраняется в глобальной переменной workdir.

3. Получение списка файлов:
```python
filenames = filter_files(os.listdir(workdir), extensions)
```
Сначала функция os.listdir() возвращает список всех файлов и папок в указанной директории. Затем эти файлы фильтруются с помощью заранее подготовленной функции filter_files(), которая оставляет только файлы с нужными расширениями.

4. Очистка существующего списка:
```python
lw_files.clear()
```

Команда очищает текущий список отображённых файлов в графическом интерфейсе. Это гарантирует, что старые данные удаляются перед добавлением новых.

5. Заполнение списка новыми файлами:
```python
for filename in filenames:
    lw_files.addItem(filename)
Циклом проходят по отфильтрованным файлам и добавляют их названия в графический компонент lw_files, который является списком в интерфейсе.
```
## <center> **Обработка изображений**

Класс ImageProcessor представляет собой инструмент для обработки изображений с использованием библиотеки Python Imaging Library (PIL, также известной как Pillow) и интеграции графического интерфейса через библиотеку PyQt5. Этот класс позволяет загружать изображения, изменять их различными способами (например, преобразовывать в черно-белые, поворачивать, отражать), сохранять обработанные версии и отображать их на экране.

**Детали реализации:**

Конструктор (__init__)

```python
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
```
Загрузка изображения (load_image)

Этот метод принимает два параметра: dir (каталог изображения) и filename (название файла). После формирования полного пути к изображению оно открывается с помощью метода Image.open() из библиотеки PIL.Также создаётся резервная копия оригинального изображения (original_image), которую можно использовать позже для восстановления первоначального состояния.

```python
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
```

Отображение изображения (show_image)

Метод получает путь к изображению и отображает его на экране в элементе QLabel окна приложения. Для показа изображения используются следующие шаги:

+ Создание экземпляра класса QPixmap, представляющего растровое изображение.
+ Определение размеров метки QLabel, чтобы подогнать изображение под нужный размер экрана.
+ Масштабирование изображения с сохранением соотношения сторон методом scaled().
+ Установка изображения в элемент QLabel.

QPixmap — это специальный класс в библиотеке PyQt5,
предназначенный для хранения и отображения растровых изображений (bitmap images). Его основное предназначение — быстрая и эффективная работа с графикой, особенно в приложениях с большим количеством графики, анимаций или динамических изображений.

Метод scaled() принадлежит классу QPixmap и служит для изменения размера изображения с сохранением пропорций или без сохранения (в зависимости от переданного флага).

```python
def show_image(self, path: str) -> None:
    """
    Метод показывает изображение в QLabel (метке).
    Принимает путь к изображению и выводит его в соответствующем размере.
    Если ширина или высота изображения превышают размеры QLabel, изображение масштабируется.
    """
    pixmapimage = QPixmap(path)  # Создаем пиксельную карту из изображения        
    label_width, label_height = lb_image.width(), lb_image.height()  # Получаем размеры QLabel
    scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)  # Масштабируем изображение
    lb_image.setPixmap(scaled_pixmap)  # Устанавливаем пиксельную карту в QLabel        
    lb_image.setVisible(True)  # Делаем QLabel видимой
```

**Обработка изображений** 

Класс поддерживает ряд методов для различных операций над изображением:

*Преобразование в ч/б (do_gray)*

Переводит изображение в чёрно-белое представление путём преобразования режима цвета (convert('L')). Результат сохраняется и выводится на экран.
```python
def do_gray(self) -> None:
    """
    Метод превращает изображение в чёрно-белое.
    Затем сохраняет изменённое изображение и отображает его.
    """
    self.image = self.image.convert('L')  # Переводим изображение в режим L (чёрно-белое)
    self.save_image()                      # Сохраняем изменённое изображение
    image_path = os.path.join(self.dir, self.save_dir, self.filename)  # Формируем путь к новому изображению
    self.show_image(image_path) # Показываем новое изображение
```

*Повороты изображения (do_left, do_right)*

Эти методы позволяют повернуть изображение соответственно на 90 градусов влево и вправо, используя операции транспонирования (transpose()). Изменённое изображение сохраняется и отображается.
```python
def do_left(self) -> None:        
    """
    Поворачивает изображение налево на 90 градусов.
    """
    self.image = self.image.transpose(Image.ROTATE_90)  # Поворот изображения на 90° против часовой стрелки
    # Сохраняем изменённое изображение
    # Формируем путь к новому изображению
    # Показываем новое изображение 

def do_right(self) -> None:
    """
    Поворачивает изображение направо на 90 градусов.
    """
    self.image = self.image.transpose(Image.ROTATE_270)  # Поворот изображения на 90° по часовой стрелке
    # Сохраняем изменённое изображение
    # Формируем путь к новому изображению
    # Показываем новое изображение   
```

**Зеркальное отражение (do_flip)**

Осуществляет горизонтальное переворачивание изображения ("переворот справа налево"). Обработанная версия сохраняется и отображается на экране.
```python
def do_right(self) -> None:
    """
    Поворачивает изображение направо на 90 градусов.
    """
    self.image = self.image.transpose(Image.ROTATE_270)  # Поворот изображения на 90° по часовой стрелке
    # Сохраняем изменённое изображение
    # Формируем путь к новому изображению
    # Показываем новое изображение
```

*Зеркальное отражение (do_flip)*

Осуществляет горизонтальное переворачивание изображения ("переворот справа налево"). Обработанная версия сохраняется и отображается на экране.

```python
def do_flip(self) -> None:
    """
    Отражает изображение слева направо (горизонтальное отражение).
    """
    self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)  # Горизонтальное зеркальное отражение
    # Сохраняем изменённое изображение
    # Формируем путь к новому изображению
    # Показываем новое изображение
```

**Усиление резкости (do_sharpen)**

Применяется стандартный фильтр резкости (filter(ImageFilter.SHARPEN)), делающий контуры изображения чётче. Как и другие методы, этот тоже сохраняет итоговую версию и показывает её на экране.
```python
def do_sharpen(self) -> None:
    """
    Применяет фильтр резкости к изображению.
    """
    self.image = self.image.filter(ImageFilter.SHARPEN)      # Применение фильтра резкости
    # Сохраняем изменённое изображение
    # Формируем путь к новому изображению
    # Показываем новое изображение
```
*Сохранение изображения (save_image)*

Проверяет, существует ли папка для сохранения обработанных изображений (self.save_dir). Если такой папки нет, она автоматически создаётся. Далее изображение сохраняется в указанной директории.

**Использование модулей и назначение функций:**

1. os.path.join(*paths)
Эта функция соединяет один или несколько компонентов пути, учитывая особенности файловой системы конкретной платформы (Windows, Linux и др.). Она гарантирует, что элементы пути будут объединены правильным способом, даже если между ними присутствуют пробелы или лишние слэши.

Примеры:

os.path.join('/home', 'user', 'Documents') вернёт /home/user/Documents
os.path.join('C:', '\\folder', 'file.txt') вернёт C:\folder\file.txt (для Windows)
Назначение: помогает создать валидный абсолютный или относительный путь, объединяя части пути.

2. os.path.exists(path)
Эта функция проверяет, существует ли заданный путь (это может быть файл или каталог). Функция возвращает True, если путь существует, иначе возвращается False.

Использование полезно, когда нужно убедиться, что файл или каталог доступен перед выполнением дальнейших операций (например, чтение или запись данных).

Примеры:

os.path.exists('/home/user/file.txt') вернёт True, если файл существует.
os.path.exists('/nonexistent/path') вернёт False.
Назначение: проверка доступности файла или каталога перед операциями чтения или записи.

3. os.path.isdir(path)
Данная функция проверяет, является ли указанный путь каталогом. Если да, возвращается True, иначе — False. Важно отметить, что эта функция не проверяет, существует ли сам путь, она лишь подтверждает, что существующий путь относится к типу каталога.

Примеры:

os.path.isdir('/home/user') вернёт True, если /home/user является существующим каталогом.
os.path.isdir('/home/user/file.txt') вернёт False, так как путь ведёт к файлу, а не к каталогу.
Назначение: определение типа объекта файловой системы (является ли он каталогом).

4. os.mkdir(path)
Создает новый каталог по указанному пути. Если каталог уже существует, возникает исключение FileExistsError. Если путь включает промежуточные несуществующие каталоги, потребуется дополнительно использовать функцию os.makedirs(), которая рекурсивно создает вложенные каталоги.

Примеры:

os.mkdir('/tmp/new_folder') создаст новую папку /tmp/new_folder, если такая ещё не существует.

Назначение: создание новых каталогов в файловой системе.

5. os.path.join(*paths) (второй раз)
Здесь повторно применяется функция объединения путей, но теперь для сборки полного пути к файлу внутри ранее сформированного каталога.

Назначение: сборка полных путей к файлам, основываясь на каталоге и имени файла.

Резюме процесса:

+ Сначала определяется полный путь к целевой папке, куда планируется сохранить изображение.
+ Проверяется, существует ли эта папка с помощью комбинации проверок exists() и isdir().
+ Если папка не найдена, она создается функцией mkdir().
+ Полностью формируется путь к файлу и изображение сохраняется в указанное место с помощью метода save() объекта изображения.
+ Такой подход удобен и надежен, позволяя избежать ошибок, связанных с отсутствием необходимых каталогов при сохранении файлов.

```python
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
```

*Возврат к оригинальному состоянию (reset_image)*

Восстанавливает исходное изображение, перезагружая копию оригинала (original_image), и обновляет экран, возвращаясь к первоначальному виду.

```python
 def reset_image(self) -> None:
    """
    Восстанавливает исходное состояние изображения, сбрасывая все применённые фильтры.
    """
    if self.original_image is None:
        return
    self.image = self.original_image.copy()  # Возвращаемся к оригинальной копии изображения
    image_path = os.path.join(workdir, self.filename)  # Формируем путь к оригиналу
    self.show_image(image_path)  # Показываем исходное изображение
```       
### Функциональность выбора и отображения изображений в приложении с графическим интерфейсом.

Давайте рассмотрим его пошагово:

**Общая логика работы программы:*

+ Описание цели:Функция show_chosen_image() предназначена для отображения выбранного пользователем изображения в окне приложения. Пользователь выбирает файл в списке, и приложение загружает выбранное изображение и отображает его на экране.
+ Определение выбранной позиции:Перед началом любых действий проверяется, действительно ли выбрана какая-нибудь позиция в списке файлов (lw_files.currentRow() >= 0). Это предотвращает попытки обработать ситуацию, когда ничего не выбрано.
+ Выбор имени файла:Если положение в списке выбрано, программа извлекает имя выбранного файла (lw_files.currentItem().text()). Переменная lw_files — это список файлов (виджет QListWidget), а метод currentItem() возвращает текущий выбранный элемент списка.
+ Загрузка изображения:Используя имя файла и рабочий каталог (workdir), вызывается метод load_image() класса ImageProcessor, который загружает изображение из файловой системы и сохраняет его для последующей обработки.
+ Формирование пути к изображению:Путём комбинирования рабочего каталога (workimage.dir) и имени файла (workimage.filename) строится полный путь к изображению.
+ Отображение изображения:Наконец, вызвав метод show_image() класса ImageProcessor, программа отображает выбранное изображение в графическом интерфейсе, помещая его в элемент QLabel.
+ Подключение сигнала к слоту:Код подключает сигнал currentRowChanged (изменение выбранной строки в списке) элемента lw_files к слоту show_chosen_image, чтобы каждый раз при изменении выбора автоматически происходило обновление изображения на экране.

*Что делают конкретные методы?* 

+ load_image():Данный метод класса ImageProcessor отвечает за загрузку изображения из файловой системы по переданному пути и сохранению данных изображения для последующих манипуляций.
+ show_image():Этот метод занимается отображением изображения в графическом интерфейсе. Вероятно, он формирует пикселизированное изображение с помощью библиотеки Qt (например, через QPixmap) и устанавливает его в компонент QLabel.

*Важность сигналов и слотов:*

Связывание сигнала currentRowChanged с функцией show_chosen_image() означает, что каждый раз, когда пользователь выбирает другой файл в списке, приложение немедленно вызывает эту функцию, вызывая обновление изображения на экране.

```python
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
```




## Запуск прототипа

+ Связывание события нажатия кнопки 'Папка' с функцией обновления списка файлов
 ```btn_dir.clicked.connect(show_filenames)```

+ Подключаем кнопки к соответствующим методам

```btn_bw.clicked.connect(workimage.do_gray)       # Кнопка "Ч/Б"```
```btn_left.clicked.connect(workimage.do_left)     # Кнопка поворота налево```
```btn_right.clicked.connect(workimage.do_right)   # Кнопка поворота направо```
```btn_sharp.clicked.connect(workimage.do_sharpen) # Кнопка повышения резкости```
```btn_flip.clicked.connect(workimage.do_flip)     # Кнопка отражения```
```btn_reset.clicked.connect(workimage.reset_image)# Кнопка восстановления исходного состояния```

+ Запуск основного цикла приложения
```app.exec()```