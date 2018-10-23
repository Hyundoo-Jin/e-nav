import pandas as pd
import numpy as np
import os
import tensorflow as tf
import collections
import pickle
import datetime
import re
def make_cell():
  return tf.nn.rnn_cell.LSTMCell(64, state_is_tuple=True)

def lstm(is_training, data, params) :
    with tf.variable_scope('lstm_scope', reuse = tf.AUTO_REUSE) :
        if is_training :
            cell = tf.contrib.rnn.DropoutWrapper(tf.nn.rnn_cell.LSTMCell(64, state_is_tuple=True), output_keep_prob = params.dropout_prob)
        # create a RNN cell composed sequentially of a number of RNNCells
        cell = tf.nn.rnn_cell.LSTMCell(64, state_is_tuple=True)

        # 'outputs' is a tensor of shape [batch_size, max_time, 256]
        # 'state' is a N-tuple where N is the number of LSTMCells containing a
        # tf.contrib.rnn.LSTMStateTuple for each cell
        outputs, state = tf.nn.dynamic_rnn(cell = cell,
                                           inputs = data,
#                                           initial_state = cell.zero_state(params.batch_size, tf.float32),
                                    #       sequence_length = length,
                                           dtype = tf.float32,
                                           )

    return outputs, state
