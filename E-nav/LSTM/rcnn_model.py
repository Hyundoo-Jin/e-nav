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
import pprint
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

parser =  argparse.ArgumentParser()
parser.add_argument('-l', '--learning_rate', type = float, default = 0.001)
parser.add_argument('-t', '--mode', type = str, default = 'train')
parser.add_argument('-d', '--decay_rate', type = float, default = 0.99)
parser.add_argument('-e', '--total_epoch', type = int, default = 300)
parser.add_argument('-s', '--decay_step', type = int, default = 20)
parser.add_argument('-p', '--dropout_prob', type = float, default = 0.5)
parser.add_argument('-b', '--batch_size', type = int, default = 256)
#parser.add_argument('-m', '--model', type = str)

params = parser.parse_args()

#model = params.model

with open('train_data_all.pickle', 'rb') as f :
    train_data = pickle.load(f)

is_training = (params.mode == 'train')
word_data = train_data['word_based_data']
doc_data = train_data['doc_based_data']
mean_data = train_data['mean_data']
labels = train_data['label']
length = train_data['length']
train_x_placeholder = tf.placeholder(tf.float32, shape = [None, length.max(), 300])
labels_placeholder = tf.placeholder(tf.int64, shape = [None, 1])
seqlen_placeholder = tf.placeholder(tf.int32, shape = [None])

max_step = int(len(word_data) /params.batch_size)

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
    cell = tf.contrib.rnn.DropoutWrapper(tf.nn.rnn_cell.LSTMCell(64), output_keep_prob = params.dropout_prob)
# create a RNN cell composed sequentially of a number of RNNCells
else :
    cell = tf.nn.rnn_cell.LSTMCell(64)

# 'outputs' is a tensor of shape [batch_size, max_time, 256]
# 'state' is a N-tuple where N is the number of LSTMCells containing a
# tf.contrib.rnn.LSTMStateTuple for each cell
outputs, state = tf.nn.dynamic_rnn(cell = cell,
                                   inputs = train_x_placeholder,
                                   sequence_length = seqlen_placeholder,
                                   time_major = False,
                                   dtype = tf.float32)

attention = tf.contrib.seq2seq.BahdanauAttention(num_units = 64, memory = outputs,
                memory_sequence_length = seqlen_placeholder)
attention = tf.contrib.seq2seq.AttentionWrapper(
                cell, attention, attention_layer_size = 64)
outputs = tf.layers.dense(inputs = attention, units = 11, name = 'dense_3', activation = tf.nn.sigmoid)
prediction = tf.argmax(outputs, 1)
accuracy = tf.reduce_mean(tf.cast(tf.equal(labels_placeholder, prediction), tf.float32))
probablity = tf.nn.softmax(outputs, name = 'softmax_tensor')

strat_lr = params.learning_rate
global_step = tf.train.get_or_create_global_step()
learning_rate = tf.train.exponential_decay(params.learning_rate, global_step,
                                   params.decay_step, params.decay_rate, staircase = True)

loss = tf.losses.sparse_softmax_cross_entropy(labels = labels_placeholder, logits = outputs)
optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate)
train_op = optimizer.minimize(loss, global_step = global_step)

t = trange(params.total_epoch)
best_saver = tf.train.Saver(max_to_keep=1)
with tf.Session() as sess :
    sess.run(tf.global_variables_initializer())
    best_acc = 0
    for epoch in t :
        for step in range(max_step) :
            if step == max_step :
                batch_x = train_x[params.batch_size * step : len(train_x)]
                batch_labels = train_label[params.batch_size * step : len(train_x)]
                batch_length = train_length[params.batch_size * step : len(train_x)]
            else :
                batch_x = train_x[params.batch_size * step : params.batch_size * (step + 1)]
                batch_labels = train_label[params.batch_size * step : params.batch_size * (step + 1)]
                batch_length = train_length[params.batch_size * step : params.batch_size * (step + 1)]

            batch_labels = batch_labels.reshape(-1, 1)

            if is_training :
                _, loss_val, att = sess.run([train_op, loss, attention],
                        feed_dict = {train_x_placeholder : batch_x,
                                labels_placeholder : batch_labels,
                                seqlen_placeholder : batch_length})
            acc_val, yhat = sess.run([accuracy, prediction],
                feed_dict = {train_x_placeholder : valid_x,
                        labels_placeholder : valid_label.reshape(-1, 1),
                        seqlen_placeholder : valid_length})
            if acc_val > best_acc :
                best_acc = acc_val
                best_saver.save(sess, os.path.join(os.getcwd(), 'model', 'word_based'))
                att.eval()
            t.set_postfix(best_acc = best_acc, loss = loss_val)

    print(classification_report(valid_label, yhat))
