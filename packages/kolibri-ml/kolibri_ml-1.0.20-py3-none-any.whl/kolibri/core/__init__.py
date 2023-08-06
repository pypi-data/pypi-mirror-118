import copy

def clone(estimator, *, safe=True):
    """Constructs a new unfitted estimator with the same parameters.
    Clone does a deep copy of the model in an estimator
    without actually copying attached data. It yields a new estimator
    with the same parameters that has not been fitted on any data.
    If the estimator's `random_state` parameter is an integer (or if the
    estimator doesn't have a `random_state` parameter), an *exact clone* is
    returned: the clone and the original estimator will give the exact same
    results. Otherwise, *statistical clone* is returned: the clone might
    yield different results from the original estimator. More details can be
    found in :ref:`randomness`.
    Parameters
    ----------
    estimator : {list, tuple, set} of estimator instance or a single \
            estimator instance
        The estimator or group of estimators to be cloned.
    safe : bool, default=True
        If safe is False, clone will fall back to a deep copy on objects
        that are not estimators.
    """
    estimator_type = type(estimator)
    # XXX: not handling dictionaries
    if estimator_type in (list, tuple, set, frozenset):
        return estimator_type([clone(e, safe=safe) for e in estimator])
    elif not hasattr(estimator, 'get_params') or isinstance(estimator, type):
        if not safe:
            return copy.deepcopy(estimator)
        else:
            if isinstance(estimator, type):
                raise TypeError("Cannot clone object. " +
                                "You should provide an instance of " +
                                "scikit-learn estimator instead of a class.")
            else:
                raise TypeError("Cannot clone object '%s' (type %s): "
                                "it does not seem to be a scikit-learn "
                                "estimator as it does not implement a "
                                "'get_params' method."
                                % (repr(estimator), type(estimator)))

    klass = estimator.__class__
    new_object_params = estimator.get_params(deep=False)
    for name, param in new_object_params.items():
        new_object_params[name] = clone(param, safe=False)
    new_object = klass(**new_object_params)
    params_set = new_object.get_params(deep=False)

    # quick sanity check of the parameters of the clone
    for name in new_object_params:
        param1 = new_object_params[name]
        param2 = params_set[name]
        if param1 is not param2:
            raise RuntimeError('Cannot clone object %s, as the constructor '
                               'either does not set or modifies parameter %s' %
                               (estimator, name))
    return new_object