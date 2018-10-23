# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
import tensorflow as tf
import os
from PIL import Image
import numpy as np

# import tflearn.datasets.oxflower17 as oxflower17

def load_data():
    X = []
    Y = []
    for file_type in ['pos']:
        for img in os.listdir(file_type):
            current_img_path = str(file_type) + '/' + str(img)
            X_sample = np.array(Image.open(current_img_path).resize((227,227)))
            X.append(X_sample)
    k = len(X)
    for i in range(k):
        Y.append([1,0]) # [1,0] pos and [0,1] neg
    # pos sample load done
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            current_img_path = str(file_type) + '/' + str(img)
            X_sample = np.array(Image.open(current_img_path).resize((227,227)))
            X.append(X_sample)
    for i in range(len(X)-k):
        Y.append([0,1])
    # neg sample load done
    X = np.array(X)
    Y = np.array(Y)
    return X, Y


def build_network():
# Building 'AlexNet'
    network = input_data(shape=[None, 227, 227, 3])
    network = conv_2d(network, 96, 11, strides=4, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_2d(network, 256, 5, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_2d(network, 384, 3, activation='relu')
    network = conv_2d(network, 384, 3, activation='relu')
    network = conv_2d(network, 256, 3, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, 17, activation='softmax')
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=0.001)
    return network

# Training
# num_cores=4,gpu_memory_fraction=0.5
# , checkpoint_path='model_alexnet',
#                         max_checkpoints=1, tensorboard_verbose=2
def train_save_CNN(network, X, Y):
    tflearn.init_graph()
    with tf.device('/gpu:0'):
        model = tflearn.DNN(network)
        model.fit(X, Y, n_epoch=1000, validation_set=0.1, shuffle=True,
                show_metric=True, batch_size=64, snapshot_step=200,
                snapshot_epoch=False, run_id='alexnet_oxflowers17')
        model.save(os.getcwd()+'/model/17flowers_model')

def load_predict_model(network, img):
    out = img.resize((227,227))
    out = np.array(out)
    model = tflearn.DNN(network)
    model.load(os.getcwd()+'/model/17flowers_model')
    result = model.predict([out])
    print(result)
    idx = np.where(result==np.max(result))
    print(np.max(result), idx[1])

# model.load('path')
# model.predict([x]) the input have to be a list
def train_CNN():
    X, Y = load_data()
    network = build_network()
    train_save_CNN(network, X, Y)

def main():
    network = build_network()
    img = Image.open(os.getcwd()+'/sunflower.jpg')
    load_predict_model(network, img)

if __name__ == '__main__':
    main()