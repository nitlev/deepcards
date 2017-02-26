from actors import Player, Team
from officials import TrickEvaluator, Referee, Distributor
from game import CommentedGameNight


def main():
    team0, team1 = Team(0, Player("Alex"), Player("Thibaud")), \
                   Team(1, Player("Marie"), Player("Veltin"))
    distributor = Distributor()
    trick_evaluator = TrickEvaluator()
    referee = Referee()
    game_night = CommentedGameNight(team0, team1, trick_evaluator,
                                    distributor, referee)
    game_night.start()
    game_night.play()
    print("Game finished")


if __name__ == '__main__':
    main()
