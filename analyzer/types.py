from dataclasses import dataclass
from typing import Optional


@dataclass
class Identifier:
    start_pos: int
    value: str

    def __add__(self, other: str):
        self.value += other
        return self

    def __str__(self):
        return self.value


@dataclass
class Constant:
    start_pos: int
    _value: str

    @property
    def value(self) -> int:
        return int(self._value)

    def __add__(self, other: str):
        self._value += other
        return self

    def __str__(self):
        return str(self.value)


@dataclass
class SemanticData:
    identifiers: list[Identifier]
    constants: list[Constant]
    current_identifier: Optional[Identifier] = None
    current_constant: Optional[Constant] = None

    def save_cur_identifier(self):
        if self.current_identifier and not any(self.current_identifier.value == identifier
                                               for identifier in self.identifiers):
            self.identifiers.append(self.current_identifier)
        self.current_identifier = None

    def save_cur_constant(self):
        if self.current_constant and not any(self.current_constant.value == constant
                                             for constant in self.constants):
            self.constants.append(self.current_constant)
        self.current_constant = None
