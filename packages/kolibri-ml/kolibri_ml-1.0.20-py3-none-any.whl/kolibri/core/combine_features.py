from kolibri.core.component import Component
import numpy as np
import os
from kdmt.file import create_dir
from scipy import sparse
from joblib import Parallel, delayed
from kolibri.utils import _print_elapsed_time
from kdmt.objects import module_path_from_object
def _transform_one(transformer, X, y, weight):
    res = transformer.transform(X)
    # if we have a weight for this transformer, multiply output
    if weight is None:
        return res
    return res * weight


def _fit_transform_one(transformer,
                       X,
                       y,
                       weight,
                       message_clsname='',
                       message=None,
                       **fit_params):
    """
    Fits ``transformer`` to ``X`` and ``y``. The transformed result is returned
    with the fitted transformer. If ``weight`` is not ``None``, the result will
    be multiplied by ``weight``.
    """
    with _print_elapsed_time(message_clsname, message):
        if hasattr(transformer, 'fit_transform'):
            res = transformer.fit_transform(X, y, **fit_params)
        else:
            res = transformer.fit(X, y, **fit_params).transform(X)

    if weight is None:
        return res, transformer
    return res * weight, transformer


def _fit_one(transformer,
             X,
             y,
             weight,
             message_clsname='',
             message=None,
             **fit_params):
    """
    Fits ``transformer`` to ``X`` and ``y``.
    """
    with _print_elapsed_time(message_clsname, message):
        return transformer.fit(X, y, **fit_params)

