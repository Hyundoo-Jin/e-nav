import pandas as pd
import numpy as np
import os
import tensorflow as tf
import collections
import pickle
import datetime
import re

def lstm_layer(is_training, data, params) :
    # create 2 LSTMCells
    with tf.variable_scope('lstm_scope', reuse = tf.AUTO_REUSE) :
        rnn_layers = [tf.nn.rnn_cell.LSTMCell(size) for size in params.lstm_sizes]
        if is_training :
            rnn_layers = [tf.contrib.rnn.DropoutWrapper(lstm, output_keep_prob = params.dropout_prob) for lstm in rnn_layers]
        # create a RNN cell composed sequentially of a number of RNNCells
        multi_rnn_cell = tf.nn.rnn_cell.MultiRNNCell(rnn_layers)

        # 'outputs' is a tensor of shape [batch_size, max_time, 256]
        # 'state' is a N-tuple where N is the number of LSTMCells containing a
        # tf.contrib.rnn.LSTMStateTuple for each cell
        outputs, state = tf.nn.dynamic_rnn(cell = multi_rnn_cell,
                                           inputs = data,
                                           initial_state = multi_rnn_cell.zero_state(params.batch_size, tf.float32),
                                           dtype=tf.float32)
    return outputs, state


def model_fn(mode, inputs, params, reuse=False) :
    is_training = (mode == 'train')
    train_x = inputs['train_x']
    labels = inputs['train_y']
    with tf.variable_scope('model', reuse=reuse):
        # Compute the output distribution of the model and the predictions
        outputs, state = lstm_layer(is_training, train_x, params)

#    logits = tf.contrib.layers.fully_connected(outputs, 1, activation_fn=tf.sigmoid)
    with tf.Session() as sess :
        outputs.eval()
    logits = tf.layers.dense(outputs, units = 18, activation = tf.sigmoid)

    predictions = {
        'classes' : tf.argmax(logits, 0),
        'probabilities' : tf.nn.softmax(logits, name = 'softmax_tensor')
    }

    loss = tf.losses.sparse_softmax_cross_entropy(labels, logits)
    correct_pred = tf.equal(tf.cast(tf.round(logits), tf.int64), labels)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    if is_training :
        strat_lr = params.learning_rate
        global_step = tf.train.get_or_create_global_step()
        learning_rate = tf.train.exponential_decay(params.learning_rate, global_step,
                                           803, 0.99, staircase = True)
        optimizer = tf.train.AdamOptimizer(params.learning_rate)
        train_op = optimizer.minimize(loss, global_step=global_step)

    with tf.variable_scope("metrics"):
        metrics = {
            'accuracy': tf.metrics.accuracy(labels=labels, predictions=tf.argmax(logits, 0)),
            'loss': tf.metrics.mean(loss)
        }

    update_metrics_op = tf.group(*[op for _, op in metrics.values()])

    # Get the op to reset the local variables used in tf.metrics
    metric_variables = tf.get_collection(tf.GraphKeys.LOCAL_VARIABLES, scope="metrics")
    metrics_init_op = tf.variables_initializer(metric_variables)

    # Summaries for training
    tf.summary.scalar('loss', loss)
    tf.summary.scalar('accuracy', accuracy)

    mask = tf.not_equal(labels, tf.cast(tf.round(logits), tf.int64))

    model_spec = inputs
    model_spec['variable_init_op'] = tf.global_variables_initializer()
    model_spec["predictions"] = predictions['classes']
    model_spec['softmax'] = predictions['probabilities']
    model_spec['loss'] = loss
    model_spec['accuracy'] = accuracy
    model_spec['metrics_init_op'] = metrics_init_op
    model_spec['metrics'] = metrics
    model_spec['update_metrics'] = update_metrics_op
    model_spec['summary_op'] = tf.summary.merge_all()

    if is_training:
        model_spec['train_op'] = train_op

    return model_spec
