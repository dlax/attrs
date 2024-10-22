from typing import Annotated

import pytest

import attr

from attr.validators import Gt, lt


def validate_x(obj, attribute, value):
    if value == 41:
        raise ValueError("forbidden value")


@attr.define
class Obj:
    x: Annotated[
        int,
        attr.Field(factory=lambda: 42),
        attr.Validator(validate_x),
        attr.Validator(lt(100)),
        Gt(-1),
    ]
    y: Annotated[
        int,
        attr.Field(kw_only=True),
        attr.Converter(lambda v: -v),
        attr.Converter(lambda v: v * 10),
    ]
    z: Annotated[str, attr.Field(), attr.Converter(str)] = "z"
    a: Annotated[str, attr.Field(init=False)] = "a"


@pytest.mark.parametrize(
    ("obj", "d"),
    [
        (Obj(x=0, y=123), {"a": "a", "x": 0, "y": -1230, "z": "z"}),
        (Obj(y=9, z=1), {"a": "a", "x": 42, "y": -90, "z": "1"}),
    ],
)
def test_base(obj, d):
    """Annotated Obj is initialized from valid values."""
    assert d == attr.asdict(obj)


def test_init_false():
    """Fields with init=False are respected in Annotated."""
    with pytest.raises(TypeError, match=r"unexpected keyword argument 'a'"):
        Obj(y=1, a="b")


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"x": 41, "y": 0}, "forbidden"),
        ({"x": -2, "y": 0}, "'x' must be > -1: -2"),
        ({"x": 102, "y": 0}, "'x' must be < 100: 102"),
    ],
)
def test_valid(kwargs, match):
    """Annotated Obj fails to initialize from invalid values."""
    with pytest.raises(ValueError, match=match):
        Obj(**kwargs)


def test_multiple_field_annotations():
    """Passing several Field annotations raises a ValueError."""

    class Invalid:
        f: Annotated[str, attr.Field(), attr.Field()]

    with pytest.raises(
        ValueError, match="only one Field annotation may be specified"
    ):
        attr.define(Invalid)


def test_converters_with_field_annotation():
    """A Field annotation is required to use a Converter annotation."""

    class Invalid:
        f: Annotated[int, attr.Converter(lambda x: x)]

    with pytest.raises(
        ValueError, match="Converter annotations must be used along with Field"
    ):
        attr.define(Invalid)


def test_validators_with_field_annotation():
    """A Field annotation is required to use a Validator annotation."""

    class Invalid:
        f: Annotated[int, attr.Validator(lambda x: x)]

    with pytest.raises(
        ValueError, match="Validator annotations must be used along with Field"
    ):
        attr.define(Invalid)
