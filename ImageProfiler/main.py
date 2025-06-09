# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import config
import os
import csv
from PIL import Image, ImageDraw, ImageFont


def add_margin(image_path, output_path, color, left_margin, top_margin):
    # Открываем изображение
    image = Image.open(image_path)

    # Получаем размеры исходного изображения
    width, height = image.size

    # Вычисляем новые размеры изображения с дополнительным местом слева
    new_width = width + left_margin
    new_height = height + top_margin

    # Создаем новое изображение с увеличенными размерами
    new_image = Image.new(image.mode, (new_width, new_height), color)

    # Вставляем исходное изображение в новое изображение с заданным отступом слева
    new_image.paste(image, (left_margin, 0))

    # Сохраняем результат
    if not os.path.exists(output_path):
        # Если папка не существует, создаем ее
        print(output_path)
        os.makedirs(output_path)

    # Формируем полный путь к сохраняемому файлу
    output_file_path = os.path.join(output_folder, f"{file_name}")

    # Сохраняем результат
    new_image.save(output_file_path)








full_path = os.path.join(config.PROJECT_PATH, config.IMAGES_PATH)

print("Полный путь:", full_path)
# Получаем список файлов в указанной папке
files = os.listdir(full_path)

output_folder = os.path.join(config.PROJECT_PATH, config.EXPORT_PATH)
output_folder = output_folder.replace("\\", "/")
# Путь к папке с изображениями
merged_images_folder = output_folder

# Получаем список файлов в папке
files_to_delete = os.listdir(merged_images_folder)

# Проходимся по списку файлов и удаляем каждый файл
for file_name in files_to_delete:
    file_path = os.path.join(merged_images_folder, file_name)
    os.remove(file_path)

print("Старые изображения удалены.")


index = 0
# Выводим список файлов
for file_name in files:
    # Путь к исходному изображению
    input_image_path = os.path.join(full_path, file_name)
    input_image_path = input_image_path.replace("\\", "/")  # Заменяем обратные слеши на прямые

    # Путь для сохранения результата (указываем папку, а не файл)
    output_folder = os.path.join(config.PROJECT_PATH, config.EXPORT_PATH)
    output_folder = output_folder.replace("\\", "/")  # Заменяем обратные слеши на прямые

    # Цвет, которым будет заполнено дополнительное пространство слева (в формате RGB)
    margin_color = (0, 0, 0)


    print(f"input_image_path: {input_image_path}")
    print(f"output_folder: {output_folder}")

    # Добавляем дополнительное пространство слева на изображение
    add_margin(input_image_path, output_folder, margin_color, config.ADD_SCREEN_WIDTH, config.ADD_SCREEN_HEIGHT)

#
# Finish generating images
#

data_path = os.path.join(config.PROJECT_PATH, config.DATA_PATH)
data_path = data_path.replace("\\", "/")
data_path += "/"
print(f'Data path: {data_path}')

# Получаем список файлов в папке
data = os.listdir(data_path)

# Инициализируем переменные для хранения максимального числа и имени файла с этим числом
max_number = -1
max_file = None

# Проходимся по каждому файлу
for file_name in data:
    # Разделяем имя файла по подчеркиванию и берем последнюю часть
    parts = file_name.split('_')
    last_part = parts[-1]

    # Пытаемся извлечь число из последней части имени файла
    try:
        number = int(last_part.split('.')[0])

        # Если это число больше текущего максимального, обновляем максимальное число и имя файла
        if number > max_number:
            max_number = number
            max_file = file_name
    except ValueError:
        # Пропускаем файлы, в именах которых нет числа после последнего подчеркивания
        pass


data_path = os.path.join(data_path, max_file)
data_path = data_path.replace("\\", "/")

if max_file:

    #data_path = os.path.join(data_path, max_file)
    #data_path = data_path.replace("\\", "/")

    with open(data_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) # Читаем первую строку, которая содержит заголовки

        for row in reader:
                # Получаем имя изображения из первого столбца
            image_name = row[0] + ".jpeg"  # Предполагаем, что изображения имеют расширение .jpeg
                # Путь к изображению
            image_path = os.path.join(merged_images_folder, image_name)
            image_path = image_path.replace("\\", "/")

            print(f"image_path: {image_path}")

                # Открываем изображение
            image = Image.open(image_path)

                # Создаем объект ImageDraw
            draw = ImageDraw.Draw(image)

                # Указываем координаты и текст, который нужно написать
            text = "Пример текста"

                # Указываем координаты левого верхнего угла текста
                # и выбираем шрифт
                # Указываем цвет текста (в формате RGB)
            font = ImageFont.truetype("arial.ttf", 36)  # Указываем путь к шрифту и его размер
            text_color = (255, 255, 255)
            location = (100, 100)

            for index, value in enumerate(row):
                if index <= len(header) and value != "":
                    tmp = header[index] + " :  " + value
                    location = (100, 50 * (1 + index))
                # Рисуем текст на изображении
                    draw.text(location , tmp, fill=text_color, font=font)

                # Сохраняем результат
            image.save(image_path)



