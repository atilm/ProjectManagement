class FibonacciSequence:
    sequence = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    def predecessor(number: int) -> int:
        index = FibonacciSequence.sequence.index(number)
        return FibonacciSequence.sequence[index - 1]

    def successor(number: int) -> int:
        index = FibonacciSequence.sequence.index(number)
        return FibonacciSequence.sequence[index + 1]
