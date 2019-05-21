import numpy

import os
os.environ['KERAS_BACKEND'] = 'theano'

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras import optimizers
import csv

# Устанавливаем seed для повторяемости результатов
numpy.random.seed(42)


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

            out_data = out_data.replace('X', '0')
            out_data = out_data.replace('+', '0')
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

# Загружаем данные
(X_train, y_train), (X_test, y_test) = load_data()

# Создаем последовательную модель
model = Sequential()

# Добавляем уровни сети
model.add(Dense(100, input_dim=100, activation="softsign", kernel_initializer="normal"))
model.add(Dense(20, activation="softsign", kernel_initializer="normal"))
model.add(Dense(10, activation="softsign", kernel_initializer="normal"))
model.add(Dense(100, activation="softsign", kernel_initializer="normal"))

# Компилируем модель
model.compile(loss="mean_absolute_error", optimizer=optimizers.SGD(lr=0.4, clipvalue=0.5), metrics=["mse"])

print(model.summary())

# Обучаем сеть
model.fit(X_train, y_train, batch_size=200, epochs=70, validation_split=0.2, verbose=2)

# Оцениваем качество обучения сети на тестовых данных
scores = model.evaluate(X_test, y_test, verbose=0)
print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))

print("Сохраняем сеть")
# Сохраняем сеть для последующего использования
# Генерируем описание модели в формате json
model_json = model.to_json()
json_file = open("seabattle_model.json", "w")
# Записываем архитектуру сети в файл
json_file.write(model_json)
json_file.close()
# Записываем данные о весах в файл
model.save_weights("seabattle_model.h5")
print("Сохранение сети завершено")

# res = model.predict(X_test)
#
# res = zip(X_test[0], y_test[0], [1 if a >= 0.2 else 0 for a in res[0]])
#
# for a in res:
#     print(a)