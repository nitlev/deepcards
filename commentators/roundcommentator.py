import sys

from cards import Card


class RoundCommentator:
    def __init__(self, verbosity=1):
        self.verbosity = verbosity

    @staticmethod
    def comment_start_of_game(game, out=sys.stdout):
        out.write("\n")
        out.write("Game {}".format(game.id))
        out.write("\n")

    @staticmethod
    def comment_turn(game, trick, out=sys.stdout):
        comments = []
        for i in range(4):
            player = game.players[(game.last_trick_winner + i) % 4]
            card = trick[i]
            comments.append(
                "{player} plays {card}".format(player=player, card=card))
        out.write(", ".join(comments) + ".")
        out.write("\n")

    @staticmethod
    def comment_start_of_turn(game, out=sys.stdout):
        out.write("{player} starts.".format(
            player=game.players[game.last_trick_winner]))
        out.write("\n")

    @staticmethod
    def comment_end_of_turn(game, out=sys.stdout):
        out.write("{player} wins.".format(
            player=game.players[game.last_trick_winner]))
        out.write("\n")

    @staticmethod
    def comment_end_of_game(game, out=sys.stdout):
        best_team = None
        best_score = 0
        out.write("\n")
        for team in game.teams:
            game_points = team.current_game_points
            out.write(
                "Team {team_id}: {points} points.".format(team_id=team.id,
                                                          points=game_points))
            out.write("\n")
            if game_points > best_score:
                best_score = game_points
                best_team = team.id
        out.write("Team {team_id} wins!".format(team_id=best_team))
        out.write("\n")

    @staticmethod
    def comment_distribution(game, out=sys.stdout):
        out.write("Trump suit will be {suit}.".format(
            suit=Card.suit_names[game.trump_suit]))
        out.write("\n")