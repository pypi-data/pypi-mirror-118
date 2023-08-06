import time
from typing import Optional, Dict
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
import numpy as np
from kolibri.logger import get_logger
logger = get_logger(__name__)

from kolibri.backend.torch.tools import AverageMeter, save_checkpoint, clip_gradient, adjust_learning_rate
from kolibri.backend.torch.models.base_model import TorchBaseModel
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TorchBaseTextClassificationModel(TorchBaseModel):
    """
    Training pipeline

    Parameters
    ----------
    num_epochs : int
        We should train the model for __ epochs

    start_epoch : int
        We should start training the model from __th epoch

    train_loader : DataLoader
        DataLoader for training data

    model : nn.Module
        Model

    model_name : str
        Name of the model

    loss_function : nn.Module
        Loss function (cross entropy)

    optimizer : optim.Optimizer
        Optimizer (Adam)

    lr_decay : float
        A factor in interval (0, 1) to multiply the learning rate with

    dataset_name : str
        Name of the dataset

    word_map : Dict[str, int]
        Word2id map

    grad_clip : float, optional
        Gradient threshold in clip gradients

    print_freq : int
        Print training status every __ batches

    checkpoint_path : str, optional
        Path to the folder to save checkpoints

    checkpoint_basename : str, optional, default='checkpoint'
        Basename of the checkpoint

    tensorboard : bool, optional, default=False
        Enable tensorboard or not?

    log_dir : str, optional
        Path to the folder to save logs for tensorboard
    """

    __task__ = 'classification'

    def to_dict(self) -> Dict:
        info = super(TorchBaseTextClassificationModel, self).to_dict()
        info['config']['multi_label'] = self.multi_label
        return info

    def __init__(self, hyper_parameters={}, embedding=None, sequence_length=None, multi_label: bool = False,
                     content_indexer=None, label_indexer=None):
            """

            Args:
                hyper_parameters: hyper_parameters to overwrite
                embedding: embedding object
                sequence_length: target sequence length_train
                multi_label: is multi-label classification
                content_indexer: text processor
                label_indexer: label processor
            """
            super().__init__(hyper_parameters, embedding, sequence_length, multi_label, content_indexer, label_indexer)
            #        self.hyper_parameters = ()
            # combine with base class hyperparameters

            self.hyper_parameters.update(self.get_default_hyper_parameters())

            if hyper_parameters:
                self.update_hyper_parameters(hyper_parameters)

    def predict_proba(self, x_data, *,
                batch_size: int = 32,
                multi_label_threshold: float = 0.5,
                predict_kwargs: Dict = None):
        """
        Generates output predictions for the input samples.

        Computation is done in batches.

        Args:
            x_data: The input texts, as a Numpy array (or list of Numpy arrays if the model has multiple inputs).
            batch_size: Integer. If unspecified, it will default to 32.
            truncating: remove values from sequences larger than `model.embedding.sequence_length`
            multi_label_threshold:
            predict_kwargs: arguments passed to ``predict()`` function of ``tf.keras.Model``

        Returns:
            array(s) of predictions.
        """
        if predict_kwargs is None:
            predict_kwargs = {}

        tensor = self.content_indexer.transform(x_data, )
        logger.debug(f'predict input shape {np.array(tensor).shape}')

        with torch.no_grad():
            pred = self.nn_model(torch.from_numpy(tensor), **predict_kwargs).numpy()

        logger.debug(f'predict output shape {pred.shape}')
        sorted_indices = np.fliplr(np.argsort(pred, axis=1))
        if self.multi_label:
            multi_label_binarizer = self.label_indexer.multi_label_binarizer  # type: ignore
            labels = multi_label_binarizer.inverse_transform(pred,
                                                                 threshold=multi_label_threshold)
        else:
            labels = np.array([self.label_indexer.inverse_transform(p) for p in sorted_indices])

        return pred, labels, pred[np.arange(pred.shape[0])[:, None], sorted_indices]

    def build_model_generator(self, generators):
        if not self.content_indexer.vocab2idx:
            self.content_indexer.build_vocab_generator(generators)

        self.label_indexer.build_vocab_generator(generators)
        self.embedding.setup_text_processor(self.content_indexer)

        if self.sequence_length is None:
            self.sequence_length = self.embedding.get_seq_length_from_corpus(generators)

        self.build_model_arc()
