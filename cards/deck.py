import random

from cards.card import Card
from cards.cardset import CardSet


class CardStack(CardSet):
    """A set that removes cards when being iterated on"""

    def __init__(self, cards=None, max_cards=32):
        CardSet.__init__(self, cards, max_cards)

    def __next__(self):
        if len(self) == 0:
            raise StopIteration
        next_card = self.cards.pop(0)
        return next_card

    def __iter__(self):
        return self


class Deck(CardStack):
    """32 or less distinct cards"""

    def __init__(self):
        CardStack.__init__(self)
        self.cards = [Card(i, j) for i in Card.suit_names
                      for j in Card.value_names]

    def shuffle(self, seed=None):
        random.seed(seed)
        random.shuffle(self.cards)

    def has_next(self):
        return len(self.cards) > 0

    def next_card(self):
        return next(self)