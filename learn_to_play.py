import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
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

    (input_data, output_data), (input_data_test, output_data_test)

    return (input_data, output_data), (input_data_test, output_data_test)


# Загружаем данные
(X_train, y_train), (X_test, y_test) = load_data()

print('\n')

# # Преобразование размерности изображений
# X_train = X_train.reshape(60000, 784)
# X_test = X_test.reshape(10000, 784)
# # Нормализация данных
# X_train = X_train.astype('float32')
# X_test = X_test.astype('float32')
# X_train /= 255
# X_test /= 255
#
# # Преобразуем метки в категории
# Y_train = np_utils.to_categorical(y_train, 10)
# Y_test = np_utils.to_categorical(y_test, 10)
#
# # Создаем последовательную модель
# model = Sequential()
#
# # Добавляем уровни сети
# model.add(Dense(800, input_dim=784, activation="relu", kernel_initializer="normal"))
# model.add(Dense(10, activation="softmax", kernel_initializer="normal"))
#
# # Компилируем модель
# model.compile(loss="categorical_crossentropy", optimizer="SGD", metrics=["accuracy"])
#
# print(model.summary())
#
# # Обучаем сеть
# model.fit(X_train, Y_train, batch_size=200, epochs=25, validation_split=0.2, verbose=2)
#
# # Оцениваем качество обучения сети на тестовых данных
# scores = model.evaluate(X_test, Y_test, verbose=0)
# print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))