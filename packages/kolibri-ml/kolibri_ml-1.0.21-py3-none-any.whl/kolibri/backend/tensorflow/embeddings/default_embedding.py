
from typing import Any
import tensorflow as tf
from tensorflow import keras
import json
from kolibri.backend.tensorflow import custom_objects

from kolibri.backend.base.base_embedding import Embedding

L = keras.layers


class DefaultEmbedding(Embedding):
    """
    DefaultEmbedding is a random init `tf.keras.layers.Embedding` layer for text sequence embedding,
    which is the defualt embedding class for dnn models.
    """

    def __init__(self,
                 embedding_size: int = 100, input_length=None, name=f'input',
                 **kwargs: Any):
        """

        Args:
            embedding_size: Dimension of the dense embedding.
            kwargs: additional params
        """
        self.embedding_size: int = embedding_size
        super(DefaultEmbedding, self).__init__(embedding_size=embedding_size,
                                               **kwargs)
        self.input_length = input_length
        self.name = name

    def _override_load_model(self, config):
        embed_model_json_str = json.dumps(config['embed_model'])
        self.embed_model = tf.keras.models.model_from_json(embed_model_json_str,
                                                           custom_objects=custom_objects)

    def to_dict(self):
        emb_json_str=super().to_dict()
        emb_json_str['embed_model']= json.loads(self.embed_model.to_json())
        return emb_json_str

    def load_embed_vocab(self):
        return None

    def build_embedding_model(self, *, vocab_size=None, force=False, **kwargs):
        if self.embed_model is None or force:
            if self.input_length:
                self.input_tensor = L.Input(shape=(None, self.input_length),
                                            name=self.name)
            else:
                self.input_tensor = L.Input(shape=(None,),
                                            name=self.name)

            layer_embedding = L.Embedding(vocab_size,
                                          self.embedding_size,
                                          input_length=self.input_length,
                                          mask_zero=True,
                                          name=self.name + f'_layer_embedding')

            self.embedded_tensor = layer_embedding(self.input_tensor)
            self.embed_model = keras.Model(self.input_tensor, self.embedded_tensor)


if __name__ == "__main__":
    pass
