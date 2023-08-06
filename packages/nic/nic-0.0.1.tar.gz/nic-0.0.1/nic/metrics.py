from nltk.translate.bleu_score import corpus_bleu
import numpy as np
import tensorflow as tf
from tensorflow import keras


def create_loss_object():
    return keras.losses.SparseCategoricalCrossentropy(
        from_logits=True
    )


class Perplexity(keras.metrics.Metric):
    def __init__(self, name="perplexity", weights=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self._cross_entropy = self.add_weight(
            name="cross-entropy",
            initializer="zeros",
            dtype=self.dtype,
        )
        self._total_target_words = self.add_weight(
            name="total-target-words",
            initializer="zeros",
            dtype=tf.int32,
        )

        if (weights is not None):
            h = weights["cross_entropy"]
            ttw = weights["total_target_words"]
            self.set_weights([
                np.array(h) if (isinstance(h, float)) else h,
                np.array(ttw) if (isinstance(ttw, int)) else ttw,
            ])

    def update_state(self, y_true, y_pred, sample_weight=None):
        target_words = tf.math.count_nonzero(
            y_true,
            dtype=self._total_target_words.dtype
        )
        self._total_target_words.assign_add(target_words)

        cross_entropy = create_loss_object()
        loss = cross_entropy(y_true, y_pred)
        self._cross_entropy.assign_add(
            tf.cast(target_words, self._cross_entropy.dtype) * loss
        )

    def result(self):
        total_target_words = tf.cast(self._total_target_words,
                                     self._cross_entropy.dtype)
        return tf.exp(self._cross_entropy / total_target_words)

    def reset_state(self):
        self._total_target_words.assign(0)
        self._cross_entropy.assign(0.0)

    def get_config(self):
        return {"cross_entropy": np.array(self._cross_entropy),
                "total_target_words": np.array(self._total_target_words)}

    @classmethod
    def from_config(cls, config):
        return cls(weights=config)


def bleu_score_of(predicted_sentences, reference_sentences):
    return 100 * corpus_bleu(reference_sentences, predicted_sentences)
