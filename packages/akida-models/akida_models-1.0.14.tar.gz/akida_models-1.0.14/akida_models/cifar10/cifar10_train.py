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
Training script for CIFAR10 models.
"""

from tensorflow.keras.datasets import cifar10
from tensorflow.keras.callbacks import LearningRateScheduler, EarlyStopping
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from cnn2snn import load_quantized_model

from ..training import get_training_parser, compile_model, evaluate_model


def get_data():
    """ Loads CIFAR10 data.

    Returns:
        tuple: train data, train labels, test data and test labels
    """
    # Input scaling: Akida is configured to take 8-bit inputs without rescaling
    # but for the training, we use float weights between 0 and 1
    a = 255
    b = 0

    #The data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # Convert class vectors to binary class matrices.
    # For hinge loss, we need to rescale them between -1 and 1
    y_train = to_categorical(y_train, 10) * 2 - 1
    y_test = to_categorical(y_test, 10) * 2 - 1

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    # Rescale inputs for Keras
    x_train = (x_train - b) / a
    x_test = (x_test - b) / a

    return x_train, y_train, x_test, y_test


def train_model(model, x_train, y_train, x_test, y_test, batch_size, epochs):
    """ Trains the model.

    Args:
        model (tf.keras.Model): the model to train
        x_train (numpy.ndarray): train data
        y_train (numpy.ndarray): train labels
        x_test (numpy.ndarray): test data
        y_test (numpy.ndarray): test labels
        batch_size (int): the batch size
        epochs (int): the number of epochs
    """

    callbacks = []

    # Learning rate: be more aggressive at the beginning, and apply decay
    lr_start = 1e-3
    lr_end = 1e-4
    lr_decay = (lr_end / lr_start)**(1. / epochs)

    lr_scheduler = LearningRateScheduler(lambda e: lr_start * lr_decay**e)
    callbacks.append(lr_scheduler)

    # Use data augmentation
    datagen_args = {}
    # random hz image shift (fraction of width)
    datagen_args['width_shift_range'] = 0.1
    # random vert image shft (fraction of height)
    datagen_args['height_shift_range'] = 0.1
    # Randomly flip images
    datagen_args['horizontal_flip'] = True

    datagen = ImageDataGenerator(**datagen_args)

    training_data = datagen.flow(x_train, y_train, batch_size=batch_size)

    history = model.fit(training_data,
                        steps_per_epoch=len(x_train) / batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(x_test, y_test),
                        callbacks=callbacks)
    print(history.history)


def tune_model(model, x_train, y_train, x_test, y_test, batch_size, epochs):
    """ Tunes the model.

    Similar to train but with a lower learning rate.

    Args:
        model (tf.keras.Model): the model to train
        x_train (numpy.ndarray): train data
        y_train (numpy.ndarray): train labels
        x_test (numpy.ndarray): test data
        y_test (numpy.ndarray): test labels
        batch_size (int): the batch size
        epochs (int): the number of epochs
    """
    # Early stop when loss has stopped decreasing
    callbacks = []
    es = EarlyStopping(monitor='loss',
                       mode='min',
                       patience=20,
                       restore_best_weights=True)
    callbacks.append(es)

    history = model.fit(x_train,
                        y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(x_test, y_test),
                        callbacks=callbacks)
    print(history.history)


def main():
    """ Entry point for script and CLI usage.
    """
    parser = get_training_parser(batch_size=500,
                                 tune=True,
                                 global_batch_size=False)[0]
    args = parser.parse_args()

    # Load the source model
    model = load_quantized_model(args.model)

    # Compile model
    learning_rate = 1e-3
    if args.action == "tune":
        learning_rate = 1e-4

    compile_model(model, learning_rate=learning_rate, loss='squared_hinge')

    # Load data
    x_train, y_train, x_test, y_test = get_data()

    # Train or tune
    if args.action in ["train", "tune"]:
        if args.action == "train":
            train_model(model, x_train, y_train, x_test, y_test,
                        args.batch_size, args.epochs)
        else:
            tune_model(model, x_train, y_train, x_test, y_test, args.batch_size,
                       args.epochs)

        # Save Model in Keras format (h5)
        if args.savemodel:
            model.save(args.savemodel, include_optimizer=False)
            print(f"Trained model saved as {args.savemodel}")

    elif args.action == "eval":
        # Evaluate model accuracy
        evaluate_model(model, x_test, y=y_test)


if __name__ == "__main__":
    main()
