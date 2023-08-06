"""Test the @classproperty decorators."""

from utilp.decorators import classproperty


class Bar(object):

    _bar = 1

    @classproperty
    def bar(cls):
        return cls._bar

    @bar.setter
    def bar(cls, value):
        cls._bar = value


def test_class_property():
    # test instance instantiation
    foo = Bar()
    assert foo.bar == 1

    baz = Bar()
    assert baz.bar == 1

    # test static variable
    baz.bar = 5
    assert foo.bar == 5

    # test setting variable on the class
    Bar.bar = 50
    assert baz.bar == 50
    assert foo.bar == 50
