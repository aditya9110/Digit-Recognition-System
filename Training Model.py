import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout, Conv2D, MaxPooling2D
from tensorflow.keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()
# print(X_train.shape, X_test.shape)    #(60000, 28, 28) (10000, 28, 28)
X_train = X_train/255
X_test = X_test/255

for sample in range(len(X_train)):
    for row in range(28):
        for data in range(28):
            if X_train[sample][row][data] != 0:
                X_train[sample][row][data] = 1

for sample in range(len(X_test)):
    for row in range(28):
        for data in range(28):
            if X_test[sample][row][data] != 0:
                X_test[sample][row][data] = 1

X_train = X_train.reshape(60000, 28, 28, 1)
X_test = X_test.reshape(10000, 28, 28, 1)

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
print('Training Initialize....\n')
model.fit(X_train, y_train, epochs=10)

model.save('digit_reader.model')
