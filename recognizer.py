import tensorflow as tf
import os
from keras.backend.tensorflow_backend import set_session
config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
#config.gpu_options.allocator_type = 'BFC' #A "Best-fit with coalescing" algorithm, simplified from a version of dlmalloc.
#config.gpu_options.per_process_gpu_memory_fraction = 0.9
config.gpu_options.allow_growth = True
tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"  
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import GRU
from keras import optimizers


from data_loader import load_data
import numpy as np





max_features = 1024

model = Sequential()

model.add(GRU(256,return_sequences=True))
model.add(Dropout(0.5))
model.add(GRU(128))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
 
model.add(Dense(5, activation='softmax'))
adam = optimizers.Adam(lr=0.0001)
model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=['accuracy'])
train_X, train_Y ,test_X, test_Y = load_data()
model.fit(train_X, train_Y, batch_size=16, epochs=100)
model.summary()

score = model.evaluate(test_X, test_Y, batch_size=10)
print("Test loss:", score[0])
print("Test accuracy:", score[1])
pred = model.predict(test_X[0:10,:,:])
print(pred)
print(test_Y[0:10,:])

pred = model.predict(test_X[30:38,:,:])
print(pred)
print(test_Y[30:38,:])
