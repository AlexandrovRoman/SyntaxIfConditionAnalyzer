import pytest

from analyzer import analyze
from analyzer.types import SemanticData

test_data = [
    ('     iF  A=3  THEN  A1:=ABC;', SemanticData(['A', 'A1', 'ABC'], [3])),
    (' If  E<C  ThEn  A1:=10;', SemanticData(['E', 'C', 'A1'], [10])),
    ('IF  E8c>+314  then  A1:=ABC  ELSE A1 := BCD ;', SemanticData(['E8c', 'A1', 'ABC', 'BCD'], [314])),
    ('IF  E=-314  THEN  A1:=ABC  ELSE A1:=0;', SemanticData(['E', 'A1', 'ABC'], [-314, 0])),
]


@pytest.mark.parametrize("inp,expected", test_data)
def test_analyze_normal(inp, expected):
    final_state = analyze(inp)
    assert final_state.semantic_data == expected
