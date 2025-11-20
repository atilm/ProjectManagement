from .representation_writer import IRepresentationWriter
from .model_to_representation_converter import IModelToRepresentationConverter
from projman.src.services.markdown.markdown_writer import MarkdownWriter

class MarkdownRepresentationWriter(IRepresentationWriter):
    def __init__(self, converter: IModelToRepresentationConverter) -> None:
        super().__init__()
        self.converter = converter

    def write(self, domain_model: object) -> str:
        document = self.converter.convert(domain_model)
        writer = MarkdownWriter()
        return writer.write(document)
