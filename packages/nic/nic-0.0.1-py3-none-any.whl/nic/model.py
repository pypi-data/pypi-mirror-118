from typing import NamedTuple

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


_DEFAULT_POOLING = "max"


class CustomModel(keras.Model):
    """
    An extended model which is needed due to the format of the data;
    the `fit` logic stays the same.
    """
    def train_step(self, data):
        images, source_captions, target_captions = data

        with tf.GradientTape() as tape:
            y_pred = self([images, source_captions], training=True)
            loss = self.compiled_loss(target_captions,
                                      y_pred,
                                      regularization_losses=self.losses)

        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        self.optimizer.apply_gradients(zip(gradients, trainable_vars))
        self.compiled_metrics.update_state(target_captions, y_pred)

        return {m.name: m.result() for m in self.metrics}

    def test_step(self, data):
        images, source_captions, target_captions = data
        y_pred = self([images, source_captions], training=False)

        self.compiled_loss(target_captions,
                           y_pred,
                           regularization_losses=self.losses)
        self.compiled_metrics.update_state(target_captions, y_pred)

        return {m.name: m.result() for m in self.metrics}


class RNNOptions(NamedTuple):
    """
    Bundles up the configuration options of an RNN module:
     - size: a positive int - the size of the RNN's hidden state
     - dropout: a float in the range (0, 1) - the dropout rate for the
       RNN's inputs. Defaults to 0
     - recurrent_dropout: a float in the range (0, 1) - the dropout rate
       for the RNN's hidden vectors. Defaults to 0; changing this value
       might lead to a significant performance hit
     - reverse_sequence: a boolean value indicating whether the input
       sequence should be fed backwards (end to start) into the RNN.
       Defaults to `False`
     - kernel_initializer: a str - the initializer for the kernel
       weights matrix, used for the linear transformation of the inputs.
       Defaults to "glorot_uniform"
     - recurrent_initializer: a str - the initializer for the
       recurrent_kernel weights matrix, used for the linear
       transformation of the recurrent state. Defaults to "orthogonal"
     - bias_initializer: a str - the initializer for the bias vector.
       Defaults to "zeros"
    """
    size: int
    dropout: float = 0.0
    recurrent_dropout: float = 0.0
    reverse_sequence: bool = False
    kernel_initializer: str = "glorot_uniform"
    recurrent_initializer: str = "orthogonal"
    bias_initializer: str = "zeros"


def define_decoder_model(features_size,
                         vocabulary_size,
                         rnn_options,
                         embedding_size=None,
                         name="nic-decoder"):
    """
    Defines the NIC model without the CNN encoder part.

    :param features_size: a positive int - the size of the features
    vector output by the CNN encoder.
    :param vocabulary_size: a positive int - the size of the vocabulary
    extracted from the train captions.
    :param rnn_options: an instance of RNNOptions to be used to set up
    the RNN module of the model.
    :param embedding_size: an int - the size of word embeddings. If
    omitted or None, defaults to `rnn_options.size`.
    :param name: a str - the name of the resulting model. Defaults to
    `nic-decoder`.
    :returns: a `tf.keras.Model` instance whose inputs are:
     - features: (batch_size, features_size)
     - captions: (batch_size, max_seq_len)
    and whose output is:
     - word projections: (batch_size, max_seq_len, vocabulary_size)
    Use keras.utils.plot_model to view the entire model.
    """
    features_input = layers.Input(shape=(features_size,),
                                  name="image-features")
    # (batch_size, hidden_size)
    transformed_features = layers.Dense(
        rnn_options.size,
        activation="relu",
        name="features-transformation"
    )(features_input)

    captions_input = layers.Input(shape=(None,),
                                  dtype=tf.int32,
                                  name="captions")
    embedding_size = (rnn_options.size
                      if (embedding_size is None)
                      else embedding_size)
    # (batch_size, max_seq_len, embedding_size)
    embedded_captions = layers.Embedding(
        vocabulary_size,
        embedding_size,
        name="word-embedding"
    )(captions_input)

    c_state = tf.zeros_like(transformed_features)
    # (batch_size, max_seq_len, hidden_size)
    # (batch_size, hidden_size)
    decoded_captions, h_state, c_state = layers.LSTM(
        rnn_options.size,
        kernel_initializer=rnn_options.kernel_initializer,
        recurrent_initializer=rnn_options.recurrent_initializer,
        bias_initializer=rnn_options.bias_initializer,
        dropout=rnn_options.dropout,
        recurrent_dropout=rnn_options.recurrent_dropout,
        go_backwards=rnn_options.reverse_sequence,
        return_sequences=True,
        return_state=True,
        name="rnn-decoder"
    )(embedded_captions, initial_state=[transformed_features, c_state])

    # (batch_size, max_seq_len, hidden_size)
    transformed_captions = layers.Dense(
        rnn_options.size,
        activation="relu",
        name="pre-projection-transformation"
    )(decoded_captions)

    # (batch_size, max_seq_len, vocabulary_size)
    word_projection = layers.Dense(
        vocabulary_size,
        activation="relu",
        name="word-projection"
    )(transformed_captions)

    return CustomModel(inputs=[features_input, captions_input],
                       outputs=word_projection,
                       name=name)


