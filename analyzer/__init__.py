from analyzer.states import Start, F
from analyzer.types import SemanticData


def analyze(input_str: str) -> SemanticData:
    state = Start(input_str)
    while not isinstance(state, F):
        state = state.analyze()
    final_state: F = state.analyze()
    return final_state.semantic_data
