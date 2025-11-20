class IRepresentationToModelConverter:
    """This is the to convert a data source's in-memory-representation
    into the domain model. E.g. markdown document to repository collection"""
    def convert(self, source : object) -> object:
        pass