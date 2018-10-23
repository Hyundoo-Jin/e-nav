import pandas as pd
import numpy as np
import os
import tensorflow as tf
import collections
import pickle
import datetime
import re
from tqdm import trange
import argparse
from sklearn.metrics import classification_report

def _weight_variable(layer_name, shape):
    init = tf.random_normal_initializer(mean=0.0, stddev=0.01)
    return tf.get_variable(
        layer_name + "_w", shape=shape,
        initializer=init)

def _bias_variable(layer_name, shape):
    init = tf.constant_initializer(value=shape)
    return tf.get_variable(
        layer_name + "_bias", shape=shape,
        initializer=init)

with open('train_data.pickle', 'rb') as f :
    train_data = pickle.load(f)

is_training = True
word_data = train_data['data']
labels = train_data['label']
labels = np.array(labels)
length = train_data['length']
length = np.array(length)

train_x_placeholder = tf.placeholder(tf.float32, shape = [None, 20, 100])
labels_placeholder = tf.placeholder(tf.int64, shape = [None, 1])
seqlen_placeholder = tf.placeholder(tf.int32, shape = [None])

batch_size = 128
dropout_prob = 0.5

max_step = int(len(word_data) /batch_size)

train_index = np.random.choice(len(word_data), int(len(word_data) * 0.7), replace=False)
valid_index = np.arange(len(word_data))
valid_index = np.delete(valid_index, train_index)

train_x = word_data[train_index]
valid_x = word_data[valid_index]
train_label = labels[train_index]
valid_label = labels[valid_index]
train_length = length[train_index]
valid_length = length[valid_index]

if is_training :
    cell = tf.contrib.rnn.DropoutWrapper(tf.nn.rnn_cell.LSTMCell(100), output_keep_prob = dropout_prob)
    cell2 = tf.contrib.rnn.DropoutWrapper(tf.nn.rnn_cell.LSTMCell(64), output_keep_prob = dropout_prob)
# create a RNN cell composed sequentially of a number of RNNCells
else :
    cell = tf.nn.rnn_cell.LSTMCell(100)
    cell2 = tf.nn.rnn_cell.LSTMCell(64)

# 'outputs' is a tensor of shape [batch_size, max_time, 256]
# 'state' is a N-tuple where N is the number of LSTMCells containing a
# tf.contrib.rnn.LSTMStateTuple for each cell
with tf.variable_scope('lstm_1', reuse=tf.AUTO_REUSE):
    outputs, state = tf.nn.dynamic_rnn(cell = cell,
                                       inputs = train_x_placeholder,
    #                                   sequence_length = seqlen_placeholder,
                                       time_major = False,
                                       dtype = tf.float32)

with tf.variable_scope('lstm_2', reuse=tf.AUTO_REUSE):
    outputs2, state2 = tf.nn.dynamic_rnn(cell = cell2,
                                       inputs = outputs,
    #                                   sequence_length = seqlen_placeholder,
                                       time_major = False,
                                       dtype = tf.float32)

layer_name = 'dense_1'
with tf.variable_scope(layer_name, reuse=tf.AUTO_REUSE):
    w_f1 = _weight_variable(layer_name, [64, 32])
    b_f1 = _bias_variable(layer_name, [32])
    tensor = tf.nn.bias_add(tf.matmul(outputs2[:, -1], w_f1), b_f1)
    tensor = tf.nn.sigmoid(tensor)
    if is_training:
        tensor = tf.nn.dropout(tensor, keep_prob=dropout_prob)

# layer_name = 'dense_2'
# with tf.variable_scope(layer_name, reuse=tf.AUTO_REUSE):
#     w_f2 = _weight_variable(layer_name, [32, 16])
#     b_f2 = _bias_variable(layer_name, [16])
#     tensor = tf.nn.bias_add(tf.matmul(tensor, w_f2), b_f2)
#     tensor = tf.nn.sigmoid(tensor)
#     if is_training:
#         tensor = tf.nn.dropout(tensor, keep_prob=dropout_prob)

tensor = tf.layers.dense(inputs = tensor, units = 11, name = 'dense_3', activation = tf.nn.sigmoid)
prediction = tf.argmax(tensor, 1)
accuracy = tf.reduce_mean(tf.cast(tf.equal(labels_placeholder, prediction), tf.float32))
probablity = tf.nn.softmax(tensor, name = 'softmax_tensor')

strat_lr = 0.001
global_step = tf.train.get_or_create_global_step()
learning_rate = tf.train.exponential_decay(strat_lr, global_step,
                                   int(len(train_index)/10), 0.99, staircase = True)

loss = tf.losses.sparse_softmax_cross_entropy(labels = labels_placeholder, logits = tensor)
optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate)
train_op = optimizer.minimize(loss, global_step = global_step)

t = trange(1000)
best_saver = tf.train.Saver(max_to_keep=1)
final_output = []
with tf.Session() as sess :
    sess.run(tf.global_variables_initializer())
    best_acc = 0
    for epoch in t :
        avg_loss = 0
        for step in range(max_step) :
            if step == max_step :
                batch_x = train_x[batch_size * step : len(train_x)]
                batch_labels = train_label[batch_size * step : len(train_x)]
                batch_length = train_length[batch_size * step : len(train_x)]
            else :
                batch_x = train_x[batch_size * step : batch_size * (step + 1)]
                batch_labels = train_label[batch_size * step : batch_size * (step + 1)]
                batch_length = train_length[batch_size * step : batch_size * (step + 1)]

            batch_labels = batch_labels.reshape(-1, 1)

            if is_training :
                _, loss_val = sess.run([train_op, loss],
                        feed_dict = {train_x_placeholder : batch_x,
                                labels_placeholder : batch_labels,
                                seqlen_placeholder : batch_length})
                avg_loss += loss_val
        avg_loss = avg_loss / max_step
        val_acc, yhat = sess.run([accuracy, prediction],
            feed_dict = {train_x_placeholder : valid_x,
                    labels_placeholder : valid_label.reshape(-1, 1),
                    seqlen_placeholder : valid_length})
        if avg_acc > best_acc :
            best_acc = avg_acc
            best_saver.save(sess, os.path.join(os.getcwd(), 'model', 'word_based'))
        t.set_postfix(best_acc = val_acc, loss = loss_val)
        print(classification_report(valid_label, yhat))
