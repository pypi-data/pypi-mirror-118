


import random

class battleship:
    def __init__(self, shipsize):
        self.shipsize = shipsize
        self.column = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.row = ["a", "b", "c", "d"]
        self.column_length = len(self.column)
        self.row_length = len(self.row)

    def shipplace(self, row_choose, position):
        new_position = []
        for pos in position:
            x = row_choose + str(pos)
            new_position.append(x)
        return new_position

    def putship(self):
        column_choose = random.choice(self.column)
        row_choose = random.choice(self.row)
        position = []
        if column_choose + self.shipsize < self.column_length:
            position = range(column_choose, column_choose + self.shipsize, 1)
        else:
            position = range(column_choose, column_choose - self.shipsize, -1)
        self.place = self.shipplace(row_choose, position)
    
    def guessship(self):
        turns = 10
        hit = 0
        while turns > 0:
            print("the ship can be located anywhere from rows - a, b, c, d and columns - 1,2,3,4,5,6,7,8,9")
            guess = input("type place: ")
            if guess in self.place:
                print("ITS A HIT!!")
                hit -= 1
                print("come on  you should only hit the ship " + hit + " times!")
                if hit == 0:
                    print("You sunk the ship")
            else:
                print("ITS A MISS")
            turns -= 1


if __name__ == '__main__':
    game1 = battleship(3)
    game1.putship()
    game1.guessship()