class FeatureUnion(Component):
    """Concatenates results of multiple transformer objects.
    This estimator applies a list of transformer objects in parallel to the
    input data, then concatenates the results. This is useful to combine
    several feature extraction mechanisms into a single transformer.
    Parameters of the transformers may be set using its name and the parameter
    name separated by a '__'. A transformer may be replaced entirely by
    setting the parameter with its name to another transformer,
    or removed by setting to 'drop'.
    Read more in the :ref:`User Guide <feature_union>`.
    .. versionadded:: 0.13
    Parameters
    ----------
    transformer_list : list of (string, transformer) tuples
        List of transformer objects to be applied to the data. The first
        half of each tuple is the name of the transformer. The tranformer can
        be 'drop' for it to be ignored.
        .. versionchanged:: 0.22
           Deprecated `None` as a transformer in favor of 'drop'.
    n_jobs : int, default=None
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.
        .. versionchanged:: v0.20
           `n_jobs` default changed from 1 to None
    transformer_weights : dict, default=None
        Multiplicative weights for features per transformer.
        Keys are transformer names, values the weights.
        Raises ValueError if key not present in ``transformer_list``.
    verbose : bool, default=False
        If True, the time elapsed while fitting each transformer will be
        printed as it is completed.
    See Also
    --------
    make_union : Convenience function for simplified feature union
        construction.
    Examples
    --------
    >>> from sklearn.pipeline import FeatureUnion
    >>> from sklearn.decomposition import PCA, TruncatedSVD
    >>> union = FeatureUnion([("pca", PCA(n_components=1)),
    ...                       ("svd", TruncatedSVD(n_components=2))])
    >>> X = [[0., 1., 3], [2., 2., 5]]
    >>> union.fit_transform(X)
    array([[ 1.5       ,  3.0...,  0.8...],
           [-1.5       ,  5.7..., -0.4...]])
    """
    _required_parameters = ["transformer_list"]


    def __init__(self, transformer_list=None, n_jobs=None, transformer_weights=None, verbose=False):

        super().__init__({})
        if transformer_list is not None:
            self.transformer_list = transformer_list
        else:
            self.transformer_list=self.get_parameter('transformer-list')

        self.n_jobs = n_jobs
        self.transformer_weights = transformer_weights
        self.verbose = verbose
        self._validate_transformers()


    def _validate_transformers(self):

        # validate estimators
        for n, t in self.transformer_list:
            if (not (hasattr(t, "fit") or hasattr(t, "fit_transform")) or not
                    hasattr(t, "transform")):
                raise TypeError("All estimators should implement fit and "
                                "transform. '%s' (type %s) doesn't" %
                                (t, type(t)))

    def _validate_transformer_weights(self):
        if not self.transformer_weights:
            return

        transformer_names = set(name for name, _ in self.transformer_list)
        for name in self.transformer_weights:
            if name not in transformer_names:
                raise ValueError(
                    f'Attempting to weight transformer "{name}", '
                    'but it is not present in transformer_list.'
                )

    def _iter(self):
        """
        Generate (name, trans, weight) tuples excluding None and
        'drop' transformers.
        """
        get_weight = (self.transformer_weights or {}).get
        return ((name, trans, get_weight(name))
                for name, trans in self.transformer_list)

    def get_feature_names(self):
        """Get feature names from all transformers.
        Returns
        -------
        feature_names : list of strings
            Names of the features produced by transform.
        """
        feature_names = []
        for name, trans, weight in self._iter():
            if not hasattr(trans, 'get_feature_names'):
                raise AttributeError("Transformer %s (type %s) does not "
                                     "provide get_feature_names."
                                     % (str(name), type(trans).__name__))
            feature_names.extend([name + "__" + f for f in
                                  trans.get_feature_names()])
        return feature_names
    @staticmethod
    def get_default_hyper_parameters(cls):
        return {
            'fixed': {
                'transformer-list': []
            },
            'tunable': {

            }
        }
    def fit(self, X, y=None, **fit_params):
        """Fit all transformers using X.
        Parameters
        ----------
        X : iterable or array-like, depending on transformers
            Input data, used to fit transformers.
        y : array-like of shape (n_samples, n_outputs), default=None
            Targets for supervised learning.
        Returns
        -------
        self : FeatureUnion
            This estimator
        """
        transformers = self._parallel_func(X, y, fit_params, _fit_one)
        if not transformers:
            # All transformers are None
            return self

        self._update_transformer_list(transformers)
        return self

    def fit_transform(self, X, y=None, **fit_params):
        """Fit all transformers, transform the data and concatenate results.
        Parameters
        ----------
        X : iterable or array-like, depending on transformers
            Input data to be transformed.
        y : array-like of shape (n_samples, n_outputs), default=None
            Targets for supervised learning.
        Returns
        -------
        X_t : array-like or sparse matrix of \
                shape (n_samples, sum_n_components)
            hstack of results of transformers. sum_n_components is the
            sum of n_components (output dimension) over transformers.
        """
        results = self._parallel_func(X, y, fit_params, _fit_transform_one)
        if not results:
            # All transformers are None
            return np.zeros((X.shape[0], 0))

        Xs, transformers = zip(*results)
        self.transformer_list=transformers

        return self._hstack(Xs)

    def _log_message(self, name, idx, total):
        if not self.verbose:
            return None
        return '(step %d of %d) Processing %s' % (idx, total, name)

    def _parallel_func(self, X, y, fit_params, func):
        """Runs func in parallel on X and y"""
        self.transformer_list = list(self.transformer_list)
        self._validate_transformers()
        self._validate_transformer_weights()
        transformers = list(self._iter())

        return Parallel(n_jobs=self.n_jobs)(delayed(func)(
            transformer, X, y, weight,
            message_clsname='FeatureUnion',
            message=self._log_message(name, idx, len(transformers)),
            **fit_params) for idx, (name, transformer,
                                    weight) in enumerate(transformers, 1))

    def transform(self, X):
        """Transform X separately by each transformer, concatenate results.
        Parameters
        ----------
        X : iterable or array-like, depending on transformers
            Input data to be transformed.
        Returns
        -------
        X_t : array-like or sparse matrix of \
                shape (n_samples, sum_n_components)
            hstack of results of transformers. sum_n_components is the
            sum of n_components (output dimension) over transformers.
        """
        Xs = Parallel(n_jobs=self.n_jobs)(
            delayed(_transform_one)(trans, X, None, weight)
            for name, trans, weight in self._iter())
        if not Xs:
            # All transformers are None
            return np.zeros((X.shape[0], 0))

        return self._hstack(Xs)

    def _hstack(self, Xs):
        if any(sparse.issparse(f) for f in Xs):
            Xs = sparse.hstack(Xs).tocsr()
        else:
            Xs = np.hstack(Xs)
        return Xs

    def _update_transformer_list(self, transformers):
        transformers = iter(transformers)
        self.transformer_list[:] = [(name, old if old == 'drop'
                                     else next(transformers))
                                    for name, old in self.transformer_list]

    @property
    def n_features_in_(self):
        # X is passed to all transformers so we just delegate to the first one
        return self.transformer_list[0][1].n_features_in_

    def persist(self, model_dir):
        """Persist this model into the passed directory."""

        metadata={"pipelines":[]}
        for i, component in enumerate(self.transformer_list):
            pipeline_dir=os.path.join(model_dir, "pipeline_"+str(i))
            create_dir(pipeline_dir)
            update = component.persist(pipeline_dir)
            component_meta = {}#component.hyperparameters
            if update:
                component_meta.update(update)
            component_meta["label"] = module_path_from_object(component)
            component_meta["name"] = component.name

            metadata["pipelines"].append(component_meta)

        return metadata
