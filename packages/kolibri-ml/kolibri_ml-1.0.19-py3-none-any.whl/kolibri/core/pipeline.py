import logging
import time
from collections import defaultdict
from kolibri.core import modules
from kolibri.core.component import Component
import numpy as np
from kolibri.utils import check_memory, _print_elapsed_time
from kolibri.core import clone
from kdmt.objects import module_path_from_object
LOGGER = logging.getLogger(__name__)


def validate_arguments(pipeline, context, allow_empty_pipeline=False):
    # type: (List[Component], Dict[Text, Any], bool) -> None
    """Validates a pipeline before it is run. Ensures, that all
    arguments are present to train the pipeline."""

    # Ensure the pipeline is not empty
    if not allow_empty_pipeline and len(pipeline) == 0:
        raise ValueError("Can not train an empty pipeline. "
                         "Make sure to specify a proper pipeline in "
                         "the configuration using the `pipeline` key." +
                         "The `backend` configuration key is "
                         "NOT supported anymore.")

    provided_properties = set(context.keys())

    for component in pipeline:
        for r in component.requires:
            if r not in provided_properties:
                raise Exception("Failed to validate at component "
                                "'{}'. Missing property: '{}'"
                                "".format(component.my_name, r))
        provided_properties.update(component.provides)

def _fit_transform_one(transformer,  X, y):
    """
    Fits ``transformer`` to ``X`` and ``y``. The transformed result is returned
    with the fitted transformer. If ``weight`` is not ``None``, the result will
    be multiplied by ``weight``.
    """
    if hasattr(transformer, 'fit_transform'):
        res = transformer.fit_transform(X, y)
    else:
        res = transformer.fit(X, y).transform(X)

    return res, transformer



class Pipeline(Component):
    """Pipeline Class.

    The **Pipeline** class represents a Machine Learning Pipeline, which
    is an ordered collection of Machine Learning tools or Primitives,
    represented by **Component instances**, that will be executed
    sequentially in order to produce results.

    The Pipeline has two working modes or phases: **fitting** and
    **predicting**.

    During the **fitting** phase, each Component instance, or **component** will be
    fitted and immediately after used to produce results on the same
    fitting data.
    This results will be then passed to the next componenet of the sequence
    as its fitting data, and this process will be repeated until the last
    component is fitted.

    During the **predicting** phase, each component will be used to produce results
    on the output of the previous one, until the last one has produce its
    results, which will be returned as the prediction of the pipelines.
    """

    def _get_tunable_hyperparameters(self):
        """Get the tunable hyperperparameters from all the blocks in this pipelines."""
        tunable = {}
        for step_name, step in self.steps.items():
            tunable[step_name] = step.get_tunable_hyperparameters()

        return tunable

    def _validate_components(self, steps):

#        names, estimators = zip(*steps)
        if steps[-1][1].component_type=="estimator":
            estimator=steps[-1]
            transformers = steps[:-1]
        else:
            estimator=None
            transformers = steps

        self.active = True

        for name, t in transformers:
            if t is None:
                continue
            else:
                if not (hasattr(t, "fit") or hasattr(t, "fit_transform")) or not hasattr(t, "transform"):
                    self.active = False
                    raise TypeError("All intermediate steps, including an evaluator, "
                                    "should implement fit and transform.")
        return transformers, estimator

    def __init__(self, steps=None, verbose=True):

