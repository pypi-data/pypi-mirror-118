import json
import os
import pathlib
import tempfile
import time
from abc import abstractmethod
from typing import Dict, Any
from kdmt.dict import nested_dict_has_key, nested_dict_set_key_value, nested_dict_get_key_path
from kolibri.indexers.sequence_indexer import SequenceIndexer
from kolibri.data.generators import DataGenerator
from kolibri.backend.tensorflow.data.generators import TFDataset
import kolibri.version
from kolibri.indexers.label_indexer import LabelIndexer
from kolibri.logger import get_logger
from kolibri.backend.base.base_embedding import Embedding

logger = get_logger(__name__)


class BaseModel(object):

    def __init__(self, hyper_parameters={}, embedding=None, sequence_length=None, multi_label=False,content_indexer=None, label_indexer=None):

        self.hyper_parameters = self.get_default_hyper_parameters()
        # combine with base class hyperparameters
        self.hyper_parameters.update(BaseModel.get_default_hyper_parameters())

        if hyper_parameters:
            self.update_hyper_parameters(hyper_parameters)

        if embedding is None:
            embedding = Embedding()  # type: ignore
        if content_indexer is None:
            content_indexer = SequenceIndexer()

        self.content_indexer = content_indexer
        self.embedding = embedding

        self.epoch = 0
        self.nn_model = None
        self.checkpoint_model_path = ""
        self.sequence_length: int
        self.sequence_length = sequence_length
        self.multi_label = multi_label
        if label_indexer is None:
            self.label_indexer = LabelIndexer(multi_label=multi_label)


    def to_dict(self):


        return {
            'kolibri_version': kolibri.version.__version__,
            'label_indexer': self.label_indexer.to_dict(),
            'embedding': self.embedding.to_dict(),  # type: ignore
            'content_indexer': self.content_indexer.to_dict(),
            '__class_name__': self.__class__.__name__,
            '__module__': self.__class__.__module__,
            'epoch': self.epoch,
            'config': {
                'hyper_parameters': self.hyper_parameters,  # type: ignore
            }
        }

    def update_hyper_parameters(self, parameters):
        if self.hyper_parameters is None:
            return

        for k, v in parameters.items():
            if nested_dict_has_key(k, self.hyper_parameters):
                key=nested_dict_get_key_path(k,self.hyper_parameters)
                nested_dict_set_key_value(key, self.hyper_parameters, v)

    @classmethod
    def get_default_hyper_parameters(cls):

        return {
            'save-best': False,
            'early-stop': False,
            'monitor': 'val_accuracy',
            'mode': 'max',
            'early-stopping-patience': 3,
            'epochs': 2,
            'batch-size':32,
            'warm-up': False,
            'shuffle': True,
            'warmup': True,
            'optimizer': 'adam',
            'loss': 'sparse_categorical_crossentropy',
            'metrics': ['accuracy'],
            'model-path':"",
            "learning-rate":1e-4,
            "momentum": 0.5,
            'display_gpu_info': False
        }

    def fit(self, x_train, y_train, x_validate=None, y_validate=None, callbacks=None, fit_kwargs={}):
        raise NotImplementedError

    def build_model_generator(self, generators):
        raise NotImplementedError

    def fit_generator(self, train_sample_gen, valid_sample_gen=None, callbacks=None, fit_kwargs={}):
        raise NotImplementedError


    def save(self, model_path: str) -> str:
        """
        Save model
        Args:
            model_path:
        """
        pathlib.Path(model_path).mkdir(exist_ok=True, parents=True)
        model_path = os.path.abspath(model_path)
        with open(os.path.join(model_path, 'model_config.json'), 'w') as f:
            info_dict = self.to_dict()
            f.write(json.dumps(info_dict, indent=2, default=str, ensure_ascii=False))
            f.close()

        self.nn_model.save_weights(os.path.join(model_path, 'model_weights.h5'))  # type: ignore
        logger.info('model saved to {}'.format(os.path.abspath(model_path)))
        self.embedding.embed_model.save_weights(os.path.join(model_path, 'embed_model_weights.h5'))
        logger.info('embedding file saved to {}'.format(os.path.abspath(model_path)))
        return model_path


    @classmethod
    def load_model(cls, model_path):
        raise NotImplementedError



if __name__ == "__main__":
    pass
