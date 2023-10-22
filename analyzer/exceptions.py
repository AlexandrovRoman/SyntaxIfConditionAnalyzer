class AnalyzeError(Exception):
    def __init__(self, message: str, *, position: int):
        super().__init__(message)
        self.position = position


class SyntaxAnalyzeError(AnalyzeError):
    pass


class SemanticAnalyzeError(AnalyzeError):
    pass
