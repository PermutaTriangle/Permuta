from ..PermSetUnbounded import PermSetUnbounded


class PermSetDescribed(PermSetUnbounded):
    def __init__(self, descriptor):
        self.descriptor = descriptor
