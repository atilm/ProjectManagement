class MarkdownConverterException(Exception):
    def __init__(self, lineNumber: int, *args: object) -> None:
        super().__init__(*args)
        self.lineNumber = lineNumber

class HeaderFormatException(MarkdownConverterException):
    pass

class ColumnNumberException(MarkdownConverterException):
    pass

class UnexpectedSectionException(MarkdownConverterException):
    pass

class MissingTableRowException(MarkdownConverterException):
    pass

class ValueConversionException(MarkdownConverterException):
    def __init__(self, inputString: str, lineNumber: int, *args: object) -> None:
        super().__init__(lineNumber, *args)
        self.inputString = inputString