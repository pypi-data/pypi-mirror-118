import json
import os
import pathlib
import tempfile
import time
from abc import abstractmethod
from typing import Any

import tensorflow as tf
from kolibri.backend.torch.callbacks.base import *

from kolibri.backend.base.base_model import BaseModel
from kolibri.backend.tensorflow.embeddings import DefaultEmbedding
from kolibri.backend.tensorflow.utils import load_data_object
from kolibri.logger import get_logger
import torch
from torch.nn import Module
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader

from kolibri.backend.torch.thtrainer import metrics as trainer_metrics
from kolibri.backend.torch.thtrainer.callbacks import ProgbarLogger, CallbackList, History
from kolibri.backend.torch.thtrainer.metrics import MetricList

logger = get_logger(__name__)

metric_dict = {
    'acc': trainer_metrics.Accuracy,
    'accuracy': trainer_metrics.Accuracy,
    'loss': trainer_metrics.Loss,
    'top-k': trainer_metrics.TopKCategoricalAccuracy,
    'mae': trainer_metrics.MeanAbsoluteError,
    'mse': trainer_metrics.MeanSquaredError
}


def make_callbacks(optim=None, model_path=None,
                   scheduler=None, monitor=None, patience=1,
                   tensorboard_logdir=None):
    used_callbacks = []

    # If you use the learning rate scheduler,
    # you will need to add LRSchedulerCallback
    if scheduler is not None:
        scheduler = LRSchedulerCallback(scheduler(optim))
        used_callbacks.append(scheduler)

    # Use checkpoint
    if model_path is not None:
        checkpoint = ModelCheckpoint(
            model_path, 'train:loss',
            save_best_only=True,
            period=10, verbose=1,
            mode='min',
            save_weights_only=True
        )
        used_callbacks.append(checkpoint)

    # Use early stopping
    if monitor is not None:
        early_stop = EarlyStopping(monitor=monitor,
                                             patience=patience,
                                             mode='min',
                                             restore_best_weights=False)
        used_callbacks.append(early_stop)

#    if tensorboard_logdir is not None:
#        used_callbacks.append(tensorboard.TensorBoard(tensorboard_logdir))

    return used_callbacks




def warmup_lr_scheduler(optimizer, warmup_iters, warmup_factor):
    def f(x):
        if x >= warmup_iters:
            return 1
        alpha = float(x) / warmup_iters
        return warmup_factor * (1 - alpha) + alpha

    return torch.optim.lr_scheduler.LambdaLR(optimizer, f)


def _check_data_loader(data, batch_size, shuffle):
    if not isinstance(data, DataLoader):
        data = DataLoader(data, batch_size=batch_size, shuffle=shuffle)
    return data


def _check_metrics(metrics, loss_fn):
    def get_metric_ins(m):
        new_m = []

        for i, mi in enumerate(m):
            if isinstance(mi, str):
                mi = mi.lower()
                if mi not in metric_dict:
                    raise RuntimeError('Not %s metric' % mi)
                if mi == 'loss':
                    _metric_ins = metric_dict[mi](loss_fn)
                else:
                    _metric_ins = metric_dict[mi]()
                new_m.append(_metric_ins)
            else:
                new_m.append(mi)
        return new_m

    if metrics is None:
        m = {}
        if loss_fn is not None:
            m['loss'] = metric_dict['loss'](loss_fn)
        metrics = MetricList(m)

    if isinstance(metrics, dict):
        metrics = dict(zip(metrics.keys(),
                           get_metric_ins(metrics.values())))
        metrics = MetricList(metrics)

    if isinstance(metrics, (list, tuple)):
        metrics = get_metric_ins(metrics)
        metrics = MetricList(metrics)

    if not isinstance(metrics, trainer_metrics.MetricList):
        raise RuntimeError('Metrics not support %s type' % str(type(metrics)))
    return metrics


