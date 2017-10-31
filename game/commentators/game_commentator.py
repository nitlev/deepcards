import sys


class GameCommentator:
    def __init__(self, verbosity=1):
        self.verbosity = verbosity

    @staticmethod
    def introduce_game(game, out=sys.stdout):
        for team in game.teams:
            out.write(
                "Team {}: {}, {}".format(team.id, team.player1, team.player2))
            out.write("\n")

    @staticmethod
    def comment_end_of_game(game, out=sys.stdout):
        best_team = None
        best_score = 0
        out.write("\n")
        for team in game.teams:
            night_points = team.game_night_points
            out.write(
                "Team {team_id}: {points} points.".format(team_id=team.id,
                                                          points=night_points))
            out.write("\n")
            if night_points > best_score:
                best_score = night_points
                best_team = team.id
        out.write("Team {team_id} wins!".format(team_id=best_team))
        out.write("\n")