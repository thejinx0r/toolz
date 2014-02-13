import itertools


no_replace = '__no__replace__'


# SANDBOX: this may be a good addition to a `sampling` module
def jackknife(seq, replace=no_replace):
    """ Repeatedly iterate over seq, each time omitting a successive element

    Elements may be replaced by a value insted of omitted.

    If `seq` is an iterator, it will be read into memory.

    >>> list(list(x) for x in jackknife(range(4)))
    [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]

    >>> list(list(x) for x in jackknife(range(4), replace=None))
    [[None, 1, 2, 3], [0, None, 2, 3], [0, 1, None, 3], [0, 1, 2, None]]

    Note that an iterator of iterators is returned so the data in ``seq`` is
    only in memory once.  If an iterator of tuples is desired, you may do:

    >>> jackknife = compose(curry(map, tuple), jackknife)  # doctest: +SKIP
    >>> list(jackknife([1, 2, 3]))  # doctest: +SKIP
    [(2, 3), (1, 3), (1, 2)]

    See Also:
        itertools.combinations
    """
    if replace is no_replace:
        replace = ()
    else:
        replace = (replace,)

    # If `seq` is an iterator, read it into memory.
    # Note: If we add more functions that resample an iterable, perhaps
    #       consider adding a new convention of allowing a callable that
    #       (re-)creates the iterable to be passed in place of `seq`.
    itcounter = iter(seq)
    if itcounter is seq:
        seq = list(seq)
        itcounter = iter(seq)

    for i, _ in enumerate(itcounter):
        it = iter(seq)
        yield itertools.chain(itertools.islice(it, i), replace,
                              itertools.islice(it, 1, None))


def do(func, x):
    """ Runs ``func`` on ``x``, returns ``x``

    Because the results of ``func`` are not returned, only the side
    effects of ``func`` are relevant.

    Logging functions can be made by composing ``do`` with a storage function
    like ``list.append`` or ``file.write``

    >>> from toolz import compose, curry
    >>> from toolz.sandbox.core import do
    >>> do = curry(do)

    >>> log = []
    >>> inc = lambda x: x + 1
    >>> inc = compose(inc, do(log.append))
    >>> inc(1)
    2
    >>> inc(11)
    12
    >>> log
    [1, 11]

    """
    func(x)
    return x