def _check_logs_param(logs, loss_fn):
    if logs is None:
        logs = []
    if isinstance(logs, (tuple, list)):
        logs = list(logs)
    else:
        raise RuntimeError('logs param must be tuple or list, but get', logs)

    if loss_fn is not None:
        logs.append('loss')

    return logs


def _check_progbar_logger_metrics(metrics, val_metrics, logs=[]):
    keys = metrics.keys()
    keys = list(keys)
    if val_metrics is None or len(val_metrics) == 0:
        return keys + logs

    train_keys = ['train:' + k for k in keys]
    val_keys = ['val:' + k for k in list(val_metrics.keys())]
    if logs is None:
        logs=[]
    return train_keys + val_keys + logs


def _check_progbar_logger_iters(key, value):
    kvs = {}
    key_t = '%s:%s'
    if isinstance(value, dict):
        value = value.items()
    elif isinstance(value, (tuple, list)):
        value = enumerate(value)
    else:
        return {key: value}

    for i, vi in value:
        _sub_key = key_t % (key, str(i))
        if isinstance(vi, (tuple, list, dict)):
            res = _check_progbar_logger_iters(_sub_key, vi)
        else:
            res = {_sub_key: vi}
        kvs.update(res)
    return kvs


def _check_progbar_logger_value(key, value):
    kvs = {}
    if key is None or key == '':
        key_t = '%s%s'
    else:
        key_t = '%s:%s'
    if isinstance(value, dict):
        value = value.items()
    elif isinstance(value, (tuple, list)):
        value = enumerate(value)
    else:
        return {key: value}

    for i, vi in value:
        _sub_key = key_t % (key, str(i))
        if isinstance(vi, (tuple, list, dict)):
            res = _check_progbar_logger_iters(_sub_key, vi)
        else:
            res = {_sub_key: vi}
        kvs.update(res)
    return kvs


