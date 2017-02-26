import random


class Card(object):
    """
    Represents a standard playing card.

    Attributes:
      suit: integer 0-3
      value: integer 0-7
    """

    suit_names = {"C": "Clubs", "D": "Diamonds", "H": "Hearts", "S": "Spades"}
    value_names = {"S": "7", "E": "8", "N": "9", "T": "10",
                   "J": "Jack", "Q": "Queen", "K": "King", "A": "Ace"}

    def __init__(self, suit, value):
        if not self.is_valid_card(suit, value):
            raise ValueError("Invalid card definition, "
                             "rank or suit is out of bound")
        self.suit = suit
        self.value = value

    def is_valid_card(self, suit, rank):
        return self.is_valid_value(rank) and self.is_valid_suit(suit)

    def is_valid_value(self, value):
        return value in self.value_names.keys()

    def is_valid_suit(self, suit):
        return suit in self.suit_names.keys()

    def __str__(self):
        """Returns a human-readable string representation."""
        return '%s of %s' % (Card.value_names[self.value],
                             Card.suit_names[self.suit])

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __hash__(self):
        return hash((self.value, self.suit))


class CardSet:
    def __init__(self, cards=None, max_cards=32):
        self.max_number_of_cards = max_cards
        cards = list() if cards is None else cards
        if not self.is_valid_stack(cards):
            raise ValueError("Hands contains too many cards or duplicates")
        self.cards = cards

    def is_valid_stack(self, cards):
        return len(cards) <= self.max_number_of_cards and len(cards) == len(set(cards))

    def add_card(self, card):
        if not self.is_valid_stack(self.cards + [card]):
            raise ValueError("{} is not valid".format(self.__class__.__name__))
        self.cards.append(card)

    def pop(self, index):
        return self.cards.pop(index)

    def remove(self, card):
        self.cards.remove(card)

    def __getitem__(self, item):
        return self.cards[item]

    def __eq__(self, other):
        return all([card1 == card2 for card1, card2 in zip(self.cards, other.cards)])

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, ", ".join([str(card) for card in self.cards]))

    def __repr__(self):
        return str(self)


class Hand(CardSet):
    """Eight or less distinct cards"""

    def __init__(self, cards=None):
        CardSet.__init__(self, cards, 8)


class Trick(CardSet):
    """Four or less distinct cards"""

    def __init__(self, cards=None):
        CardSet.__init__(self, cards, 4)


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
