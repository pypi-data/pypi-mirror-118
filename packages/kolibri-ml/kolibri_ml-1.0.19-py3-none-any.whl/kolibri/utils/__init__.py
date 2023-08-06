from contextlib import contextmanager
import timeit
from distutils.version import LooseVersion
import joblib
try:
    from pkg_resources import parse_version  # type: ignore
except ImportError:
    # setuptools not installed
    parse_version = LooseVersion  # type: ignore

@contextmanager
def _print_elapsed_time(source, message=None):
    """Log elapsed time to stdout when the context is exited.
    Parameters
    ----------
    source : str
        String indicating the source or the reference of the message.
    message : str, default=None
        Short message. If None, nothing will be printed.
    Returns
    -------
    context_manager
        Prints elapsed time upon exit if verbose.
    """
    if message is None:
        yield
    else:
        start = timeit.default_timer()
        yield
        print(
            _message_with_time(source, message,
                               timeit.default_timer() - start))



def _message_with_time(source, message, time):
    """Create one line message for logging purposes.
    Parameters
    ----------
    source : str
        String indicating the source or the reference of the message.
    message : str
        Short message.
    time : int
        Time in seconds.
    """
    start_message = "[%s] " % source

    # adapted from joblib.logger.short_format_time without the Windows -.1s
    # adjustment
    if time > 60:
        time_str = "%4.1fmin" % (time / 60)
    else:
        time_str = " %5.1fs" % time
    end_message = " %s, total=%s" % (message, time_str)
    dots_len = (70 - len(start_message) - len(end_message))
    return "%s%s%s" % (start_message, dots_len * '.', end_message)


def check_memory(memory):
    """Check that ``memory`` is joblib.Memory-like.
    joblib.Memory-like means that ``memory`` can be converted into a
    joblib.Memory instance (typically a str denoting the ``location``)
    or has the same interface (has a ``cache`` method).
    Parameters
    ----------
    memory : None, str or object with the joblib.Memory interface
    Returns
    -------
    memory : object with the joblib.Memory interface
    Raises
    ------
    ValueError
        If ``memory`` is not joblib.Memory-like.
    """

    if memory is None or isinstance(memory, str):
        if parse_version(joblib.__version__) < parse_version('0.12'):
            memory = joblib.Memory(cachedir=memory, verbose=0)
        else:
            memory = joblib.Memory(location=memory, verbose=0)
    elif not hasattr(memory, 'cache'):
        raise ValueError("'memory' should be None, a string or have the same"
                         " interface as joblib.Memory."
                         " Got memory='{}' instead.".format(memory))
    return memory