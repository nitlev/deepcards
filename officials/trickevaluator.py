from cards import Trick
from officials import Evaluator


class TrickEvaluator(Evaluator):
    def __init__(self, trump_suit=None):
        Evaluator.__init__(self, trump_suit)

    def get_rank(self, card):
        if card.suit == self.trump_suit:
            return self.get_trump_rank(card.value)
        else:
            return self.get_non_trump_rank(card.value)

    def get_trump_rank(self, value):
        return self.trump_data.get(value).get("rank")

    def get_non_trump_rank(self, value):
        return self.non_trump_data.get(value).get("rank")

    def winner(self, trick: Trick, who_started=0):
        first_card = trick[0]
        demanded_suit = first_card.suit
        trick_winner_index = 0
        winner_card = first_card
        for i, card in enumerate(trick[1:]):
            if card.suit in [self.trump_suit, demanded_suit] and self.is_higher(card, winner_card):
                trick_winner_index = i + 1
                winner_card = card
        who_win = (who_started + trick_winner_index) % 4
        return who_win

    def is_higher(self, card1, card2):
        """Returns True if card1 > card2, else False.
        card1 suit is supposed to be either from demanded suit or trump suit"""
        win_by_trump = card1.suit == self.trump_suit and card2.suit != self.trump_suit
        win_by_value = card1.suit == card2.suit and self.get_rank(card1) > self.get_rank(card2)
        if win_by_trump:
            return True
        elif win_by_value:
            return True
        else:
            return False