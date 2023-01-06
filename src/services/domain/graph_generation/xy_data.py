class XyData:
    def __init__(self) -> None:
        self.x = []
        self.y = []
        self.color = []

    def append(self, x, y, color) -> None:
        self.x.append(x)
        self.y.append(y)
        self.color.append(color)