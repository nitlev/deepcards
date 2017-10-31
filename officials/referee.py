class Referee:
    @staticmethod
    def count_team_points(team):
        bonus = 10 if team.won_last_turn else 0
        points = team.won_cards.total_points + bonus
        if team.started:
            return points if points >= 82 else 0
        else:
            return points if points <= 80 else 162

    def winning_team(self, game):
        which_team_started = game.which_team_started
        if self.count_team_points(which_team_started) >= 82:
            return which_team_started
        else:
            return game.which_team_didnt_start