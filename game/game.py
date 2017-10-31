from cards import Deck
from officials import Evaluator, Referee, Distributor
from players import Team
from .commented_round import CommentedRound
from .round import Round


class Game:
    def __init__(self, team1: Team, team2: Team, evaluator: Evaluator,
                 distributor: Distributor, referee: Referee,
                 verbosity: int):
        self.teams = [team1, team2]
        self.which_player_starts = 0
        self.evaluator = evaluator
        self.distributor = distributor
        self.referee = referee
        self.number_of_games_played = 0
        self.verbosity = verbosity

    def play(self):
        while not self.is_finished():
            round = self.new_round()
            round.distribute_cards_and_choose_trump()
            round.play()
            round.count_points()
            round.close()
            self.number_of_games_played += 1

    def is_finished(self):
        return max([team.game_night_points for team in self.teams]) > 1000

    def new_round(self):
        deck = Deck()
        round = Round(self.number_of_games_played, self.teams[0],
                      self.teams[1], deck, self.evaluator,
                      self.distributor, self.referee,
                      self.number_of_games_played % 4)
        if self.verbosity == 0:
            return round
        else:
            return CommentedRound(round)
