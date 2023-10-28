from src.services.domain.representation_writing.model_to_representation_converter import IModelToRepresentationConverter
from src.domain.completion_date_history import *
from src.services.markdown.markdown_document import MarkdownDocument
from src.services.markdown.markdown_document_builder import *

class ModelToMarkdownTrackingFileConverter(IModelToRepresentationConverter):
    def convert(self, history : CompletionDateHistory) -> MarkdownDocument:
        builder = MarkdownDocumentBuilder()\
            .withSection(f"{history.projectId} completion dates", 0)\
            .withTable(self._records_to_table(history.records))
        
        return builder.build()
        
    def _records_to_table(self, records: list[CompletionDateRecord]):
        builder = MarkdownTableBuilder()\
            .withHeader("Date", "Earliest", "Probable", "Latest", "Comment")
        return builder.build()