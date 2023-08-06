import os

import torch
import torch.nn.functional as F
from torch.optim import SGD
from torch.utils.data import DataLoader

from ignite.contrib.handlers import ProgressBar
from ignite.engine import Events, create_supervised_evaluator, create_supervised_trainer
from ignite.metrics import Accuracy, Loss, RunningAverage
from kolibri.utils.common import load_data_object
from kolibri.backend.base.base_model import BaseModel
from kolibri.backend.torch.embeddings.default_embedding import DefaultEmbedding
from pathlib import Path
from kolibri.backend.torch.callbacks.base import *
from kolibri.logger import get_logger
from kolibri.backend.torch.data.generator import TorchDataset
logger = get_logger(__name__)


class TorchBaseModel(BaseModel):

    def __init__(self, hyper_parameters={}, embedding=None, sequence_length=None, multi_label=False,
                 content_indexer=None, label_indexer=None):
        if embedding is None:
            embedding = DefaultEmbedding()  # type: ignore
        super().__init__(hyper_parameters, embedding, sequence_length, multi_label, content_indexer, label_indexer)


    def fit(self, x_train, y_train, x_validate=None, y_validate=None, callbacks=None, fit_kwargs={}):

        train_gen = TorchDataset(x_train, y_train)
        if x_validate is not None:
            valid_gen = TorchDataset(x_validate, y_validate)
        else:
            valid_gen = None
        return self.fit_generator(train_sample_gen=train_gen,
                                  valid_sample_gen=valid_gen,
                                  callbacks=callbacks,
                                  fit_kwargs=fit_kwargs)


    def fit_generator(self, train_sample_gen, valid_sample_gen=None, callbacks=None, fit_kwargs={}):

        train_sample_gen.reset()
        valid_sample_gen.reset()
        self.build_model_generator([g for g in [train_sample_gen, valid_sample_gen] if g])
        train_sample_gen.reset()
        train_set = train_sample_gen
#        train_set.set_batch_size(fit_kwargs['batch_size'])
        train_set.label_indexer = self.label_indexer
        train_set.content_indexer = self.content_indexer

        if fit_kwargs is None:
            fit_kwargs = {}

        if valid_sample_gen:
            valid_gen = valid_sample_gen
#            valid_gen.set_batch_size(fit_kwargs['batch_size'])
            valid_gen.label_indexer = self.label_indexer
            valid_gen.content_indexer = self.content_indexer

        device = "cpu"

        if torch.cuda.is_available():
            device = "cuda"

        self.nn_model.to(device)  # Move model before creating optimizer
        self.optimizer = SGD(self.nn_model.parameters(), lr=self.hyper_parameters['learning-rate'], momentum=self.hyper_parameters['momentum'])
        trainer = create_supervised_trainer(self.nn_model, self.optimizer, F.nll_loss, device=device)
        evaluator = create_supervised_evaluator(
            self.nn_model, metrics={"accuracy": Accuracy(), "nll": Loss(F.nll_loss)}, device=device
        )

        RunningAverage(output_transform=lambda x: x).attach(trainer, "loss")

        if self.hyper_parameters['display_gpu_info']:
            from ignite.contrib.metrics import GpuInfo

            GpuInfo().attach(trainer, name="gpu")

        pbar = ProgressBar(persist=True)
        pbar.attach(trainer, metric_names="all")

        @trainer.on(Events.EPOCH_COMPLETED)
        def log_training_results(engine):
            evaluator.run(DataLoader(train_set))
            metrics = evaluator.state.metrics
            avg_accuracy = metrics["accuracy"]
            avg_nll = metrics["nll"]
            pbar.log_message(
                f"Training Results - Epoch: {engine.state.epoch} Avg accuracy: {avg_accuracy:.2f} Avg loss: {avg_nll:.2f}"
            )

        @trainer.on(Events.EPOCH_COMPLETED)
        def log_validation_results(engine):
            evaluator.run(DataLoader(valid_gen))
            metrics = evaluator.state.metrics
            avg_accuracy = metrics["accuracy"]
            avg_nll = metrics["nll"]
            pbar.log_message(
                f"Validation Results - Epoch: {engine.state.epoch} Avg accuracy: {avg_accuracy:.2f} Avg loss: {avg_nll:.2f}"
            )

            pbar.n = pbar.last_print_n = 0

        trainer.run(DataLoader(train_set), max_epochs=fit_kwargs['epochs'])



    def to_dict(self):
        dict_values = super().to_dict()
        dict_values['torch_version'] = torch.__version__
        for param_tensor in self.nn_model.state_dict():
            dict_values[param_tensor]=self.nn_model.state_dict()[param_tensor].size()
        return dict_values

    @classmethod
    def load_model(cls, model_path):


        model_config_path = os.path.join(model_path, 'model_config.json')
        with open(model_config_path, 'r') as f:
            model_config = json.loads(f.read())

        model=cls(model_config['config']['hyper_parameters'])


        model.content_indexer = load_data_object(model_config['content_indexer'])
        model.label_indexer = load_data_object(model_config['label_indexer'])
        model.epoch = model_config['epoch']

        model.nn_model= torch.load(os.path.join(model_path, 'torch_nn.o'))
        embedding=DefaultEmbedding()
        embedding.embed_model=torch.load(os.path.join(model_path, 'embeddings.o'))

        model.embedding=embedding
        model.nn_model.eval()

        return model

    def save(self, model_path: str) -> str:
        """
        Save model
        Args:
            model_path:
        """
        Path(model_path).mkdir(exist_ok=True, parents=True)
        model_path = os.path.abspath(model_path)
        with open(os.path.join(model_path, 'model_config.json'), 'w') as f:
            info_dict = self.to_dict()
            f.write(json.dumps(info_dict, indent=2, default=str, ensure_ascii=False))
            f.close()

        torch.save(self.nn_model, os.path.join(model_path, 'torch_nn.o'))
        torch.save(self.embedding.embed_model,os.path.join(model_path, 'embeddings.o'))
        return os.path.join(model_path, 'torch_nn.o')

if __name__ == "__main__":
    path = ''
    m = TFBaseModel.load_model(path)
    m.nn_model.summary()
