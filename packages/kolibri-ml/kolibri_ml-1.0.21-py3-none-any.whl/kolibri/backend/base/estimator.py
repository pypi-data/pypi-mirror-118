import uuid, os
import numpy as np
from kolibri.core.component import Component
from kolibri.indexers.label_indexer import LabelIndexer
from kdmt.ml.common import sklearn_numpy_warning_fix
from kolibri.evaluators.evaluator import ClassifierEvaluator
from kolibri.explainers.shap_explainer import PlotSHAP
from kolibri.optimizers.optuna.objective import EstimatorObjective
from kolibri.samplers import get_sampler
from kolibri.config import TaskType
from kolibri import settings
from kolibri.config import ParamType
from kdmt.dict import update
from copy import deepcopy
from kdmt.objects import class_from_module_path
import joblib
from kolibri.version import __version__

KOLIBRI_MODEL_FILE_NAME = "classifier_kolibri.pkl"


class BaseEstimator(Component):
    """
    This is an abstract class.
    All estimators inherit from BaseEstimator.
    The notion of Estimator represents any mathematical model that estimate a response function. In machine learning it can represent either
    a supervised or unsupervised classification algorithm.

    Estimators have the following paramters that can be modified using the configuration object.

    Fixed Hyperparameters
    ---------------------
    base-estimator: a defined kolibri or sklearn.BaseEstimator (default=LogisticRegression)
        This is used by kolibri.bakend.meta estimators as a base estimator for each member of the ensemble is an instance of the base estimator

    explain : boolean (default=False)
        used to output an explanation file in the output folder.

    sampler: str (default=None), A sampler such as SMOTE can be used to balance the data in case the dataset is heavily unbalanced.
    see kolibri.samplers for various options that can be used.

    "priors-thresolding":boolean (default=False), a strategy to handle unbalanced dataset, by class prior probability.

    evaluate-performance: boolean (default=False), use this config to generate performance data before training the model.

    optimize-estimator: boolean (default=False), use this config to optimise the parameters of the estimtors. the optimisation stategy optimised the tunable parameters.

    Tunable Hyperparameters
    ---------------------

    These hyper parameters are used in optimization strategies to optimize the performances.
    one obvious parameter to optimise is the base model used to train the data.

    """

    name = "Unknown"

    short_name = "Unknown"

    component_type="estimator"

    provides = ["classification", "target_ranking"]

    requires = ["features", "text_features"]


    def __init__(self, params, classifier=None, indexer=None):


        super().__init__(parameters=params)
        self.hyperparameters=update(self.hyperparameters, BaseEstimator.get_default_hyper_parameters())

        if params is not None:
            self.override_default_parameters(params)

        self.stop_training = False
        self.library_version = __version__
        self.model = classifier
        self.uid = self.hyperparameters.get("uid", str(uuid.uuid4()))
        self.ml_task = None
        self.model_file_path = None
        self.multi_label=self.get_parameter("multi-label")
        self.multi_label_threshold=self.get_parameter("multi-label-threshold")

        if indexer is not None:
            self.indexer = indexer
        else:
            self.indexer = LabelIndexer(multi_label=self.get_parameter("multi-label"))

        self.validatation_data=None

        sklearn_numpy_warning_fix()
        self.sampler=None
        if self.get_parameter('sampler'):
            self.sampler = get_sampler(self.get_parameter('sampler'))

        self.class_priors = None
        self.performace_scores = "Not computed"




    @classmethod
    def get_default_hyper_parameters(cls):

        return {
            "fixed": {
                "base-estimator": None,
                "explain": False,
                "sampler": None,
                "priors-thresolding": False,
                'evaluate-performance': False,
                'task-type': TaskType.CLASSIFICATION,
                "multi-label": False,
                'optimize-estimator': False,
                "class-weight": False,
            },

            "tunable": {
                "model": {
                    "description": "This is just an example of a tuneable variable",
                    "value": "logreg",
                    "type": ParamType.CATEGORICAL,
                },
                "multi-label-threshold": {
                    "description": "Threshold probability value that affect the number of predicted labels per prediction",
                    "value": 0.5,
                    "type": "float",
                    "range": [0.3, 0.7]
                }
            }
        }

    def is_fitted(self):
        # base class method
        return False

    def reload(self):
        if not self.is_fitted() and self.model_file_path is not None:
            self.load_model(self.model_file_path)

    def fit( self,  X, y, X_validation=None, y_validation=None, **kwargs ):

        if self.get_parameter('optimize-estimator'):
            self.optimize(X, y)

        elif self.get_parameter('evaluate-performance'):
            evaluator = ClassifierEvaluator(estimator=self.model)
            if X_validation is None or y_validation is None:
                self.performace_scores = evaluator.cv_compute_performance_report(X=X, y=y, labels=list(
                    self.indexer.vocab2idx.keys()))
            else:
                self.performace_scores=evaluator.compute_performance_report(X=X, y=y, X_val=X_validation, y_val=y_validation)
            self.validatation_data=np.column_stack((self.indexer.inverse_transform(evaluator.predictions[:,0]), evaluator.predictions[:,1]))

    def copy(self):
        pass

    def save(self, model_file_path):
        pass

    def load_model(self, model_file_path):
        pass


    def explain(
        self,
        X_train,
        y_train,
        X_validation,
        y_validation,
        model_file_path,
        learner_name,
        target_name=None,
        class_names=None,
        ml_task=None,
    ):
        # do not produce feature importance for Baseline
        if self.algorithm_short_name == "Baseline":
            return
        PlotSHAP.compute(
                self,
                X_train,
                y_train,
                X_validation,
                y_validation,
                model_file_path,
                learner_name,
                class_names,
                ml_task,
            )

    def get_metric_name(self):
        return None

    def get_params(self):
        params = {
            "library_version": self.library_version,
            "algorithm_name": self.algorithm_name,
            "algorithm_short_name": self.algorithm_short_name,
            "uid": self.uid,
            "params": self.params,
            "name": self.name,
        }
        if hasattr(self, "best_ntree_limit") and self.best_ntree_limit is not None:
            params["best_ntree_limit"] = self.best_ntree_limit
        return params

    def set_params(self, json_desc, learner_path):
        self.library_version = json_desc.get("library_version", self.library_version)
        self.algorithm_name = json_desc.get("algorithm_name", self.algorithm_name)
        self.algorithm_short_name = json_desc.get(
            "algorithm_short_name", self.algorithm_short_name
        )
        self.uid = json_desc.get("uid", self.uid)
        self.params = json_desc.get("params", self.params)
        self.name = json_desc.get("name", self.name)
        self.model_file_path = learner_path

        if hasattr(self, "best_ntree_limit"):
            self.best_ntree_limit = json_desc.get(
                "best_ntree_limit", self.best_ntree_limit
            )


    @classmethod
    def required_packages(cls):
        return ["sklearn"]

    def evaluate(self, X_val=None, y_val=None):

        if X_val is not None and y_val is not None:
            pred = self.predict(X_val)

            self.performace_scores = ClassifierEvaluator().get_performance_report(y_true=y_val, y_pred=pred)

    def compute_priors(self, y):
        unique, counts = np.unique(y, return_counts=True)
        self.class_priors = dict(zip(unique, counts))

        total = sum(self.class_priors.values(), 0.0)
        self.class_priors = {k: v / total for k, v in self.class_priors.items()}

    def predict_proba(self, X):
        """Given a bow vector of an input text, predict the class label.

        Return probabilities for all y_values.

        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""
        raw_predictions=None
        try:
            if self.get_parameter('task-type') == TaskType.BINARY_CLASSIFICATION:
                raw_predictions=self.model.predict_proba(X)[:, 1]
            elif self.get_parameter('task-type') == TaskType.CLASSIFICATION:
                raw_predictions=self.model.predict_proba(X)
        except:
            raise Exception('Predict_proba raised an error in Estimator')


        if self.get_parameter("priors-thresolding"):
            if not raw_predictions is None:
                try:
                    priors = np.array([v for v in self.class_priors.values()])
                    raw_predictions = (raw_predictions.T - priors[:, None]) / priors[:, None]
                    raw_predictions = np.argmax(raw_predictions.T, axis=1)
                except Exception as e:
                    print(e)

        # sort the probabilities retrieving the indices of
        # the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(raw_predictions, axis=1))

        return raw_predictions, sorted_indices, [p[sorted_indices[i]] for i, p in enumerate(raw_predictions)]

    def predict(self, X):
        """Given a bow vector of an input text, predict most probable label.

        Return only the most likely label.

        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""
        probabilities=[]
        try:
            raw_predictions, class_ids, probabilities=self.predict_proba(X)
        except:
            class_ids=self.model.predict(X)


        if self.multi_label:
            multi_label_binarizer = self.label_indexer.multi_label_binarizer  # type: ignore
            classes = multi_label_binarizer.inverse_transform(class_ids,
                                                              threshold=self.multi_label_threshold)

        else:
            classes=np.array([self.indexer.inverse_transform(np.ravel(p)) for p in class_ids])

        return self.process([list(zip(classe, probability)) for classe, probability in zip(classes, probabilities)])

    def objective(self, X, y):
        objective=EstimatorObjective(X, y, self, None, eval_metric=self.get_parameter('opt-metric-name'), n_jobs=-1, random_state=42)
        return objective


    def process(self, results):

        if results is not None:
            ranking= [result[:settings.TARGET_RANKING_LENGTH] for result in results]

            target = [{"name": result[0][0], "confidence": result[0][1]} for result in results]

            target_ranking = [[{"name":r[0], "confidence":r[1]} for r in rank] for rank in ranking]
        else:
            target = {"name": None, "confidence": 0.0}
            target_ranking = []


        response={
            "label": target,
            "ranking": target_ranking
        }
        return response

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):

 #       meta = model_metadata.for_component(cls.name)
        file_name = model_metadata.get("classifier_file", KOLIBRI_MODEL_FILE_NAME)
        classifier_file = os.path.join(model_dir, file_name)

        if os.path.exists(classifier_file):
            model = joblib.load(classifier_file)
            return model
        else:
            return cls(model_metadata)

    def persist(self, model_dir):
        """Persist this model into the passed directory."""

        classifier_file = os.path.join(model_dir, KOLIBRI_MODEL_FILE_NAME)
        joblib.dump(self, classifier_file)

        return {
            "classifier_file": KOLIBRI_MODEL_FILE_NAME,
            "performace_scores": self.performace_scores,
        }

