from officials import Evaluator


class Referee(Evaluator):
    def __init__(self, trump_suit=None):
        Evaluator.__init__(self, trump_suit)

    def card_points(self, card):
        if card.suit == self.trump_suit:
            return self.trump_data[card.value]["points"]
        else:
            return self.non_trump_data[card.value]["points"]

    def cards_points(self, cards):
        return sum([self.card_points(card) for card in cards])

    def count_team_absolute_points(self, team):
        return self.cards_points(team.won_cards)

    def count_team_points(self, team):
        bonus = 10 if team.won_last_turn else 0
        points = self.count_team_absolute_points(team) + bonus
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