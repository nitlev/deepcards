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


