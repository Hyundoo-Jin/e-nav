"""Create the input data pipeline using `tf.data`"""

import tensorflow as tf
import pickle
import numpy as np


def input_fn(is_training, filenames, labels, params):
    num_samples = len(filenames)
    assert len(filenames) == len(labels), "Filenames and labels should have same length"

    # Create a Dataset serving batches of images and labels
    # We don't repeat for multiple epochs because we always train and evaluate for one epoch
    embeddings = []
    label_list = []
    for filename in filenames :
        with open(filename, 'rb') as f :
            temp = pickle.load(f)
            embeddings.append(temp['data'].T.reshape(-1, 100))
            label_list.append(temp['label'])

#    embeddings = np.array(embeddings, dtype = np.float32)
    label_list = np.array(label_list, dtype = np.int64)


    if is_training:
        dataset = (tf.data.Dataset.from_tensor_slices(
                    (tf.constant(embeddings), tf.constant(label_list)))
            .shuffle(num_samples)  # whole dataset into the buffer ensures good shuffling
#            .map(parse_fn, num_parallel_calls=params.num_parallel_calls)
            .batch(params.batch_size)
            .prefetch(1)  # make sure you always have one batch ready to serve
        )
    else:
        dataset = (tf.data.Dataset.from_tensor_slices((tf.constant(embeddings), tf.constant(label_list)))
#            .map(parse_fn, num_parallel_calls=params.num_parallel_calls)
            .batch(params.batch_size)
            .prefetch(1)  # make sure you always have one batch ready to serve
        )

    # Create reinitializable iterator from dataset
    iterator = dataset.make_one_shot_iterator()
    vector, labels = iterator.get_next()
    iterator_init_op = iterator.initializer

    inputs = {'train_x': vector, 'train_y': labels, 'iterator_init_op': iterator_init_op}
    return inputs
