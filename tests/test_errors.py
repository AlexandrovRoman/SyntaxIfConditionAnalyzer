import pytest

from analyzer import analyze
from analyzer.exceptions import SyntaxAnalyzeError, SemanticAnalyzeError

test_data = [
    ('IF  E:=314  THEN  A1:=ABC  ELSE A1:=0;', SyntaxAnalyzeError, 'Ожидается цифра, буква, пробел или знак сравнения'),
    ('IF  E=314  TH EN  A1:=ABC  ELSE A1:=0;', SyntaxAnalyzeError, 'Ожидается пробел или then'),
    ('IF  E=314  THEN  A1:=ABC  ', SyntaxAnalyzeError, 'Строка закончилась без достижения финального состояния'),
    ('IF  E=314  THEN  A1:  ELSE A1:=0;', SyntaxAnalyzeError, 'Ожидается цифра, буква, пробел или :='),
    ('IF  E=314  THEN  A1:=1ABC  ELSE A1:=0;', SyntaxAnalyzeError, 'Ожидается цифра или пробел'),
    ('IF  E=0314  THEN  A1:=ABC  ELSE A1:=0;', SyntaxAnalyzeError, 'Ожидается пробел'),
    ('IF  Elim4n8c348nxnjkldv=314  THEN  A1:=ABC  ELSE A1:=0;', SemanticAnalyzeError,
     'Elim4n8c348nxnjkldv слишком длинное название идентификатора'),
    ('IF  E=-32769  THEN  A1:=ABC  ELSE A1:=0;', SemanticAnalyzeError, '-32769 выходит за допустимый предел чисел'),
    ('IF  E82G=314  THEN  A1:=ABC  ELSE else:=0;', SemanticAnalyzeError, 'else является зарезервированным словом'),
    ('IF  E=314  THEN  tHen:=ABC  ELSE A1:=0;', SemanticAnalyzeError, 'tHen является зарезервированным словом'),
    ('IF  iF=314  THEN  A1:=ABC  ELSE A1:=0;', SemanticAnalyzeError, 'iF является зарезервированным словом'),
]


@pytest.mark.parametrize("inp,expected_ex,msg", test_data)
def test_analyze_normal(inp, expected_ex, msg):
    with pytest.raises(expected_ex, match=msg):
        analyze(inp)
