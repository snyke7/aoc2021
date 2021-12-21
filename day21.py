import attr
from typing import Callable, Tuple
from copy import copy


@attr.s(auto_attribs=True)
class PlayerState:
    score: int = 0
    location: int = 1

    def advance(self, steps: int, win_cond: int) -> bool:
        self.location = (self.location + steps - 1) % 10 + 1
        self.score += self.location
        return self.score >= win_cond

    def deadvance(self, steps: int) -> None:
        self.score -= self.location
        self.location = (self.location - steps - 1) % 10 + 1

    def __copy__(self):
        return PlayerState(self.score, self.location)


@attr.s(auto_attribs=True)
class Die:
    die_strat: Callable[[], int]
    num_rolls: int = 0

    def do_roll(self) -> int:
        result = self.die_strat()
        self.num_rolls += 1
        return result


@attr.s(auto_attribs=True)
class GameState:
    die: Die
    player1: PlayerState = PlayerState()
    player2: PlayerState = PlayerState()
    is_player1_turn: bool = True

    def do_turn(self) -> bool:
        total_adv = self.die.do_roll() + self.die.do_roll() + self.die.do_roll()
        the_player = self.player1 if self.is_player1_turn else self.player2
        result = the_player.advance(total_adv, 1000)
        self.is_player1_turn = not self.is_player1_turn
        return result

    def run_game(self) -> None:
        while not self.do_turn():
            pass


@attr.s(auto_attribs=True)
class DeterministicDieStrat:
    prev_roll: int = 100

    def roll_dice(self):
        self.prev_roll = self.prev_roll % 100 + 1
        return self.prev_roll


QDICE_DISTR = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}


@attr.s(auto_attribs=True)
class QuantumGameStates:
    player1: PlayerState = PlayerState()
    player2: PlayerState = PlayerState()
    is_player1_turn: bool = True

    def calc_winning_universes(self) -> Tuple[int, int]:
        player1_win, player2_win = 0, 0
        for die_total, num_universes in QDICE_DISTR.items():
            win = (self.player1 if self.is_player1_turn else self.player2).advance(die_total, 21)
            if win:
                if self.is_player1_turn:
                    player1_win += num_universes
                else:
                    player2_win += num_universes
            else:
                self.is_player1_turn = not self.is_player1_turn
                num_wins1, num_wins2 = self.calc_winning_universes()
                player1_win += num_wins1 * num_universes
                player2_win += num_wins2 * num_universes
                self.is_player1_turn = not self.is_player1_turn
            (self.player1 if self.is_player1_turn else self.player2).deadvance(die_total)
        return player1_win, player2_win


def get_solution():
    start_locs = [6, 10]

    game = GameState(Die(DeterministicDieStrat().roll_dice))
    game.player1.location = start_locs[0]
    game.player2.location = start_locs[1]
    game.run_game()
    loser_score = min(game.player1.score, game.player2.score)
    die_rolls = game.die.num_rolls
    print(loser_score * die_rolls)

    qgame = QuantumGameStates()
    qgame.player1.location = start_locs[0]
    qgame.player2.location = start_locs[1]
    result = qgame.calc_winning_universes()
    # takes slightly over a minute. could maybe be improved by only considering monotone die rolls, ie not considering
    # 9, 3 but considering 3, 9 twice
    print(result)
    print(max(result))


# 3: one       111
# 4: three     112, 121, 211
# 5: six       113, 131, 311, 122, 212, 221
# 6: ten       123, 132, 213, 231, 312, 321, 222
# 7: six       223, 232, 322, 331, 313, 133
# 8: three     233, 323, 332
# 9: one       333
