#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
KWS model training script.
"""

import os
import pickle

from tensorflow.keras.utils import to_categorical, get_file

from cnn2snn import load_quantized_model, quantize_layer

from ..cyclic_lr import CyclicLR
from ..training import get_training_parser, compile_model, evaluate_model


def get_data():
    """ Loads KWS data.

    Returns:
        tuple: train data, train labels, validation data and validation labels
    """
    # Input scaling: Akida is configured to take 8-bit inputs without rescaling
    # but for the training, we use float weights between 0 and 1
    a = 255
    b = 0

    # Load pre-processed dataset
    fname = get_file(
        fname='kws_preprocessed_all_words_except_backward_follow_forward.pkl',
        origin=
        'http://data.brainchip.com/dataset-mirror/kws/kws_preprocessed_all_words_except_backward_follow_forward.pkl',
        cache_subdir=os.path.join('datasets', 'kws'))

    print('Loading pre-processed dataset...')
    with open(fname, 'rb') as f:
        [x_train_ak, y_train, x_val_ak, y_val, _, _, _, _] = pickle.load(f)

    # For cnn2snn Keras training, data must be scaled (usually to [0,1])
    x_train_keras = \
        (x_train_ak.astype('float32') - b) / a
    x_val_keras = \
        (x_val_ak.astype('float32') - b) / a

    return x_train_keras, y_train, x_val_keras, y_val


def train_model(model, x_train, y_train, x_val, y_val, batch_size, epochs):
    """ Trains the model.

    Args:
         model (tf.keras.Model): the model to train
        x_train (numpy.ndarray): train data
        y_train (numpy.ndarray): train labels
        x_val (numpy.ndarray): validation data
        y_val (numpy.ndarray): validation labels
        batch_size (int): the batch size
        epochs (int): the number of epochs
    """
    # Warn user if number of epochs is not a multiple of 8
    if epochs % 8:
        print("WARNING: for better performance, the number of epochs "
              f" must be a multiple of 8; got 'epochs' = {epochs}")

    # Training parameters (cyclical learning rate)
    scaler = 4
    base_lr = 5e-6
    max_lr = 2e-3

    # Cyclical learning rate
    callbacks = []
    clr = CyclicLR(base_lr=base_lr,
                   max_lr=max_lr,
                   step_size=scaler * x_train.shape[0] / batch_size,
                   mode='triangular')
    callbacks.append(clr)

    history = model.fit(x_train,
                        to_categorical(y_train),
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(x_val, to_categorical(y_val)),
                        callbacks=callbacks)
    print(history.history)


def main():
    """ Entry point for script and CLI usage.
    """
    parsers = get_training_parser(batch_size=100, global_batch_size=False)

    train_parser = parsers[2]
    train_parser.add_argument("-laq",
                              "--last_activ_quantization",
                              type=int,
                              default=None,
                              help="The last layer activation quantization")

    args = parsers[0].parse_args()

    # Load the source model
    model = load_quantized_model(args.model)

    # If specified, change the last layer activation bitwidth
    if "last_activ_quantization" in args and args.last_activ_quantization:
        model = quantize_layer(model, 'separable_6_relu',
                               args.last_activ_quantization)

    # Compile model
    compile_model(model, learning_rate=2e-3)

    # Load data
    x_train, y_train, x_val, y_val = get_data()

    # Train model
    if args.action == "train":
        train_model(model, x_train, y_train, x_val, y_val, args.batch_size,
                    args.epochs)

        # Save model in Keras format (h5)
        if args.savemodel:
            model.save(args.savemodel, include_optimizer=False)
            print(f"Trained model saved as {args.savemodel}")

    elif args.action == "eval":
        # Evaluate model accuracy
        evaluate_model(model, x_val, y=to_categorical(y_val))


if __name__ == "__main__":
    main()
