from ..permset_unbounded import PermSetUnbounded


class PermSetDescribed(PermSetUnbounded):
    """A base class for unbounded perm sets."""
    # TODO: Make things abstract properties as a solution?

    # TODO: These two attribute needs to be defined in all immediate subclasses
    DEFAULT_CLASS = None
    DESCRIPTOR_CLASS = None

    # TODO: This needs to be defined in classes for specific descriptors
    DESCRIPTOR = None

    def __init__(self, descriptor):
        self._descriptor = descriptor
