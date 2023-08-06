from typing import List, Dict, Any

import numpy as np
from sklearn import metrics as sklearn_metrics

import kolibri
from kolibri.backend.tensorflow.layers import L
from kolibri.backend.tensorflow.models.base_model import TFBaseModel
from kolibri.logger import get_logger

logger = get_logger(__name__)

from kdmt.ml.metrics.multi_label_classification import multi_label_classification_report


class TFBaseTextClassificationModel(TFBaseModel):
    """
    Abstract Classification Model
    """

    __task__ = 'classification'

    def to_dict(self) -> Dict:
        info = super(TFBaseTextClassificationModel, self).to_dict()
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

    def _activation_layer(self):
        if self.multi_label:
            return L.Activation('sigmoid')
        else:
            return L.Activation('softmax')

    # def build_model(self,
    #                 x_train,
    #                 y_train):
    #     """
    #     Build Model with x_data and y_data
    #
    #     This function will setup a :class:`CorpusGenerator`,
    #      then call py:meth:`BaseTextClassificationModel.build_model_gen` for preparing processor and model
    #
    #     Args:
    #         x_train:
    #         y_train:
    #
    #     Returns:
    #
    #     """
    #
    #     train_gen = DataGenerator(x_train, y_train)
    #     self.build_model_generator([train_gen])
    #
    def build_model_generator(self, generators):
        if not self.content_indexer.vocab2idx:
            self.content_indexer.build_vocab_generator(generators)

        self.label_indexer.build_vocab_generator(generators)
        self.embedding.setup_text_processor(self.content_indexer)

        if self.sequence_length is None:
            self.sequence_length = self.embedding.get_seq_length_from_corpus(generators)

        if self.nn_model is None:
            self.build_model_arc()
            self.compile_model()

    @classmethod
    def get_default_hyper_parameters(cls) -> Dict[str, Dict[str, Any]]:
        raise {}

    def build_model_arc(self):
        raise NotImplementedError

    def compile_model(self,
                      loss: Any = None,
                      optimizer: Any = None,
                      metrics: Any = None,
                      **kwargs: Any) -> None:
        """
        Configures the model for training.
        """
        if loss is None:
            if self.multi_label:
                loss = 'binary_crossentropy'
            else:
                loss = self.hyper_parameters['loss']
        if optimizer is None:
            optimizer = self.hyper_parameters['optimizer']
        if metrics is None:
            metrics = [self.hyper_parameters['metrics']]

        self.nn_model.compile(loss=loss,
                              optimizer=optimizer,
                              metrics=metrics,
                              **kwargs)

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
        with kolibri.backend.tensorflow.custom_object_scope():
            tensor = self.content_indexer.transform(x_data, )
            logger.debug(f'predict input shape {np.array(tensor).shape}')
            pred = self.nn_model.predict(tensor, batch_size=batch_size, **predict_kwargs)
            logger.debug(f'predict output shape {pred.shape}')
            sorted_indices = np.fliplr(np.argsort(pred, axis=1))
            if self.multi_label:
                multi_label_binarizer = self.label_indexer.multi_label_binarizer  # type: ignore
                labels = multi_label_binarizer.inverse_transform(pred,
                                                                 threshold=multi_label_threshold)
            else:
                labels = np.array([self.label_indexer.inverse_transform(p) for p in sorted_indices])

        return pred, labels, pred[np.arange(pred.shape[0])[:, None], sorted_indices]


    def evaluate(self, x_data, y_data, *,
                 batch_size: int = 32,
                 digits: int = 4,
                 multi_label_threshold: float = 0.5,
                 truncating: bool = False, ):
        y_pred = self.predict(x_data,
                              batch_size=batch_size,
                              truncating=truncating,
                              multi_label_threshold=multi_label_threshold)


        if self.multi_label:
            report = multi_label_classification_report(y_data,  # type: ignore
                                                       y_pred,  # type: ignore
                                                       binarizer=self.label_indexer.multi_label_binarizer)  # type: ignore

        else:
            original_report = sklearn_metrics.classification_report(y_data,
                                                                    y_pred[0][:,0],
                                                                    output_dict=True,
                                                                    digits=digits)
            print(sklearn_metrics.classification_report(y_data,
                                                        y_pred[0][:,0],
                                                        output_dict=False,
                                                        digits=digits))
            report = {
                'detail': original_report,
                **original_report['weighted avg']
            }
        return report


if __name__ == "__main__":
    pass
