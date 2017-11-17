from time import sleep

from nose.tools import eq_

from anycache import AnyCache


def test_maxsize_0():
    """Disable Caching."""
    ac = AnyCache(maxsize=0)

    @ac.decorate()
    def myfunc(posarg, kwarg=3):
        # count the number of calls
        myfunc.callcount += 1
        return posarg + kwarg
    myfunc.callcount = 0

    eq_(myfunc(4, 5), 9)
    eq_(myfunc.callcount, 1)
    eq_(myfunc(4, 2), 6)
    eq_(myfunc.callcount, 2)
    eq_(myfunc(4, 2), 6)
    eq_(myfunc.callcount, 3)
    eq_(ac.size, 0)


def test_maxsize_none():
    """Unlimited Caching."""
    ac = AnyCache(maxsize=None)

    @ac.decorate()
    def myfunc(posarg, kwarg=3):
        # count the number of calls
        myfunc.callcount += 1
        return posarg + kwarg
    myfunc.callcount = 0

    eq_(myfunc(4, 2), 6)
    size1 = ac.size
    n = 5
    calls = n * n

    for posarg in range(n):
        for kwarg in range(n):
            eq_(myfunc(posarg, kwarg), posarg+kwarg)
    eq_(calls * size1, ac.size)
    eq_(myfunc.callcount, calls)

    ac.clear()
    eq_(ac.size, 0)


def test_maxsize_value():
    """Limited Caching."""
    ac = AnyCache(maxsize=None, debug=True)

    @ac.decorate()
    def myfunc(posarg, kwarg=3):
        # count the number of calls
        myfunc.callcount += 1
        sleep(2)  # wait for slow windows file system
        return posarg + kwarg
    myfunc.callcount = 0

    eq_(myfunc(4, 2), 6)
    size1 = ac.size
    n = 3
    calls = n * n

    for maxsize in (5*size1, 8*size1):
        ac.clear()
        myfunc.callcount = 0
        ac.maxsize = maxsize

        for posarg in range(n):
            for kwarg in range(n):
                eq_(myfunc(posarg, kwarg), posarg+kwarg)
        eq_(maxsize, ac.size)
        eq_(myfunc.callcount, calls)
        # last should be in cache
        eq_(myfunc(posarg, kwarg), posarg+kwarg)
        eq_(maxsize, ac.size)
        eq_(myfunc.callcount, calls)