class TorchBaseModel(BaseModel):

    def __init__(self, hyper_parameters={}, embedding=None, sequence_length=None, multi_label=False,
                 content_indexer=None, label_indexer=None):
        if embedding is None:
            embedding = DefaultEmbedding()  # type: ignore
        super().__init__(hyper_parameters, embedding, sequence_length, multi_label, content_indexer, label_indexer)



        self.optimizer = self.hyper_parameters['optimizer']
        self.loss_fn = torch.nn.CrossEntropyLoss()# self.hyper_parameters['loss']

        self.metrics = _check_metrics(self.hyper_parameters['metrics'], self.loss_fn)
        m = []
        self.val_metrics = MetricList(m)

        self.device = 'cpu'
        if torch.cuda.is_available():
            self.device = 'cuda'

        self._stop_training = False
        self.validation_data = None

    def fit_generator(self, train_sample_gen, valid_sample_gen=None, callbacks=None, fit_kwargs={}):

        def make_scheduler(optim):
            return torch.optim.lr_scheduler.CosineAnnealingLR(optim, fit_kwargs['epochs'], 0)

        def make_optim(params):
            return torch.optim.Adam(params, fit_kwargs['learning-rate'], weight_decay=1e-4)

        logs=[]
        self.build_model_generator([g for g in [train_sample_gen, valid_sample_gen] if g])

        if torch.cuda.is_available():
            torch.backends.cudnn.benchmark = True
            self.nn_model = self.nn_model.cuda()

        model_params = [p for p in self.nn_model.parameters() if p.requires_grad]

        validate_steps = 1
        validate_init = 1
        verbose=1


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

        if fit_kwargs['optimizer'] is None:
            self.optimizer = torch.optim.Adam(model_params, fit_kwargs['learning-rate'], weight_decay=1e-4)
        else:
            self.optimizer = make_optim(model_params)

        scheduler = None
        if make_scheduler is None:
            scheduler = make_scheduler(self.optimizer)

        callbacks = make_callbacks(optim=self.optimizer, model_path=self.hyper_parameters['model-path'],
                                        scheduler=scheduler, monitor=self.hyper_parameters['monitor'], patience=self.hyper_parameters['early-stopping-patience'])

        n_steps = len(train_set)
        progress = ProgbarLogger(stateful_metrics=self.metrics.keys())
        progress.set_params({
            'batch_size': fit_kwargs['batch_size'],
            'epochs': 1,
            'steps': n_steps,
            'samples': n_steps,
            'verbose': verbose,
            'metrics': list(set(['eval:' + k for k in self.metrics.keys()] + ['loss'])) + logs,
        })

        if callbacks is not None:
                callbacks = list(callbacks) + [progress]
        history = History()
        callbacks.append(history)
        callbacks = CallbackList(callbacks)
        callbacks.set_model(self.nn_model)

        epochs=fit_kwargs['epochs']
        n_steps = len(train_sample_gen)
        callbacks.set_params({
            'batch_size': fit_kwargs['batch_size'],
            'epochs': epochs,
            'steps': n_steps,
            'verbose': verbose,
            'samples': n_steps,
            'metrics': _check_progbar_logger_metrics(self.metrics, self.val_metrics, logs),
        })
        if valid_sample_gen is not None:
            callbacks.set_validation_data(valid_sample_gen)

        # ref detection warmup
        warmup_scheduler = None
        if self.hyper_parameters['warmup']:
            warmup_factor = 1. / 1000
            warmup_iters = min(1000, len(train_sample_gen) - 1)
            warmup_scheduler = warmup_lr_scheduler(
                self.optimizer,
                warmup_iters,
                warmup_factor
            )

        train_logs = {}
        callbacks.on_train_begin(train_logs)
        for epoch in range(1, epochs+1):
            self.nn_model.train()
            if self._stop_training:
                callbacks.on_train_end({})
                return history

            epoch_logs = {}
            callbacks.on_epoch_begin(epoch, epoch_logs)
            self._train_data_loader(epoch, train_sample_gen, callbacks, epoch_logs, warmup_scheduler)

            # evaluate validattion_data
            eval_val_data = epoch % validate_steps == 0 and epoch >= validate_init
            if valid_sample_gen is not None and eval_val_data:
                if verbose > 0:
                    print('\nStarting evaluate model')
                eval_res = self.evaluate(
                    valid_sample_gen,
                    fit_kwargs['batch_size'],
                    shuffle=False,
                    metrics=self.val_metrics,
                    verbose=0,
                    device=self.device,
                    logs=logs
                )
                res = _check_progbar_logger_value('val', eval_res)
                epoch_logs.update(res)

            callbacks.on_epoch_end(epoch, epoch_logs)

        callbacks.on_train_end(train_logs)
        return history

    def to_dict(self):
        dict_values = super().to_dict()
        dict_values['tf_version'] = tf.__version__
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

    def _train_data_loader(self, epoch, data_loader, callbacks, epoch_logs, warmup_scheduler=None):
        self.metrics.reset()
        prefix = ''
        if self.validation_data is not None:
            prefix = 'train'

        loss_sum = 0
        batch_idx = -1
        batch_log = {}
        for batch_data in zip(data_loader):
            batch_idx += 1
            if self._stop_training:
                return batch_log

            callbacks.on_batch_begin(batch_idx, batch_log)

            loss = self.train_on_batch(*batch_data[0])

            batch_log['loss'] = loss.item()
            loss_sum += loss.item()
            callbacks.on_batch_end(batch_idx, batch_log)

            if epoch == 1 and warmup_scheduler is not None:
                warmup_scheduler.step()
        res = self.metrics.compute()
        res = _check_progbar_logger_value(prefix, res)
        epoch_logs.update(res)
        return batch_log

    def train_on_batch(self, X, y=None):
        X = X.to(self.device)
        if y is not None:
            y = y.to(self.device)

        def closure():
            self.optimizer.zero_grad()
            output = self.model(X)
            if y is None:
                pair = (output, )
            else:
                pair = (output, y)
            self.metrics.update(pair)
            loss = self.loss_fn(*pair)
            loss.backward()
            return loss
        return self.optimizer.step(closure)

    @torch.no_grad()
    def predict(self, X):
        self.model.eval()
        return self.model(X)

    def evaluate_batch(self, X, y=None, device=None):
        device = device or self.device
        X = X.to(device)
        if y is not None:
            y = y.to(device)
        output = self.model(X)
        loss = None
        if self.loss_fn is not None:
            if y is None:
                loss = self.loss_fn(output)
            else:
                loss = self.loss_fn(output, y)
        if y is None:
            if loss is None:
                return output
            else:
                return loss, output
        else:
            if loss is None:
                return (output, y)
            else:
                return loss, (output, y)

    @torch.no_grad()
    def evaluate(self,
                 data_loader, batch_size=1,
                 shuffle=False, metrics=None,
                 verbose=1, device=None,
                 logs=None):
        '''
        # Arguments
            data_loader: `DataLoader`
            batch_size: `Integer` DataLoader batch size
            shuffle: Boolean (whether to shuffle the training data
                before each epoch) or str (for 'batch').
            metrics: List of `thtrainer.metrics.Metric` instances.
                Compute metrics at the end of each batch.
            verbose: `Integer`. 0, 1, or 2. Verbosity mode.
                0 = silent, 1 = progress bar, 2 = one line per epoch.
            logs: List or tuple
                Keys added by the user in the logs of Batch or Epoch,
                if you need to be displayed in ProgressBar or TensorBoard,
                you need to make logs equal to Keys.
        '''

        data_loader = _check_data_loader(data_loader, batch_size, shuffle)
        if not isinstance(metrics, trainer_metrics.MetricList):
            metrics = _check_metrics(metrics, self.loss_fn)
        n_steps = len(data_loader)

        logs = _check_logs_param(logs, self.loss_fn)

        if verbose > 0:
            progress = ProgbarLogger(stateful_metrics=metrics.keys())
            progress.set_params({
                'batch_size': batch_size,
                'epochs': 1,
                'steps': n_steps,
                'samples': n_steps,
                'verbose': verbose,
                'metrics': list(set(['eval:' + k for k in self.metrics.keys()] + ['loss'])) + logs,
            })

        device = device or self.device
        self.model.eval()
        metrics.reset()
        epoch_logs = {}

        if verbose > 0:
            progress.on_train_begin({})
            progress.on_epoch_begin(1, epoch_logs)

        loss_sum = 0
        batch_logs = {}
        for batch, batch_data in zip(range(n_steps), data_loader):
            if verbose > 0:
                progress.on_batch_begin(batch, batch_logs)

            output = self.evaluate_batch(*batch_data, device)
            if self.loss_fn is not None:
                loss, output = output
                loss_sum += loss.item()
                batch_logs['loss'] = loss_sum / (batch + 1)
            metrics.update(output)

            if verbose > 0:
                progress.on_batch_end(batch, batch_logs)

        res = metrics.compute()

        if self.loss_fn is not None:
            _key = 'val:loss'
            loss = loss_sum / len(data_loader)
            epoch_logs[_key] = loss
            res['val:loss'] = loss

        if verbose > 0:
            res = _check_progbar_logger_value('', res)
            epoch_logs.update(res)

        if verbose > 0:
            progress.on_epoch_end(1, epoch_logs)
            progress.on_train_end(epoch_logs)

        return res

    def stop_training(self):
        self._stop_training = True

    def save_weights(self, filepath, overwrite=True):
        torch.save(self.model.state_dict(), filepath)

    def save(self, filepath, overwrite=True):
        torch.save(self.model, filepath)

    def get_weights(self):
        return self.model.state_dict()

    def set_weights(self, weights):
        self.model.load_state_dict(weights)

    @abstractmethod
    def build_model(self,
                    x_data: Any,
                    y_data: Any) -> None:
        raise NotImplementedError


if __name__ == "__main__":
    path = ''
    m = TFBaseModel.load_model(path)
    m.nn_model.summary()
