from typing import TYPE_CHECKING

from analyzer.config import KEYWORDS, ALLOWED_CONSTANT_RANGE, MAX_IDENTIFIER_LEN
from analyzer.exceptions import SemanticAnalyzeError
if TYPE_CHECKING:
    from analyzer.types import Identifier, Constant


def semantic_analyze_identifier(identifier: 'Identifier'):
    """ Проверка семантических критериев идентификатора """

    if identifier.value.lower() in KEYWORDS:
        raise SemanticAnalyzeError(f'{identifier} является зарезервированным словом',
                                   position=identifier.start_pos)
    if len(identifier.value) > MAX_IDENTIFIER_LEN:
        raise SemanticAnalyzeError(f'{identifier} '
                                   f'слишком длинное название идентификатора',
                                   position=identifier.start_pos)


def semantic_analyze_constant(const: 'Constant'):
    """ Проверка семантических критериев константы """

    if const.value not in ALLOWED_CONSTANT_RANGE:
        raise SemanticAnalyzeError(f'{const} выходит за допустимый предел чисел',
                                   position=const.start_pos)
