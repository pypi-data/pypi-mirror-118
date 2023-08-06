import torch
from torch import nn
from kolibri.backend.torch.models.text.classification.base_model import TorchBaseTextClassificationModel

import torch.nn.functional as F

class FastText(TorchBaseTextClassificationModel):

    def __init__(self, params):
        super(FastText, self).__init__(hyper_parameters=params)
        self.nn_model=nn.Module()

    def build_model_arc(self):
        output_dim = self.label_indexer.vocab_size
        config = self.hyper_parameters 
        # embedding layer

        emb_size=self.embedding.embedding_size
        hidden_size=config['hidden-size']
        # hidden layer
        self.nn_model.hidden = nn.Linear(emb_size, hidden_size)

        # output layer
        self.nn_model.fc = nn.Linear(hidden_size, output_dim)

        self.nn_model.forward=self.forward

    @classmethod
    def get_default_hyper_parameters(cls):
        return {
            'hidden-size': 20,
            'layer-output': {
            }
        }



    def forward(self, text):
        """
        Parameters
        ----------
        text : torch.Tensor (batch_size, word_pad_len)
            Input data

        words_per_sentence : torch.Tensor (batch_size)
            Sentence lengths

        Returns
        -------
        scores : torch.Tensor (batch_size, n_classes)
            Class scores
        """
        # word embedding
        embeddings = self.embedding.embed_model(text)  # (batch_size, word_pad_len, emb_size)

        # average word embeddings in to sentence erpresentations
        avg_embeddings = embeddings.mean(dim=1).squeeze(1)  # (batch_size, emb_size)
        hidden = self.nn_model.hidden(avg_embeddings)  # (batch_size, hidden_size)

        # compute probability
        scores = self.nn_model.fc(hidden)  # (batch_size, n_classes)

        return F.softmax(scores)
