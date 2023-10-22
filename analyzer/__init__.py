from analyzer.states import Start, F


def analyze(input_str: str) -> F:
    state = Start(input_str)
    while not isinstance(state, F):
        state = state.analyze()
    return state.analyze()
