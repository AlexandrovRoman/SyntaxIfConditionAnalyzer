from abc import ABC, abstractmethod

from analyzer.config import KEYWORDS, ALLOWED_CONSTANT_RANGE
from analyzer.exceptions import SyntaxAnalyzeError, SemanticAnalyzeError, AnalyzeError
from analyzer.types import SemanticData


class BaseStateAnalyzer(ABC):
    max_output_literal_len = min_output_literal_len = 1

    def __init__(self, input_str: str, cur_pos: int = 0, semantic_data: SemanticData = None):
        if not semantic_data:
            semantic_data = SemanticData([], [], None, None)
        self.input_str = input_str
        self.cur_pos = cur_pos
        self.semantic_data = semantic_data

    @property
    def relative_str(self) -> str:
        s = self.input_str[self.cur_pos:self.cur_pos + self.max_output_literal_len]
        if len(s) < self.min_output_literal_len:
            raise SyntaxAnalyzeError('Строка закончилась без достижения финального состояния', position=self.cur_pos)
        return s

    def _semantic_analyze_identifiers(self):
        if not self.semantic_data.identifiers:
            return
        identifier = self.semantic_data.identifiers[-1]
        if identifier.lower() in KEYWORDS:
            raise SemanticAnalyzeError(f'{identifier} является зарезервированным словом',
                                       position=self.cur_pos - len(identifier))
        if len(identifier) > 8:
            raise SemanticAnalyzeError(f'{identifier} '
                                       f'слишком длинное название идентификатора',
                                       position=self.cur_pos - len(identifier))

    def _semantic_analyze_constants(self):
        if not self.semantic_data.constants:
            return
        const = self.semantic_data.constants[-1]
        if const not in ALLOWED_CONSTANT_RANGE:
            raise SemanticAnalyzeError(f'{const} выходит за допустимый предел чисел',
                                       position=self.cur_pos - len(str(const)))

    def semantic_analyze(self):
        self._semantic_analyze_identifiers()
        self._semantic_analyze_constants()

    @abstractmethod
    def syntax_analyze(self) -> 'BaseStateAnalyzer':
        pass

    def analyze(self):
        self.semantic_analyze()
        next_state = self.syntax_analyze()
        if not next_state:
            raise AnalyzeError('Функция - анализатор не вернула следующее состояние и не вызвала ошибку',
                               position=self.cur_pos)
        return next_state


class SimpleSpaceTransfer(BaseStateAnalyzer):
    next_state = BaseStateAnalyzer

    def syntax_analyze(self):
        s = self.relative_str[0]
        if s == ' ':
            return self.next_state(self.input_str, self.cur_pos + 1, self.semantic_data)
        raise SyntaxAnalyzeError('Ожидается пробел', position=self.cur_pos)


class LoopSpace(BaseStateAnalyzer):
    error_message = 'Ожидается пробел'

    def syntax_analyze(self):
        s = self.relative_str[0]
        if s == ' ':
            return self.__class__(self.input_str, self.cur_pos + 1, self.semantic_data)
        raise SyntaxAnalyzeError(self.error_message, position=self.cur_pos)


class IdentifierAnalyzer(BaseStateAnalyzer):
    error_message = 'Ожидается цифра или буква'

    def syntax_analyze(self):
        s = self.relative_str[0]
        if s.isalnum():
            self.semantic_data.current_identifier += s
            return self.__class__(self.input_str, self.cur_pos + 1, self.semantic_data)
        raise SyntaxAnalyzeError(self.error_message, position=self.cur_pos)


class NumberAnalyzer(BaseStateAnalyzer):
    error_message = 'Ожидается цифра'

    def syntax_analyze(self):
        s = self.relative_str[0]
        if s.isdigit():
            self.semantic_data.current_constant += s
            return self.__class__(self.input_str, self.cur_pos + 1, self.semantic_data)
        raise SyntaxAnalyzeError(self.error_message, position=self.cur_pos)
