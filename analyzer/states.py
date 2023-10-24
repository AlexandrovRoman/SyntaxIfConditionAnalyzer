from analyzer.base import BaseStateAnalyzer, SimpleSpaceTransfer, LoopSpace, IdentifierAnalyzer, NumberAnalyzer
from analyzer.exceptions import SyntaxAnalyzeError
from analyzer.types import Identifier, Constant


class Start(LoopSpace):
    max_output_literal_len = 2
    min_output_literal_len = 1
    error_message = 'Ожидается if или пробел'

    def syntax_analyze(self):
        s = self.relative_str
        if s.lower() == 'if':
            return W0(self.input_str, self.cur_pos+2, self.semantic_data)
        return super().syntax_analyze()


class W0(SimpleSpaceTransfer):
    @property
    def next_state(self):
        return G1


class G1(LoopSpace):
    error_message = 'Ожидается пробел или буква'

    def syntax_analyze(self):
        s = self.relative_str
        if s.isalpha():
            self.semantic_data.current_identifier = Identifier(self.cur_pos, s)
            return I0(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class I0(IdentifierAnalyzer):
    error_message = 'Ожидается цифра, буква, пробел или знак сравнения'

    def syntax_analyze(self):
        s = self.relative_str
        if s == ' ':
            self.semantic_data.save_cur_identifier()
            return G2(self.input_str, self.cur_pos+1, self.semantic_data)
        if s in ('<', '>', '='):
            self.semantic_data.save_cur_identifier()
            return C1(self.input_str, self.cur_pos + 1, self.semantic_data)
        return super().syntax_analyze()


class G2(LoopSpace):
    max_output_literal_len = 4
    error_message = 'Ожидается пробел, знак сравнения или then'

    def syntax_analyze(self):
        s = self.relative_str
        if s[0] in ('<', '>', '='):
            self.semantic_data.save_cur_identifier()
            return C1(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s.lower() == 'then':
            return W1(self.input_str, self.cur_pos + 4, self.semantic_data)
        return super().syntax_analyze()


class C1(LoopSpace):
    error_message = 'Ожидается пробел, буква, цифра или знак'

    def syntax_analyze(self):
        s = self.relative_str
        if s.isalpha():
            self.semantic_data.current_identifier = Identifier(self.cur_pos, s)
            return I1(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s == '0':
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return N0(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s in ('+', '-'):
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return Z1(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s.isdigit():
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return N1(self.input_str, self.cur_pos + 1, self.semantic_data)
        return super().syntax_analyze()


class I1(IdentifierAnalyzer):
    error_message = 'Ожидается цифра, буква, пробел или знак сравнения'

    def syntax_analyze(self):
        s = self.relative_str
        if s == ' ':
            self.semantic_data.save_cur_identifier()
            return G2(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class Z1(BaseStateAnalyzer):
    def syntax_analyze(self):
        s = self.relative_str
        if s == '0':
            self.semantic_data.current_constant += s
            return N0(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s.isdigit():
            self.semantic_data.current_constant += s
            return N1(self.input_str, self.cur_pos + 1, self.semantic_data)
        raise SyntaxAnalyzeError('Ожидается цифра', position=self.cur_pos)


class N0(SimpleSpaceTransfer):
    @property
    def next_state(self):
        return G3

    def syntax_analyze(self):
        self.semantic_data.save_cur_constant()
        return super().syntax_analyze()


class N1(NumberAnalyzer):
    error_message = 'Ожидается цифра или пробел'

    def syntax_analyze(self):
        s = self.relative_str
        if s == ' ':
            self.semantic_data.save_cur_constant()
            return G3(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class G3(LoopSpace):
    max_output_literal_len = 4
    error_message = 'Ожидается пробел или then'

    def syntax_analyze(self):
        s = self.relative_str
        if s.lower() == 'then':
            return W1(self.input_str, self.cur_pos+4, self.semantic_data)
        return super().syntax_analyze()


class W1(SimpleSpaceTransfer):
    @property
    def next_state(self):
        return G4


class G4(LoopSpace):
    error_message = 'Ожидается пробел или буква'

    def syntax_analyze(self):
        s = self.relative_str
        if s.isalpha():
            self.semantic_data.current_identifier = Identifier(self.cur_pos, s)
            return I2(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class I2(IdentifierAnalyzer):
    max_output_literal_len = 2

    error_message = 'Ожидается цифра, буква, пробел или :='

    def syntax_analyze(self):
        s = self.relative_str
        if s[0] == ' ':
            self.semantic_data.save_cur_identifier()
            return G5(self.input_str, self.cur_pos+1, self.semantic_data)
        if s == ':=':
            self.semantic_data.save_cur_identifier()
            return W2(self.input_str, self.cur_pos+2, self.semantic_data)
        return super().syntax_analyze()


class G5(LoopSpace):
    max_output_literal_len = 2
    error_message = 'Ожидается пробел или :='

    def syntax_analyze(self):
        s = self.relative_str
        if s == ':=':
            self.semantic_data.current_identifier = Identifier(self.cur_pos, s)
            return W2(self.input_str, self.cur_pos+2, self.semantic_data)
        return super().syntax_analyze()


class W2(LoopSpace):
    error_message = 'Ожидается пробел, буква, цифра или знак'

    def syntax_analyze(self):
        s = self.relative_str
        if s.isalpha():
            self.semantic_data.current_identifier = Identifier(self.cur_pos, s)
            return I3(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s == '0':
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return N2(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s in ('+', '-'):
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return Z2(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s.isdigit():
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return N3(self.input_str, self.cur_pos + 1, self.semantic_data)
        return super().syntax_analyze()


class I3(IdentifierAnalyzer):
    error_message = 'Ожидается цифра, буква, пробел или знак сравнения'

    def syntax_analyze(self):
        s = self.relative_str
        if s == ' ':
            self.semantic_data.save_cur_identifier()
            return G6(self.input_str, self.cur_pos+1, self.semantic_data)
        if s == ';':
            self.semantic_data.save_cur_identifier()
            return F(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class Z2(BaseStateAnalyzer):
    def syntax_analyze(self):
        s = self.relative_str
        if s == '0':
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return N2(self.input_str, self.cur_pos+1, self.semantic_data)
        if s.isdigit():
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return N3(self.input_str, self.cur_pos+1, self.semantic_data)
        raise SyntaxAnalyzeError('Ожидается цифра', position=self.cur_pos)


class N2(SimpleSpaceTransfer):
    @property
    def next_state(self):
        return G6

    def syntax_analyze(self):
        self.semantic_data.save_cur_constant()
        s = self.relative_str
        if s == ';':
            return F(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class N3(NumberAnalyzer):
    error_message = 'Ожидается цифра или пробел'

    def syntax_analyze(self):
        s = self.relative_str
        if s == ' ':
            self.semantic_data.save_cur_constant()
            return G6(self.input_str, self.cur_pos+1, self.semantic_data)
        if s == ';':
            self.semantic_data.save_cur_constant()
            return F(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class G6(LoopSpace):
    max_output_literal_len = 4
    error_message = 'Ожидается пробел, else или ;'

    def syntax_analyze(self):
        s = self.relative_str
        if s[0] == ';':
            return F(self.input_str, self.cur_pos+1, self.semantic_data)
        if s.lower() == 'else':
            return W3(self.input_str, self.cur_pos+4, self.semantic_data)
        return super().syntax_analyze()


class W3(SimpleSpaceTransfer):
    @property
    def next_state(self):
        return G7


class G7(LoopSpace):
    error_message = 'Ожидается пробел или буква'

    def syntax_analyze(self):
        s = self.relative_str
        if s.isalpha():
            self.semantic_data.current_identifier = Identifier(self.cur_pos, s)
            return I4(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class I4(IdentifierAnalyzer):
    max_output_literal_len = 2

    error_message = 'Ожидается цифра, буква, пробел или :='

    def syntax_analyze(self):
        s = self.relative_str
        if s[0] == ' ':
            self.semantic_data.save_cur_identifier()
            return G8(self.input_str, self.cur_pos+1, self.semantic_data)
        if s == ':=':
            self.semantic_data.save_cur_identifier()
            return W4(self.input_str, self.cur_pos+2, self.semantic_data)
        return super().syntax_analyze()


class G8(LoopSpace):
    max_output_literal_len = 2
    error_message = 'Ожидается пробел или :='

    def syntax_analyze(self):
        s = self.relative_str
        if s == ':=':
            self.semantic_data.current_identifier = Identifier(self.cur_pos, s)
            return W4(self.input_str, self.cur_pos+2, self.semantic_data)
        return super().syntax_analyze()


class W4(LoopSpace):
    error_message = 'Ожидается пробел, буква, цифра или знак'

    def syntax_analyze(self):
        s = self.relative_str
        if s.isalpha():
            self.semantic_data.current_identifier = Identifier(self.cur_pos, s)
            return I5(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s == '0':
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return N4(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s in ('+', '-'):
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return Z3(self.input_str, self.cur_pos + 1, self.semantic_data)
        if s.isdigit():
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return N5(self.input_str, self.cur_pos + 1, self.semantic_data)
        return super().syntax_analyze()


class I5(IdentifierAnalyzer):
    error_message = 'Ожидается цифра, буква, пробел или знак сравнения'

    def syntax_analyze(self):
        s = self.relative_str
        if s == ' ':
            self.semantic_data.save_cur_identifier()
            return G9(self.input_str, self.cur_pos+1, self.semantic_data)
        if s == ';':
            self.semantic_data.save_cur_identifier()
            return F(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class Z3(BaseStateAnalyzer):
    def syntax_analyze(self):
        s = self.relative_str
        if s == '0':
            self.semantic_data.current_constant += s
            return N4(self.input_str, self.cur_pos+1, self.semantic_data)
        if s.isdigit():
            self.semantic_data.current_constant = Constant(self.cur_pos, s)
            return N5(self.input_str, self.cur_pos+1, self.semantic_data)
        raise SyntaxAnalyzeError('Ожидается цифра', position=self.cur_pos)


class N4(SimpleSpaceTransfer):
    @property
    def next_state(self):
        return G9

    def syntax_analyze(self):
        self.semantic_data.save_cur_constant()
        s = self.relative_str
        if s == ';':
            return F(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class N5(NumberAnalyzer):
    error_message = 'Ожидается цифра или пробел'

    def syntax_analyze(self):
        s = self.relative_str
        if s == ' ':
            self.semantic_data.save_cur_constant()
            return G9(self.input_str, self.cur_pos+1, self.semantic_data)
        if s == ';':
            self.semantic_data.save_cur_constant()
            return F(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class G9(LoopSpace):
    error_message = 'Ожидается пробел или ;'

    def syntax_analyze(self):
        s = self.relative_str
        if s[0] == ';':
            return F(self.input_str, self.cur_pos+1, self.semantic_data)
        return super().syntax_analyze()


class F(BaseStateAnalyzer):
    def syntax_analyze(self):
        if self.cur_pos < len(self.input_str):
            raise SyntaxAnalyzeError('Достигнуто конечное состояние до конца строки', position=self.cur_pos)

    def analyze(self):
        self.syntax_analyze()
        return self
