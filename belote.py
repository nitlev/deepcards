from actors import Player, Team
from game import GameNight, CommentedGameNight
from officials import TrickEvaluator, Referee, Distributor


def main():
    team0, team1 = Team(0, Player("Alex"), Player("Thibaud")), \
                   Team(1, Player("Marie"), Player("Veltin"))
    distributor = Distributor()
    trick_evaluator = TrickEvaluator()
    referee = Referee()
    game_night = GameNight(team0, team1, trick_evaluator,
                           distributor, referee, verbosity=1)
    commented_game_night = CommentedGameNight(game_night)
    commented_game_night.start()
    commented_game_night.play()
    print("Game finished")


if __name__ == '__main__':
    main()
