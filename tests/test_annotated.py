from typing import Annotated

import pytest

import attr


@attr.define
class Obj:
    x: Annotated[
        int,
        attr.Field(factory=lambda: 42),
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