#        super().__init__()
        self.steps={s[0]:s[1] for s in steps}

        self.memory=None
        self.transformers, self.estimator = self._validate_components(steps)


        self.verbose = verbose

    @staticmethod
    def from_configs(params):
        """Transform the passed names of the pipeline components into classes"""

        steps = []
        # Transform the passed names of the pipeline components into classes
        for component_name, param_val in params.items():
            component = modules.create_component_by_name(
                component_name, param_val)
            steps.append((component_name, component))

        return Pipeline(steps)
    @staticmethod
    def _flatten_dict(hyperparameters):
        return {
            (block, name): value
            for block, block_hyperparameters in hyperparameters.items()
            for name, value in block_hyperparameters.items()
        }

    def get_tunable_hyperparameters(self, flat=False):
        """Get the tunable hyperparamters of each block.

        Args:
            flat (bool): If True, return a flattened dictionary where each key
                is a two elements tuple containing the name of the block as the first
                element and the name of the hyperparameter as the second one.
                If False (default), return a dictionary where each key is the name of
                a block and each value is a dictionary containing the complete
                hyperparameter specification of that block.

        Returns:
            dict:
                A dictionary containing the block names as keys and
                the block tunable hyperparameters dictionary as values.
        """
        tunables = self._tunable_hyperparameters.copy()
        if flat:
            tunables = self._flatten_dict(tunables)

        return tunables

    @classmethod
    def _sanitize_value(cls, value):
        """Convert numpy values to their python primitive type equivalent.

        If a value is a dict, recursively sanitize its values.

        Args:
            value:
                value to sanitize.

        Returns:
            sanitized value.
        """
        if isinstance(value, dict):
            return {
                key: cls._sanitize_value(value)
                for key, value in value.items()
            }
        if isinstance(value, np.integer):
            return int(value)
        elif isinstance(value, np.floating):
            return float(value)
        elif isinstance(value, np.ndarray):
            return value.tolist()
        elif isinstance(value, np.bool_):
            return bool(value)
        elif value == 'None':
            return None

        return value

    @classmethod
    def _sanitize(cls, hyperparameters):
        """Convert tuple hyperparameter keys to nested dicts.

        Also convert numpy types to primary python types.

        The input hyperparameters dict can specify them in two formats:

        One is the native MLBlocks format, where each key is the name of a block and each value
        is a dict containing a complete hyperparameter specification for that block::

            {
                'block_name': {
                    'hyperparameter_name': 'hyperparameter_value',
                    ...
                },
                ...
            }

        The other one is an alternative format where each key is a two element tuple containing
        the name of the block as the first element and the name of the hyperparameter as the
        second one::

            {
                ('block_name', 'hyperparameter_name'): 'hyperparameter_value',
                ...
            }


        Args:
            hyperparaeters (dict):
                hyperparameters dict to sanitize.

        Returns:
            dict:
                Sanitized dict.
        """
        params_tree = defaultdict(dict)
        for key, value in hyperparameters.items():
            value = cls._sanitize_value(value)
            if isinstance(key, tuple):
                block, hyperparameter = key
                params_tree[block][hyperparameter] = value
            else:
                params_tree[key] = value

        return params_tree
    @property
    def hyperparameters(self):
        """Get the current hyperparamters of each block.

        Args:
            flat (bool): If True, return a flattened dictionary where each key
                is a two elements tuple containing the name of the block as the first
                element and the name of the hyperparameter as the second one.
                If False (default), return a dictionary where each key is the name of
                a block and each value is a dictionary containing the complete
                hyperparameter specification of that block.

        Returns:
            dict:
                A dictionary containing the block names as keys and
                the current block hyperparameters dictionary as values.
        """
        hyperparameters = dict()
        for block_name, block in self.steps.items():
            hyperparameters[block_name] = block.get_hyperparameters()

        return hyperparameters

    def set_hyperparameters(self, hyperparameters):
        """Set new hyperparameter values for some blocks.

        Args:
            hyperparameters (dict):
                A dictionary containing the block names as keys and the new hyperparameters
                dictionary as values.
        """
        hyperparameters = self._sanitize(hyperparameters)
        for block_name, block_hyperparams in hyperparameters.items():
            self.steps[block_name].set_hyperparameters(block_hyperparams)

    def fit2(self, X, y, X_val=None, y_val=None):

        """ fit
        Sequentially fit and transformer texts in all but last step, then fit
        the model in last step.
        Parameters
        ----------
        X: numpy.ndarray of shape (n_samples, n_features)
            The texts upon which the transforms/estimator will create their
            model.
        y: An array_like object of length_train n_samples
            Contains the true class y_values for all the samples in X.
        Returns
        -------
        Pipeline
            self
        """
        Xt = X
        Xt_val = X_val
        for transformer in self.transformers:
            start=time.time()
            if transformer is None:
                pass
            if hasattr(transformer, "fit_transform"):
                Xt = transformer.fit_transform(Xt, y)
                if Xt_val is not None:
                    Xt_val = transformer.fit_transform(Xt_val, y_val)
            else:
                Xt = transformer.fit(Xt, y).transform(Xt)
                if Xt_val is not None:
                    Xt_val = transformer.transform(Xt_val)
            print('fitted component ' + transformer.name + '. Elapsed time ' + str(time.time() - start))

        if self.estimator is not None:
            print('fitting estimator '+self.estimator.name)
            self.estimator.fit(Xt, y, Xt_val, y_val)

            return self
        else:
            return Xt

    def _fit(self, X, y=None, X_val=None, y_val=None):

        # Setup the memory
        memory = check_memory(self.memory)

        fit_transform_one_cached = memory.cache(_fit_transform_one)

        for step_idx, (name, transformer) in enumerate(self.transformers):
            if transformer is None :
                with _print_elapsed_time('Pipeline',
                                         self._log_message(step_idx)):
                    continue

            if memory.location is None:
                    # we do not clone when caching is disabled to
                    # preserve backward compatibility
                    cloned_transformer = transformer
            else:
                cloned_transformer = clone(transformer)

            # Fit or load from cache the current transformer
            X, fitted_transformer = fit_transform_one_cached(
                cloned_transformer, X, y)
            # Replace the transformer of the step with the fitted
            # transformer. This is necessary when loading the transformer
            # from the cache.
            self.steps[name] = fitted_transformer
        return X

    def fit_transform(self, X, y=None):
        """Fit the model and transform with the final estimator
        Fits all the transforms one after the other and transforms the
        data, then uses fit_transform on transformed data with the final
        estimator.
        Parameters
        ----------
        X : iterable
            Training data. Must fulfill input requirements of first step of the
            pipeline.
        y : iterable, default=None
            Training targets. Must fulfill label requirements for all steps of
            the pipeline.
        **fit_params : dict of string -> object
            Parameters passed to the ``fit`` method of each step, where
            each parameter name is prefixed such that parameter ``p`` for step
            ``s`` has key ``s__p``.
        Returns
        -------
        Xt : array-like of shape  (n_samples, n_transformed_features)
            Transformed samples
        """
        Xt = self._fit(X, y)

        last_step = self.estimator
        with _print_elapsed_time('Pipeline',
                                 self._log_message(len(self.steps) - 1)):
            if last_step is None:
                return Xt
            if hasattr(last_step, 'fit_transform'):
                return last_step.fit_transform(Xt, y)
            else:
                return last_step.fit(Xt, y).transform(Xt)

    @property
    def transform(self):
        """Apply transforms, and transform with the final estimator
        This also works where final estimator is ``None``: all prior
        transformations are applied.
        Parameters
        ----------
        X : iterable
            Data to transform. Must fulfill input requirements of first step
            of the pipeline.
        Returns
        -------
        Xt : array-like of shape  (n_samples, n_transformed_features)
        """
        # _final_estimator is None or has transform, otherwise attribute error
        # XXX: Handling the None case means we can't use if_delegate_has_method
        if self.estimator is not None:
            self.estimator.transform
        return self._transform

    def _transform(self, X):
        Xt = X
        for _, transform in self.transformers:
            Xt = transform.transform(Xt)
        return Xt

    def fit(self, X, y=None, X_val=None, y_val=None):
        """Fit the model
        Fit all the transforms one after the other and transform the
        data, then fit the transformed data using the final estimator.
        Parameters
        ----------
        X : iterable
            Training data. Must fulfill input requirements of first step of the
            pipeline.
        y : iterable, default=None
            Training targets. Must fulfill label requirements for all steps of
            the pipeline.
      Returns
        -------
        self : Pipeline
            This estimator
        """

        Xt = self._fit(X, y)
        with _print_elapsed_time('Pipeline',
                                 self._log_message(len(self.steps) - 1)):
            if self.estimator is not None:
                self.estimator[1].fit(Xt, y)

        return self

    def _log_message(self, step_idx):
        if not self.verbose:
            return None
        name, step = list(self.steps.items())[step_idx]

        return '(step %d of %d) Processing %s' % (step_idx + 1,
                                                  len(self.steps),
                                                  name)

    def predict(self, X):
        """ predict
        Sequentially applies all transforms and then predict with last step.
        Parameters
        ----------
        X: numpy.ndarray of shape (n_samples, n_features)
            All the samples we want to predict the label for.
        Returns
        -------
        list
            The predicted class label for all the samples in X.
        """
        if isinstance(X, dict):
            for k, val in X.items():
                if not isinstance(X[k], list):
                    X[k]=[val]
            Xt=X
        elif isinstance(X, list):
            Xt = X
        else:
            Xt=[X]

        for transform in self.transformers:
            if transform is not None:
                Xt = transform[1].transform(Xt)
        return self.estimator[1].predict(Xt)

    def get_info(self):
        info = "Pipeline:\n["
        names, estimators = zip(*self.steps)
        learner = estimators[-1]
        transforms = estimators[:-1]
        i = 0
        for t in transforms:
            try:
                if t.get_info() is not None:
                    info += t.get_info()
                    info += "\n"
                else:
                    info += 'Transform: no info available'
            except NotImplementedError:
                info += 'Transform: no info available'
            i += 1

        if learner is not None:
            try:
                if hasattr(learner, 'get_info'):
                    info += learner.get_info()
                else:
                    info += 'Learner: no info available'
            except NotImplementedError:
                info += 'Learner: no info available'
        info += "]"
        return info

    def persist(self, dir_name):
        """Persist all components of the pipeline to the passed path.

        Returns the directory of the persisted model."""

        metadata = {
            "pipeline": [],
        }


        for component in self.steps.values():
            update = component.persist(dir_name)
            component_meta = component.hyperparameters
            if update:
                component_meta.update(update)
            component_meta["label"] = module_path_from_object(component)
            component_meta["name"] = component.name

            metadata["pipeline"].append(component_meta)

        return metadata
