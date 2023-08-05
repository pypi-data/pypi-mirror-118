"""
!/usr/bin/env python3
-*- coding: utf-8 -*-
PROGRAMMER:   David Mixer
DATE CREATED: 14 June 2020
REVISED DATE: 09 Aug 2021
PURPOSE:

The game class defines the rules of the game and is responsible
for displaying the text based interface.

"""


from .utils import clear_screen


class Game:
    """ The game class defines the rules of the game and displays the
    text based interface to the user.

    Inputs:
        p1 - Player One should always be a HumanPlayer() object.
        p2 - Player Two can be any of the AI opponents (RandomPlayer,
             ReflectPlayer, or Cycle Player).

    """

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.valid_moves = ['rock', 'paper', 'scissors']

    def _play_single_round(self):
        clear_screen()
        self._play_round(1, 0, 0)

    def _play_match(self, maxpoints, winbypoints):
        self._play_round(1, maxpoints, winbypoints)

    def _display_ui_footer(self, round):
        if round < 10:
            print("  =================[ ROUND #0{} ]================="
                  "\n".format(round))
        else:
            print("  =================[ ROUND #{} ]================="
                  "\n".format(round))

    def _display_score(self):
        print("                -------------------")

        if self.p1.score < 10:
            print("                <  PLAYER_1:  0{}  >".format(self.p1.score))
        else:
            print("                <  PLAYER_1:  {}  >".format(self.p1.score))

        if self.p2.score < 10:
            print("                <  PLAYER_2:  0{}  >".format(self.p2.score))
        else:
            print("                <  PLAYER_2:  {}  >".format(self.p2.score))

        print("                -------------------\n")

    def _beats(self, one, two):
        # Return true if player one beats player two
        return ((one == 'rock' and two == 'scissors') or
                (one == 'scissors' and two == 'paper') or
                (one == 'paper' and two == 'rock'))

    def _get_round_result(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"    PLAYER_1: {move1}\n    PLAYER_2: {move2}\n")
        if self._beats(move1, move2):
            print("  PLAYER_1 WINS!!\n")
            self.p1.score += 1
        elif move1 == move2:
            print("  WE HAVE A TIE!!\n")
        else:
            print("  PLAYER_2 WINS!!\n")
            self.p2.score += 1
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def _play_round(self, round, maxpoints, winbypoints):
        self._display_ui_header()
        self._display_score()
        self._display_ui_footer(round)
        self._get_round_result()
        if not self._game_is_over(maxpoints, winbypoints):
            # We don't have a winner yet.
            # Play another round.
            clear_screen(2)
            self._play_round(round + 1, maxpoints, winbypoints)

    def _game_is_over(self, maxpoints, winbypoints):
        # First player to reach maxpoints points wins,
        # but you have to win by at least winbypoints!
        score1 = self.p1.score
        score2 = self.p2.score
        if score1 >= maxpoints and (
                score1 - score2) >= winbypoints:
            # Player 1 is the winner.
            return True
        elif score2 >= maxpoints and (
                score2 - score1) >= winbypoints:
            # Player 2 is the winner
            return True
        else:
            return False

    def _game_over(self):
        print("  **************** GAME OVER! ****************\n")
        print("   ", "=" * 15)
        print("      FINAL SCORE")
        print("   ", "=" * 15)
        print(f"\n     PLAYER_1:  {self.p1.score}")
        print(f"     PLAYER_2:  {self.p2.score}")
        if self.p1.score == self.p2.score:
            print(f"\n  WE HAVE A TIE!!!!")
        elif self.p1.score > self.p2.score:
            print(f"\n  PLAYER_1 IS THE WINNER!!!!")
        else:
            print(f"\n  PLAYER_2 IS THE WINNER!!!!")

    def _display_match_rules(self, maxpoints, winbypoints):
        print(" ", 15 * "-")
        print("   Match Rules")
        print(" ", 15 * "-", "\n")
        print("    The player with the most points wins.")
        print(f"    The game ends when a player has at least {maxpoints} "
              "points and")
        print(f"    is ahead of the opposing player by at least {winbypoints} "
              "points.\n")
        choice = input("  Hit <ENTER> to continue... ").lower()
        clear_screen(0)

    def _display_intro(self):
        clear_screen(0)
        self._display_ui_header()
        print("    Ready to play some Rock, Paper, Scissors?\n")

    def _display_ui_header(self):
        print("\n  ==========[ ROCK / PAPER / SCISSORS ]==========\n")

    def _choose_game_type(self):
        print("    Select the type of game you want to play:\n")
        print("      1. Play One Round")
        print("      2. Play A Match")
        choice = ""
        while choice not in ['1', '2']:
            choice = input("\n    Please select 1 or 2. > ").lower()
        print("")
        return choice

    def play_game(self):
        self._display_intro()
        if self._choose_game_type() == "1":
            self._play_single_round()
        else:
            maxpoints = 5
            winbypoints = 2
            self._display_match_rules(maxpoints, winbypoints)
            self._play_match(maxpoints, winbypoints)
        self._game_over()
