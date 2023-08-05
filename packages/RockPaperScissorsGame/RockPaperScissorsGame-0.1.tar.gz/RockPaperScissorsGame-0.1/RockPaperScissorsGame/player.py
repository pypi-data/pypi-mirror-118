"""
!/usr/bin/env python3
-*- coding: utf-8 -*-
PROGRAMMER:   David Mixer
DATE CREATED: 14 June 2020
REVISED DATE: 09 Aug 2021
PURPOSE:

The Player class is the parent class for all of the Players in this
game and contains the attributes and methods common to all AI players.

"""


class Player:
    """ The Player class is the parent class for all of the Players in this
    game and contains the attributes and methods common to all AI players.

    Attributes:
        score - Contains the player's current game score

    """

    def __init__(self):
        self.score = 0
        self.valid_moves = ['rock', 'paper', 'scissors']

    def move(self):
        """ This unintelligent player always chooses 'rock'.

        """

        return 'rock'

    def learn(self, my_move, their_move):
        """ This unintelligent player does not have the ability to learn
        from opponent moves.

        """

        pass
