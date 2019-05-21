import numpy

import os

os.environ['KERAS_BACKEND'] = 'theano'

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras import optimizers
from keras import utils
from keras import models


def get_categorizer(input_data: numpy.ndarray,
                    result_data: numpy.ndarray,
                    num_cat: int,
                    train_amount: float = 0.8,
                    model: models = Sequential(),
                    layers: list = None,
                    loss: str = "categorical_crossentropy",
                    optimizer: str = "SGD",
                    metrics: str = "accuracy",
                    batch_size: int = None) -> type(lambda a: a):
    """
    Возвращает по полученным параметрам функцию-классификатор
    :param input_data: list
        Список с входными данными. Каждый элемент списка также может быть списком.
    :param result_data: list
        Список с ожидаемыми данными. Каждый элемент списка также может быть списком.
    :param num_cat: int
        Количество ожидаемых категорий.
    :param train_amount: float, optional
        Размер обучающей выборки в диапазоне от 0 до 1. По умолчанию 0.8 (80%)
    :param model: keras.models, optional
        Модель из keras.models. По умолчанию Sequential (последовательная)
    :param layers: list, optional
        Список слоев в соответствующем порядке. Слои в списке должны соответствовать
        одному из типов слоёв в keras. По умолчанию используются два полносвязных слоя,
        один из которых по размеру равен количеству свойств объекта, а второй -
        количеству категорий.
    :param loss: string, optional
        Функция ошибки. Должна соответствовать одному из названий функций
        ошибки в keras. По умолчанию = "categorical_crossentrophy"
    :param optimizer: string, optional
        Функция оптимизации. Должна соответствовать одному из названий функций
        оптимизации в keras. По умолчанию = "SGD"
    :param metrics: string, optional
        Функция измерения точности. Должна соответствовать одному из названий метрик
        в keras. По умолчанию = "accuracy"
    :param batch_size: int, optional
        Размер пакета обрабатываемых за один раз обучающих примеров.
        По умолчанию составляет 0.5% от обучающей выборки. Если размер меньше 200,
        он автоматически становится равным 200.
    :return: Функция-классификатор. Рекомендуется применять к ней декораторы.
    """
    idl = len(input_data)
    input_data_test = input_data[int(idl * train_amount):]
    input_data_train = input_data[:int(idl * train_amount)]
    features_num = len(input_data_train[0])
    batch_size = batch_size if batch_size else idl * 0.005
    batch_size = batch_size if batch_size > 200 else 200

    rdl = len(result_data)
    result_data_test = result_data[int(rdl * train_amount):]
    result_data_train = result_data[:int(rdl * train_amount)]
    result_data_test = utils.to_categorical(result_data_test, num_cat)
    result_data_train = utils.to_categorical(result_data_train, num_cat)

    if layers:
        for layer in layers:
            model.add(layer)
    else:
        model.add(Dense(features_num, input_dim = features_num, activation = 'relu', kernel_initializer = "normal"))
        model.add(Dense(num_cat, input_dim = num_cat, activation = "softmax", kernel_initializer = "normal"))

    model.compile(loss = loss, optimizer = optimizer, metrics = [metrics])
    model.fit(input_data_train, result_data_train, batch_size = batch_size)

    scores = model.evaluate(input_data_test, result_data_test, verbose = 0)
    print(scores)

    with open('last_model.json', 'w') as f:
        f.write(model.to_json())
    model.save_weights('last_weights.h5')

    return lambda x: model.predict(x)
