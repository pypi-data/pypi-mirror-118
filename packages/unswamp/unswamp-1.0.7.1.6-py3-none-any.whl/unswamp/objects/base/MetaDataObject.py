class MetaDataObject:
    ##################################################################################################
    # Constructor
    ##################################################################################################
    def __init__(self, meta_data=None):
        if meta_data is None:
            meta_data = {}
        self.meta_data = meta_data

    ##################################################################################################
    # Properties
    ##################################################################################################
    @property
    def meta_data(self):
        return self._meta_data

    @meta_data.setter
    def meta_data(self, value):
        self._meta_data = value
