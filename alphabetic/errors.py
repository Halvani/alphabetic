class FileNotFoundError(Exception):
    """ Raised if a specific file is not found in the given location. """
    pass


class UnsupportedLanguage(Exception):
    """ Raised if a specific language is not currently supported. """
    pass
