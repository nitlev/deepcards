import sys

from cards import Card


class RoundCommentator:
    def __init__(self, verbosity=1, stream=None):
        self.verbosity = verbosity
        self.stream = stream or sys.stdout

    def comment_start_of_round(self, round):
        self.stream.write("\n")
        self.stream.write("Game {}".format(round.id))
        self.stream.write("\n")

    def comment_turn(self, round, trick):
        comments = []
        for i in range(4):
            player = round.players[(round.last_trick_winner + i) % 4]
            card = trick[i]
            comments.append(
                "{player} plays {card}".format(player=player, card=card))
        self.stream.write(", ".join(comments) + ".")
        self.stream.write("\n")

    def comment_end_of_turn(self, round):
        self.stream.write("{player} wins.".format(
            player=round.players[round.last_trick_winner]))
        self.stream.write("\n")

    def comment_end_of_round(self, round):
        best_team = None
        best_score = 0
        self.stream.write("\n")
        for team in round.teams:
            game_points = team.current_game_points
            self.stream.write(
                "Team {team_id}: {points} points.".format(team_id=team.id,
                                                          points=game_points))
            self.stream.write("\n")
            if game_points > best_score:
                best_score = game_points
                best_team = team.id
        self.stream.write("Team {team_id} wins!".format(team_id=best_team))
        self.stream.write("\n")

    def comment_distribution(self, round):
        self.stream.write("Trump suit will be {suit}.".format(
            suit=Card.suit_names[round.trump_suit]))
        self.stream.write("\n")