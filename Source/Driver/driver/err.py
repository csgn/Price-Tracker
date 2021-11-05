from abc import ABC


class __Error(ABC, Exception):
    pass


class ConnectionError(__Error):
    pass


class TableNotFoundError(__Error):
    pass


class TableDoesNotExistsError(__Error):
    pass


class TableNotCreatedError(__Error):
    pass
