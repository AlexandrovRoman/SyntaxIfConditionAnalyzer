from abc import ABC, abstractmethod

from analyzer.exceptions import SyntaxAnalyzeError, AnalyzeError
from analyzer.types import SemanticData


class BaseStateAnalyzer(ABC):
    """ Базовый класс состояния """

    max_output_literal_len = min_output_literal_len = 1

    def __init__(self, input_str: str, cur_pos: int = 0, semantic_data: SemanticData = None):
        if not semantic_data:
            semantic_data = SemanticData([], [])
        self.input_str = input_str
        self.cur_pos = cur_pos
        self.semantic_data = semantic_data

    @property
    def relative_str(self) -> str:
        """ Срез строки с текущей позиции на длину max_output_literal_len, с проверкой на окончание строки """
        s = self.input_str[self.cur_pos:self.cur_pos + self.max_output_literal_len]
        if len(s) < self.min_output_literal_len:
            raise SyntaxAnalyzeError('Строка закончилась без достижения финального состояния', position=self.cur_pos)
        return s

    @abstractmethod
    def syntax_analyze(self) -> 'BaseStateAnalyzer':
        """ Возвращает следующее состояние. Если не получилось его определить - вызывает синтаксическую ошибку """

    def analyze(self):
        """ Получает следующее состояние. Если вернулось None и не вызвалась ошибка - вызываем её """

        next_state = self.syntax_analyze()
        if not next_state:
            raise AnalyzeError('Функция - анализатор не вернула следующее состояние и не вызвала ошибку',
                               position=self.cur_pos)
        return next_state


class SimpleSpaceTransfer(BaseStateAnalyzer):
    """ Универсальный класс для перехода через пробел в следующее состояние """

    next_state = BaseStateAnalyzer

    def syntax_analyze(self):
        s = self.relative_str[0]
        if s == ' ':
            return self.next_state(self.input_str, self.cur_pos + 1, self.semantic_data)
        raise SyntaxAnalyzeError('Ожидается пробел', position=self.cur_pos)


class LoopSpace(BaseStateAnalyzer):
    """ Универсальный класс для состояний, в которых возможно любое количество пробелов """

    error_message = 'Ожидается пробел'

    def syntax_analyze(self):
        s = self.relative_str[0]
        if s == ' ':
            return self.__class__(self.input_str, self.cur_pos + 1, self.semantic_data)
        raise SyntaxAnalyzeError(self.error_message, position=self.cur_pos)


class IdentifierAnalyzer(BaseStateAnalyzer):
    """ Универсальный класс для набора идентификатора """

    error_message = 'Ожидается цифра или буква'

    def syntax_analyze(self):
        s = self.relative_str[0]
        if s.isalnum():
            self.semantic_data.current_identifier += s
            return self.__class__(self.input_str, self.cur_pos + 1, self.semantic_data)
        raise SyntaxAnalyzeError(self.error_message, position=self.cur_pos)


class NumberAnalyzer(BaseStateAnalyzer):
    """ Универсальный класс для набора константы """

    error_message = 'Ожидается цифра'

    def syntax_analyze(self):
        s = self.relative_str[0]
        if s.isdigit():
            self.semantic_data.current_constant += s
            return self.__class__(self.input_str, self.cur_pos + 1, self.semantic_data)
        raise SyntaxAnalyzeError(self.error_message, position=self.cur_pos)
