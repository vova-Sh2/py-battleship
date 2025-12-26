class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.get_deck(start, end)

    def get_deck(self, start: tuple, end: tuple) -> list:
        row1, column1 = start
        row2, column2 = end
        deck = []
        if row1 == row2:
            step = 1 if column2 >= column1 else -1
            for column in range(column1, column2 + step, step):
                deck.append(Deck(row1, column))
        elif column1 == column2:
            step = 1 if row2 >= row1 else -1
            for row in range(row1, row2 + step, step):
                deck.append(Deck(row, column1))
        else :
            raise ValueError("Ship must be vertical or horizontal")
        return deck

    def fire(self, row: int, column: int) -> None:
        for i in self.decks:
            if i.row == row and i.column == column:
                if i.is_alive:
                    i.is_alive = False
        for i in self.decks:
            if i.is_alive:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.WATER = "~"
        self.HIT = "*"
        self.MISS = "0"
        self.SUNK = "x"
        self.SHIP = u"\u25A1"
        self.field = {}
        self.arena = [[self.WATER] * 10 for _ in range(10)]
        for start, end in ships:
            shi = Ship(start, end)
            for i in shi.decks:
                self.field[(i.row, i.column)] = shi
        for row, column in self.field:
            self.arena[row][column] = self.SHIP

    def fire(self, location: tuple) -> str:
        row, column = location
        if location in self.field:
            self.field[location].fire(row, column)
            if self.field[location].is_drowned:
                self.print_field()
                return "Sunk!"
            self.arena[row][column] = self.HIT
            self.print_field()
            return "Hit!"
        self.arena[row][column] = self.MISS
        self.print_field()
        return "Miss!"

    def print_field(self) -> None:
        for dec in self.field:
            row, column = dec
            if self.field[dec].is_drowned:
                self.arena[row][column] = self.SUNK

        for row in range(10):
            print("  ".join(self.arena[row]))
