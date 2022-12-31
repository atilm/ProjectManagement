class GraphColorCycle:
    Blue = [0.230, 0.299, 0.754]
    Red = [0.706, 0.016, 0.150]
    Green = [0.085, 0.532, 0.201]
    Purple = [0.436, 0.308, 0.631]
    Orange = [0.759, 0.334, 0.046]
    Gray = [0.5, 0.5, 0.5]

    Colors = [Blue, Red, Green, Purple, Orange]

    def get(number: int) -> list:
        index = number % len(GraphColorCycle.Colors)
        return GraphColorCycle.Colors[index]
    