import random
from .player import Player


class HumanPlayer(Player):
    """ This player is always prompted to manually select the next move.

    """

    def move(self):
        choice = ""
        print("  It's your move!!\n")
        while choice not in self.valid_moves:
            choice = input("  Rock, paper, scissors? > ").lower()
        print("")
        return choice


class CyclePlayer(Player):
    """ This player randomly selects it's first move.  It then cycles through
    the list of available moves (rock, paper, or scissors) in order and chooses
    the move that comes after the move that it selected last. If paper is the
    last move selected, for example, the current move will always be scissors.

    """

    def __init__(self):
        super().__init__()
        self.moves = []
        # Select the first move randomly.
        self.moves.append(random.choice(self.valid_moves))

    def move(self):
        count = 0
        for item in self.valid_moves:
            if item == self.moves[-1]:
                break
            count += 1
        return self.valid_moves[(count + 1) % 3]

    def learn(self, my_move, their_move):
        self.moves.append(my_move)


class ReflectPlayer(Player):
    """ This player randomly selects it's first move.  It then remembers
    it's opponents moves and always chooses it's opponents last move as
    it's next move.

    """

    def __init__(self):
        super().__init__()
        self.moves = []
        self.moves.append(random.choice(self.valid_moves))

    def move(self):
        # Select opponent's last move as current move
        return self.moves[-1]

    def learn(self, my_move, their_move):
        # Remember opponent's move
        self.moves.append(their_move)


class RandomPlayer(Player):
    """ This player always chooses a move randomly.

    """

    def move(self):
        return random.choice(self.valid_moves)
