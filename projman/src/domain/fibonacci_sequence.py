class FibonacciSequence:
    sequence = [0, 1, 2, 3, 5, 8, 13, 20, 21, 34, 40, 55, 100]

    def is_in_sequence(value: float):
        return value in FibonacciSequence.sequence[1:-1]

    def predecessor(number: int) -> int:
        index = FibonacciSequence.sequence.index(number)
        return FibonacciSequence.sequence[index - 1]

    def successor(number: int) -> int:
        index = FibonacciSequence.sequence.index(number)
        return FibonacciSequence.sequence[index + 1]
