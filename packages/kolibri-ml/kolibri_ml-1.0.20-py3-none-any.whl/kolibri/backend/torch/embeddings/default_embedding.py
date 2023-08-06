
from typing import Any
import torch.nn as nn
import json

from kolibri.backend.base.base_embedding import Embedding



class DefaultEmbedding(Embedding):
    """
    DefaultEmbedding is a random  layer for text sequence embedding,
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

    def load_embed_vocab(self):
        return None

    def build_embedding_model(self, *, vocab_size=None, force=False, **kwargs):
        if self.embed_model is None or force:
            self.embed_model = nn.Embedding(vocab_size, self.embedding_size)


if __name__ == "__main__":
    pass
