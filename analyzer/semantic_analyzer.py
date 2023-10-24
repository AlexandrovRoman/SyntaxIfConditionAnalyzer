from analyzer.config import KEYWORDS, ALLOWED_CONSTANT_RANGE
from analyzer.exceptions import SemanticAnalyzeError
from analyzer.types import Identifier, Constant, SemanticData


def _semantic_analyze_identifier(identifier: Identifier):
    if identifier.value.lower() in KEYWORDS:
        raise SemanticAnalyzeError(f'{identifier} является зарезервированным словом',
                                   position=identifier.start_pos)
    if len(identifier.value) > 8:
        raise SemanticAnalyzeError(f'{identifier} '
                                   f'слишком длинное название идентификатора',
                                   position=identifier.start_pos)


def _semantic_analyze_identifiers(identifiers: list[Identifier]):
    for identifier in identifiers:
        _semantic_analyze_identifier(identifier)


def _semantic_analyze_constant(const: Constant):
    if const.value not in ALLOWED_CONSTANT_RANGE:
        raise SemanticAnalyzeError(f'{const} выходит за допустимый предел чисел',
                                   position=const.start_pos)


def _semantic_analyze_constants(constants: list[Constant]):
    for const in constants:
        _semantic_analyze_constant(const)


def semantic_analyze(semantic_data: SemanticData):
    _semantic_analyze_identifiers(semantic_data.identifiers)
    _semantic_analyze_constants(semantic_data.constants)
