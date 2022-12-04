class IdGenerator:
    def __init__(self) -> None:
        self._id_counter = 0

    def next(self):
        self._id_counter += 1
        return f"{self._id_counter}"