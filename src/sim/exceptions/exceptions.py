class NotImplementedWarning(Exception):
    def __init__(self, msg=None):
        super(NotImplementedWarning, self).__init__(msg)
