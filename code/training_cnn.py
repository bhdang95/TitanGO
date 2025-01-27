from __future__ import print_function

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from dlgo.agent.predict import DeepLearningAgent
from dlgo.agent.predict import load_prediction_agent
from dlgo.encoders.sevenplane import SevenPlaneEncoder
import time
import h5py

np.random.seed(123)
X = np.load('generated_games/features-200.npy')
Y = np.load('generated_games/labels-200.npy')

samples = X.shape[0]
size = 9
input_shape = (size, size, 1)

X = X.reshape(samples, size, size, 1)

train_samples = 10000
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Dropout(rate=0.6))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.6))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(rate=0.6))
model.add(Dense(size * size, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

model.fit(X_train, Y_train,
          batch_size=64,
          epochs=5,
          verbose=1,
          validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])



encoder = SevenPlaneEncoder((19, 19))
dlAgent = DeepLearningAgent(model, encoder)
with h5py.File('cnn_agent.h5', 'w') as dlAgent_out:
	dlAgent.serialize(dlAgent_out)
# time.sleep(15)
