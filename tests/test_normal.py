import pytest

from analyzer import analyze
from analyzer.types import SemanticData, Identifier, Constant

test_data = [
    ('     iF  A=3  THEN  A1:=ABC;', SemanticData(
        [Identifier(9, 'A'), Identifier(20, 'A1'), Identifier(24, 'ABC')], [Constant(11, '3')])
     ),
    (' If  E<C  ThEn  A1:=10;', SemanticData(
        [Identifier(5, 'E'), Identifier(7, 'C'), Identifier(16, 'A1')], [Constant(20, '10')])),
    ('IF  E8c>+314  then  A1:=ABC  ELSE A1 := BCD ;', SemanticData(
        [Identifier(4, 'E8c'),
         Identifier(20, 'A1'),
         Identifier(24, 'ABC'),
         Identifier(34, 'A1'),
         Identifier(40, 'BCD')], [Constant(8, '+314')]
    )
     ),
    ('IF  E=-314  THEN  A1:=ABC  ELSE A1:=0;', SemanticData(
        [Identifier(4, 'E'),
         Identifier(18, 'A1'),
         Identifier(22, 'ABC'),
         Identifier(32, 'A1')],
        [Constant(6, '-314'), Constant(36, '0')]
    )
     ),
]


@pytest.mark.parametrize("inp,expected", test_data)
def test_analyze_normal(inp, expected):
    semantic_data = analyze(inp)
    assert semantic_data == expected
