from ..PermSetUnbounded import PermSetUnbounded


class PermSetDescribed(PermSetUnbounded):
    descriptor = None
    def __init__(self, descriptor):
        self.descriptor = descriptor
