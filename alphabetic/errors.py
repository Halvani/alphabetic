class FileNotFoundError(Exception):
    """ Raised if a specific file is not found in the given location. """
    pass

class Non_Existing_ISO_639_2_Langcode(Exception):
    """ Raised if an ISO 639-2 langcode is provided that not exists in the internal json database. """
    pass
