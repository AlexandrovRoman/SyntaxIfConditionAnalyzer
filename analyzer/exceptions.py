class AnalyzeError(Exception):
    """ Базовый класс ошибки. Дополнительно хранит в себе позицию, на которой она произошла """

    def __init__(self, message: str, *, position: int):
        super().__init__(message)
        self.position = position


class SyntaxAnalyzeError(AnalyzeError):
    pass


class SemanticAnalyzeError(AnalyzeError):
    pass
