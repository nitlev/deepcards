from .card import Card


class RankedCard(Card):
    def __init__(self, card: Card):
        Card.__init__(self, card.suit, card.value, card.owner)
        self.card = card
    
    def is_higher_than(self, card2):
        """Returns True if self > card2, else False.
        card1 suit is supposed to be either from demanded suit or trump suit"""
        win_by_trump = self.is_trump and not card2.is_trump
        win_by_value = self.suit == card2.suit and self.rank > card2.rank
        if win_by_trump:
            return True
        elif win_by_value:
            return True
        else:
            return False

    @property
    def is_trump(self):
        return NotImplementedError

    @property
    def rank(self):
        return NotImplementedError


class Trump(RankedCard):
    trump_data = {"S": {"name": "Seven", "rank": 0, "points": 0},
                  "E": {"name": "Eight", "rank": 1, "points": 0},
                  "N": {"name": "Nine", "rank": 6, "points": 14},
                  "T": {"name": "Ten", "rank": 4, "points": 10},
                  "J": {"name": "Jack", "rank": 7, "points": 20},
                  "Q": {"name": "Queen", "rank": 2, "points": 3},
                  "K": {"name": "King", "rank": 3, "points": 4},
                  "A": {"name": "Ace", "rank": 5, "points": 11}}

    def __init__(self, card: Card):
        RankedCard.__init__(self, card)
        self.card = card

    @property
    def points(self):
        value = self.card.value
        return self.trump_data.get(value).get("points")

    @property
    def rank(self):
        value = self.card.value
        return self.trump_data.get(value).get("rank")

    @property
    def is_trump(self):
        return True


class NonTrump(RankedCard):
    non_trump_data = {"S": {"name": "Seven", "rank": 0, "points": 0},
                      "E": {"name": "Eight", "rank": 1, "points": 0},
                      "N": {"name": "Nine", "rank": 2, "points": 0},
                      "T": {"name": "Ten", "rank": 6, "points": 10},
                      "J": {"name": "Jack", "rank": 3, "points": 2},
                      "Q": {"name": "Queen", "rank": 4, "points": 3},
                      "K": {"name": "King", "rank": 5, "points": 4},
                      "A": {"name": "Ace", "rank": 7, "points": 11}}

    def __init__(self, card: Card):
        RankedCard.__init__(self, card)
        self.card = card

    @property
    def points(self):
        value = self.card.value
        return self.non_trump_data.get(value).get("points")

    @property
    def rank(self):
        value = self.card.value
        return self.non_trump_data.get(value).get("rank")

    @property
    def is_trump(self):
        return False
