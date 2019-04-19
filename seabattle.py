import random as rnd

EMPTY = ' '
DEAD = 'X'
HIT = '+'
MISSED = '-'
SHIP = 'O'

LETTERKEYS = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J'
]

def digit(key):
    if key in LETTERKEYS:
        return LETTERKEYS.index(key) + 1
    elif 1 <= key <= 10:
        return key
    else:
        raise ValueError


def area(posx, posy):
    res = []
    for i in range(3):
        for j in range(3):
            res.append((posx - 1 + i, posy - 1 + j))
    return res


def around(posx, posy):
    return [a for a in area(posx, posy) if
            not (a[0] == posx and a[1] == posy) and (1 <= a[0] <= 10 and 1 <= a[1] <= 10)]


# Класс-родитель корабля
class SBGameShip:
    def __init__(self, field, angle = None, length = None, posx = None, posy = None):
        self.angle = 0 if angle is None else angle
        self.length = 0 if length is None else length
        self.posx = 0 if not posx else posx
        self.posy = 0 if not posy else posy
        self.field = field
        self.cells = list()

    def __randomcoords(self):
        posx = 0
        posy = 0
        self.angle = rnd.randint(0, 3)
        if self.angle == 0:
            posx = rnd.randint(self.length, self.field.xlength)
            posy = rnd.randint(1, self.field.ylength)
        elif self.angle == 1:
            posx = rnd.randint(1, self.field.xlength)
            posy = rnd.randint(1, self.field.ylength - self.length)
        elif self.angle == 2:
            posx = rnd.randint(1, self.field.xlength - self.length)
            posy = rnd.randint(1, self.field.ylength)
        elif self.angle == 3:
            posx = rnd.randint(1, self.field.xlength)
            posy = rnd.randint(self.length, self.field.ylength)

        self.posx = posx
        self.posy = posy

        self.gen_cells()

    def gen_cells(self):
        if self.angle == 0:
            self.cells = [[self.posx - cell, self.posy, False] for cell in range(self.length)]
        elif ship.angle == 1:
            self.cells = [[self.posx, self.posy + cell, False] for cell in range(self.length)]
        elif ship.angle == 2:
            self.cells = [[self.posx + cell, self.posy, False] for cell in range(self.length)]
        elif ship.angle == 3:
            self.cells = [[self.posx, self.posy - cell, False] for cell in range(self.length)]

    def randompos(self):
        ship_not_put = True
        while(ship_not_put):
            try:
                self.__randomcoords()
                self.field.put_ship(self)
                ship_not_put = False
            except ValueError:
                pass

    def isdead(self):
        return False not in [a[2] for a in self.cells]

    def around(self):
        res = set()
        own_cells = [(cell[0], cell[1]) for cell in self.cells]
        for cell in own_cells:
            for a in around(cell[0], cell[1]):
                if a not in own_cells:
                    res.add(a)
        res = list(res)
        res = [a for a in res if 1 <= a[0] <= 10 and 1 <= a[1] <= 10]
        return res

    def __str__(self):
        return str(self.cells)


class SBGameField:
    def __init__(self):
        self.ships = list()
        self.hitten = set()

        self.xlength = self.ylength = 10

    def get_all_ship_cells(self):
        cells = []
        for ship in self.ships:
            for cell in ship.cells:
                cells.append((cell[0], cell[1]))
        return cells

    def __getitem__(self, key):
        key = digit(key)
        rowitems = [None,] + [EMPTY for cell in range(10)]
        for cell in self.hitten:
            if cell[0] == key:
                rowitems[cell[1]] = cell[2]
        for ship in self.ships:
            for cell in ship.cells:
                if cell[0] == key:
                    if not cell[2]:
                        rowitems[cell[1]] = SHIP
                    elif ship.isdead():
                        rowitems[cell[1]] = DEAD
                    else:
                        rowitems[cell[1]] = HIT
        return rowitems

    def field(self):
        return {key: self[key] for key in LETTERKEYS}

    def opfield(self):
        return {key: [(cell if cell != SHIP else EMPTY) for cell in self[key]] for key in LETTERKEYS}

    def __str__(self):
        field = self.field()
        header = '   |  ' + '  |  '.join(key for key in field) + '  |'
        border = '-' * len(header)
        content = '\n'.join(
            ['{:<2}'.format(str(i)) + ' |' + '|'.join(
             '{:^5}'.format(field[key][i]) for key in field.keys()) + '|\n' + border for i in range(1, 11)])
        return header + '\n' + border + '\n' + content

    def as_opposite(self):
        field = self.opfield()
        header = '   |  ' + '  |  '.join(key for key in field) + '  |'
        border = '-' * len(header)
        content = '\n'.join(
            ['{:<2}'.format(str(i)) + ' |' + '|'.join(
             '{:^5}'.format(field[key][i]) for key in field.keys()) + '|\n' + border for i in range(1, 11)])
        return header + '\n' + border + '\n' + content

    def can_ship(self, posx, posy):
        all_cells = self.get_all_ship_cells()
        banned_cells = []
        for cell in all_cells:
            banned_cells += area(cell[0], cell[1])
        return (posx, posy) not in banned_cells

    def put_ship(self, ship):
        crossing = False not in [self.can_ship(cell[0], cell[1]) for cell in ship.cells]
        if not crossing:
            raise ValueError('Здесь нельзя поставить корабль')
        self.ships.append(ship)

    def hit(self, posx, posy):
        success = False
        for ship in self.ships:
            for cell in ship.cells:
                if (cell[0], cell[1]) == (posx, posy):
                    cell[2] = True
                    self.hitten.add((posx, posy, HIT))
                    success = True
            if ship.isdead():
                for a in ship.around():
                    self.hitten.add((a[0], a[1], MISSED))
        if not success:
            self.hitten.add((posx, posy, MISSED))


# инициализация поля
GameField = SBGameField()

# инициализация кораблей
ships = []
for i in range(1, 5):
    for j in reversed(range(5-i)):
        ship = SBGameShip(length = i, field = GameField)
        ship.randompos()




print(GameField.as_opposite())
print(GameField)
