from dataclasses import dataclass
from typing import Optional


@dataclass
class SemanticData:
    identifiers: list[str]
    constants: list[int]
    current_identifier: Optional[str]
    current_constant: Optional[str]

    def save_cur_identifier(self):
        if self.current_identifier and self.current_identifier not in self.identifiers:
            self.identifiers.append(self.current_identifier)
        self.current_identifier = None

    def save_cur_constant(self):
        if self.current_constant:
            if (const := int(self.current_constant)) not in self.constants:
                self.constants.append(const)
        self.current_constant = None
