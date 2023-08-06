import json
import os
import pathlib
import tempfile
import time
from abc import abstractmethod
from typing import Any

import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, LambdaCallback

from kolibri.backend.base.base_model import BaseModel
from kolibri.backend.tensorflow.embeddings import DefaultEmbedding
from kolibri.utils.common import load_data_object
from kolibri.logger import get_logger
from kolibri.backend.tensorflow.data.generators import TFDataset
logger = get_logger(__name__)


class TFBaseModel(BaseModel):

    def __init__(self, hyper_parameters={}, embedding=None, sequence_length=None, multi_label=False,
                 content_indexer=None, label_indexer=None):
        if embedding is None:
            embedding = DefaultEmbedding()  # type: ignore
        super().__init__(hyper_parameters, embedding, sequence_length, multi_label, content_indexer, label_indexer)


    def fit(self, x_train, y_train, x_validate=None, y_validate=None, callbacks=None, fit_kwargs={}):

        train_gen = TFDataset(x_train, y_train)
        if x_validate is not None:
            valid_gen = TFDataset(x_validate, y_validate)
        else:
            valid_gen = None
        return self.fit_generator(train_sample_gen=train_gen,
                                  valid_sample_gen=valid_gen,
                                  callbacks=callbacks,
                                  fit_kwargs=fit_kwargs)
    def fit_generator(self, train_sample_gen, valid_sample_gen=None, callbacks=None, fit_kwargs={}):

        self.build_model_generator([g for g in [train_sample_gen, valid_sample_gen] if g])

        model_summary = []
        self.nn_model.summary(print_fn=lambda x: model_summary.append(x))
        logger.debug('\n'.join(model_summary))

        train_set = train_sample_gen
        train_set.set_batch_size(fit_kwargs['batch_size'])
        train_set.label_indexer = self.label_indexer
        train_set.content_indexer = self.content_indexer

        if fit_kwargs is None:
            fit_kwargs = {}

        if valid_sample_gen:
            valid_gen = valid_sample_gen
            valid_gen.set_batch_size(fit_kwargs['batch_size'])
            valid_gen.label_indexer = self.label_indexer
            valid_gen.content_indexer = self.content_indexer

            fit_kwargs['validation_data'] = valid_gen
            fit_kwargs['validation_steps'] = len(valid_gen)

        def on_epoch_end(_a, _b):
            self.epoch += 1

        if valid_sample_gen is not None:
            if callbacks is None:
                callbacks = []
            if LambdaCallback(on_epoch_end=on_epoch_end) not in callbacks:
                callbacks.append(LambdaCallback(on_epoch_end=on_epoch_end))

            if self.hyper_parameters['save-best']:
                self.checkpoint_model_path = os.path.join(tempfile.gettempdir(), str(time.time()))
                pathlib.Path(self.checkpoint_model_path).mkdir(parents=True, exist_ok=True)
                self.checkpoint_model_path = os.path.join(self.checkpoint_model_path, 'best_weights.h5')
                callbacks.append(
                    ModelCheckpoint(filepath=self.checkpoint_model_path, monitor=self.hyper_parameters['monitor'],
                                    save_best_only=True, verbose=1, mode=self.hyper_parameters['mode']))
            if self.hyper_parameters['early-stop']:
                callbacks.append(EarlyStopping(monitor=self.hyper_parameters['monitor'],
                                               patience=self.hyper_parameters['early_stopping_patience']))
        fit_kwargs['epochs']= self.epoch + self.hyper_parameters['epochs']
        history = self.nn_model.fit(train_sample_gen,
                                    steps_per_epoch=len(train_sample_gen),
                                    initial_epoch=self.epoch,
                                    callbacks=callbacks,
                                    **fit_kwargs)
        if os.path.exists(self.checkpoint_model_path):
            self.nn_model.load_weights(self.checkpoint_model_path)

        return self.nn_model

    def to_dict(self):
        model_json_str = self.nn_model.to_json()
        dict_values=super().to_dict()
        dict_values['tf_version']=tf.__version__
        dict_values['nn_model']= json.loads(model_json_str)
        return dict_values

    @classmethod
    def load_model(cls, model_path):
        from kolibri.backend.tensorflow.layers.crf import ConditionalRandomField
        model_config_path = os.path.join(model_path, 'model_config.json')
        with open(model_config_path, 'r') as f:
            model_config = json.loads(f.read())
        model = load_data_object(model_config)

        model.embedding = load_data_object(model_config['embedding'])
        model.content_indexer = load_data_object(model_config['content_indexer'])
        model.label_indexer = load_data_object(model_config['label_indexer'])
        model.epoch = model_config['epoch']
        tf_model_str = json.dumps(model_config['nn_model'])
        model.nn_model = tf.keras.models.model_from_json(tf_model_str,
                                                         {'ConditionalRandomField': ConditionalRandomField})

        if isinstance(model.nn_model.layers[-1], ConditionalRandomField):
            model.layer_crf = model.nn_model.layers[-1]

        model.nn_model.load_weights(os.path.join(model_path, 'model_weights.h5'))
        model.embedding.embed_model.load_weights(os.path.join(model_path, 'embed_model_weights.h5'))
        return model
    @abstractmethod
    def build_model(self,
                    x_data: Any,
                    y_data: Any) -> None:
        raise NotImplementedError


if __name__ == "__main__":
    path = ''
    m = TFBaseModel.load_model(path)
    m.nn_model.summary()
