class ExternalException(Exception):
    pass


class DatabaseException(ExternalException):
    pass


class MessageProducerException(ExternalException):
    pass


class LineProviderException(ExternalException):
    pass