def define_encoder_model(pooling=None):
    """
    Defines and returns the CNN encoder part of the NIC model which is
    Inception ResNet v2 trained on ImageNet with the top layer removed
    and max or average pooling applied so that the output is a vector.

    :param pooling: a str - the pooling to apply after the last
    convolutional layer. Can be `'max'` (the default) or `'avg'`.
    :returns: a `tf.keras.Model` whose input is a preprocessed image
    of shape (299, 299, 3) and whose output is a features vector of
    shape (1536,).
    """
    if (pooling is None):
        pooling = _DEFAULT_POOLING

    image_encoder = \
        tf.keras.applications.inception_resnet_v2.InceptionResNetV2(
            include_top=False,
            weights="imagenet",
            pooling=pooling
        )
    return tf.keras.Model(image_encoder.input,
                          image_encoder.layers[-1].output,
                          name="inception-resnet-v2")


def connect(decoder_model, *,
            image_shape,
            encoder_model=None,
            name="nic"):
    """
    Conntects the entire NIC model.

    :param decoder_model: the decoder model, defined with
    `define_decoder_model`.
    :param image_shape: a three-tuple of ints - the shape of the input
    images, as expected by the encoder model.
    :param encoder_model: the encoder model which is assumed to work on
    image tensors and to return a single vector for each image - the
    features corresponding to the image. If `None` (the default), or
    str, this is the model defined by
    `define_encoder_model(pooling=encoder_model)`.
    :param name: a str - the name of the resulting model.
    :returns: a `tf.keras.Model` whose inputs are:
     - images: (batch_size, image_shape...)
     - captions: (batch_size, max_seq_len)
    and whose output is:
     - word projections: (batch_size, max_seq_len, vocabulary_size)
    Use keras.utils.plot_model to view the entire model.
    """
    if (encoder_model is None or isinstance(encoder_model, str)):
        encoder_model = define_encoder_model(
            pooling=encoder_model
        )

    images = layers.Input(shape=image_shape,
                          name="images-input")
    captions = layers.Input(shape=(None,),
                            dtype=tf.int32,
                            name="captions-input")
    features = encoder_model(images)
    word_projection = decoder_model([features, captions])

    return CustomModel(
        inputs=[images, captions],
        outputs=word_projection,
        name=name
    )


def define_model(vocabulary_size,
                 rnn_options,
                 embedding_size=None,
                 pooling=None):
    """
    Defines the whole NIC model.

    :param vocabulary_size: a positive int - the size of the vocabulary
    extracted from the train data.
    :param rnn_options: an instance of RNNOptions describing the RNN
    module of the model.
    :param embedding_size: an int - the size of word embeddings. If
    omitted or None, defaults to `rnn_options.size`.
    :param pooling: a str - the type of pooling to apply to the last
    convolutional layer of the encoder. See `define_encoder_model`.
    Defaults to `None`.
    :returns: a `tf.keras.Model` whose inputs are:
     - images: (batch_size, 299, 299, 3)
     - captions: (batch_size, max_seq_len)
    and whose output is:
     - word projections: (batch_size, max_seq_len, vocabulary_size)
    Use keras.utils.plot_model to view the entire model.
    """
    encoder = define_encoder_model(pooling)
    features_size = encoder.layers[-1].output_shape[-1]
    decoder = define_decoder_model(
        features_size,
        vocabulary_size,
        rnn_options,
        embedding_size,
        name="nic-decoder"
    )

    return connect(decoder,
                   image_shape=(299, 299, 3),
                   encoder_model=encoder)
