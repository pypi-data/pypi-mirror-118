from typing import *


class Map:
    def __init__(self, path: list, name: str, backgroundColor: Tuple[int], pathColor: Tuple[int], displayColor: Tuple[int] = None):
        self.name = name
        self.path = path
        self.backgroundColor = backgroundColor
        self.pathColor = pathColor
        self.displayColor = self.backgroundColor if displayColor is None else displayColor
        # print(self.name, sum([abs(self.path[n][0] - self.path[n+1][0]) + abs(self.path[n][1] - self.path[n+1][1]) for n in range(len(self.path) - 1)]))

    def __str__(self):
        return self.name

Maps = [
    Map([[25, 0], [25, 375], [775, 375], [775, 25], [40, 25], [40, 360], [760, 360], [760, 40], [55, 40], [55, 345], [745, 345], [745, 55], [0, 55]], 'Race Track', (19, 109, 21), (189, 22, 44), (189, 22, 44)),
    Map([[400, 225], [400, 50], [50, 50], [50, 400], [50, 50], [750, 50], [750, 400], [750, 50], [400, 50], [400, 225]], 'The Sky', (171, 205, 239), (255, 255, 255)),
    Map([[0, 25], [775, 25], [775, 425], [25, 425], [25, 75], [725, 75], [725, 375], [0, 375]], 'Wizard\'s Lair', (187, 11, 255), (153, 153, 153)),
    Map([[0, 25], [700, 25], [700, 375], [100, 375], [100, 75], [800, 75]], 'Pond', (6, 50, 98), (0, 0, 255)),
    Map([[0, 400], [725, 400], [725, 325], [650, 325], [650, 375], [750, 375], [750, 75], [650, 75], [650, 125], [725, 125], [725, 50], [0, 50]], 'The Moon', (100, 100, 100), (255, 255, 102), (255, 255, 102)),
    Map([[25, 0], [25, 425], [525, 425], [525, 25], [275, 25], [275, 275], [750, 275], [750, 0]], 'Plains', (19, 109, 21), (155, 118, 83)),
    Map([[0, 25], [475, 25], [575, 125], [575, 275], [475, 375], [325, 375], [225, 275], [225, 125], [325, 25], [800, 25]], 'Octagon', (218, 112, 214), (0, 255, 255)),
    Map([[350, 0], [350, 150], [25, 150], [25, 300], [350, 300], [350, 450], [450, 450], [450, 300], [775, 300], [775, 150], [450, 150], [450, 0]], 'Candyland', (255, 105, 180), (199, 21, 133)),
    Map([[300, 225], [575, 225], [575, 325], [125, 325], [125, 125], [675, 125], [675, 425], [25, 425], [25, 0]], 'Lava Spiral', (207, 16, 32), (255, 140, 0), (178, 66, 0)),
    Map([[0, 25], [750, 25], [750, 200], [25, 200], [25, 375], [800, 375]], 'Desert', (170, 108, 35), (178, 151, 5)),
    Map([[125, 0], [125, 500], [400, 500], [400, -50], [675, -50], [675, 500]], 'Disconnected', (64, 64, 64), (100, 100, 100), (100, 0, 0)),
    Map([[0, 225], [800, 225]], 'The End', (100, 100, 100), (200, 200, 200))
]
