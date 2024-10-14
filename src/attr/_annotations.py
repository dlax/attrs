class Field:
    """Define an attr field with Annotated.

    This behaves similarly to the field() function, but without 'validator'
    and 'converter', which have their own annotation classes.
    """

    __slots__ = (
        "factory",
        "repr",
        "eq",
        "order",
        "hash",
        "init",
        "metadata",
        "kw_only",
        "on_setattr",
        "alias",
    )

    def __init__(
        self,
        *,
        factory=None,
        repr=True,
        eq=None,
        order=None,
        hash=None,
        init=True,
        metadata=None,
        kw_only=False,
        on_setattr=None,
        alias=None,
    ):
        self.factory = factory
        self.repr = repr
        self.eq = eq
        self.order = order
        self.hash = hash
        self.init = init
        self.metadata = metadata
        self.kw_only = kw_only
        self.on_setattr = on_setattr
        self.alias = alias
