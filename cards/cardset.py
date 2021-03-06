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

    def to_ranked(self, suit):
        new_cardset = self.__class__()
        for card in self.cards:
            new_cardset.add_card(card.to_ranked(suit))
        return new_cardset

    @property
    def total_points(self):
        return sum([card.points for card in self.cards])

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
    """
    Four or less distinct cards.

    If cards are ranked, this class is also able to find the winning card of
    the trick.
    """

    def __init__(self, cards=None):
        CardSet.__init__(self, cards, 4)

    @property
    def winner(self):
        first_card = self.cards[0]
        demanded_suit = first_card.suit
        winner_card = first_card
        for i, card in enumerate(self.cards[1:]):
            if (card.is_trump or card.suit == demanded_suit) and \
                    card.is_higher_than(winner_card):
                winner_card = card
        return winner_card
