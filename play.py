import os
os.environ['KERAS_BACKEND'] = 'theano'

from keras.utils import np_utils
from keras.models import model_from_json
from keras import optimizers
from keras import losses

import csv
import numpy

def load_data():
    input_data = []
    output_data = []

    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ';')
        for row in csv_reader:
            in_data = row[0]
            out_data = row[1]
            in_data = in_data.replace('X', '1')
            in_data = in_data.replace('+', '1')
            in_data = in_data.replace('_', '0')
            in_data = in_data.replace('-', '0')

            out_data = out_data.replace('X', '1')
            out_data = out_data.replace('+', '1')
            out_data = out_data.replace('O', '1')
            out_data = out_data.replace('_', '0')
            out_data = out_data.replace('-', '0')

            in_data = list(map(lambda a: int(a), in_data))
            out_data = list(map(lambda a: int(a), out_data))

            input_data.append(in_data)
            output_data.append(out_data)

    input_data = numpy.asarray(input_data)
    output_data = numpy.asarray(output_data)

    input_data_test = input_data[8000:]
    input_data = input_data[:8000]

    output_data_test = output_data[8000:]
    output_data = output_data[:8000]

    return (input_data, output_data), (input_data_test, output_data_test)

print("Загружаю сеть из файлов")
# Загружаем данные об архитектуре сети
json_file = open("seabattle_model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
# Создаем модель
loaded_model = model_from_json(loaded_model_json)
# Загружаем сохраненные веса в модель
loaded_model.load_weights("seabattle_model.h5")
print("Загрузка сети завершена")

# Загружаем данные
(X_train, y_train), (X_test, y_test) = load_data()

# Компилируем загруженную модель
loaded_model.compile(loss="mean_absolute_error", optimizer=optimizers.SGD(lr=0.4, clipvalue=0.5), metrics=["mse"])


# Оцениваем качество обучения сети загруженной сети на тестовых данных
scores = loaded_model.evaluate(X_test, y_test, verbose=0)
print("Точность работы загруженной сети на тестовых данных: %.2f%%" % (scores[1]*100))

res = loaded_model.predict(X_test)

print(res[0])

xt = numpy.asarray([255 if a == 1 else a for a in X_test[15]]).reshape(10, 10)
yt = numpy.asarray([255 if a == 1 else a for a in y_test[15]]).reshape(10, 10)
rt = numpy.asarray([int(-numpy.sign(a))*255 for a in res[15]]).reshape(10, 10)

from PIL import Image, ImageDraw

image = Image.new("L", (500, 500), (255, ))
draw = ImageDraw.Draw(image)
for i in range(10):    # For every pixel:
    for j in range(10):
        draw.rectangle((i*50, j*50, (i+1)*50, (j+1)*50), fill = (xt[i][j], ))

image.save("images/xt.png", "PNG")

image = Image.new("L", (500, 500), (255, ))
draw = ImageDraw.Draw(image)
for i in range(10):    # For every pixel:
    for j in range(10):
        draw.rectangle((i*50, j*50, (i+1)*50, (j+1)*50), fill = (yt[i][j], ))

image.save("images/yt.png", "PNG")

image = Image.new("L", (500, 500), (255, ))
draw = ImageDraw.Draw(image)
for i in range(10):    # For every pixel:
    for j in range(10):
        draw.rectangle((i*50, j*50, (i+1)*50, (j+1)*50), fill = (rt[i][j], ))

image.save("images/rt.png", "PNG")

