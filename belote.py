from players.team import Team
from players.players import Player
from game import CommentedGame
from game.game import Game
from officials import TrickEvaluator, Referee
from officials.distributor import Distributor


def main():
    team0, team1 = Team(0, Player("Alex"), Player("Thibaud")), \
                   Team(1, Player("Marie"), Player("Veltin"))
    distributor = Distributor()
    trick_evaluator = TrickEvaluator()
    referee = Referee()
    game = Game(team0, team1, trick_evaluator,
                distributor, referee, verbosity=1)
    commented_game = CommentedGame(game)
    commented_game.start()
    commented_game.play()
    print("Game finished")


if __name__ == '__main__':
    main()
