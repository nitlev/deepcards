from cards import Hand


class Player:
    def __init__(self, name="", starting_strategy=None, playing_strategy=None):
        self.name = name
        self.hand = Hand()
        self.starting_strategy = starting_strategy
        self.playing_strategy = playing_strategy
        self.teamID = None

    def play(self, trick, trump_suit):
        card = self.choose_card(trick, trump_suit)
        self.play_card(card, trick)

    def choose_card(self, trick, trump_suit):
        if len(trick) == 0:
            return self.choose_card_from(self.hand)
        else:
            demanded_suit = trick[0].suit
            demanded_cards_in_hand = self.get_demanded_suit_cards_in_hand(
                demanded_suit)
            trump_cards_in_hand = self.get_trump_cards_in_hand(trump_suit)
            if len(demanded_cards_in_hand) > 0:
                return self.choose_card_from(demanded_cards_in_hand)
            elif len(trump_cards_in_hand) > 0:
                return self.choose_card_from(trump_cards_in_hand)
            else:
                return self.choose_card_from(self.hand)

    @staticmethod
    def choose_card_from(cards):
        return cards[0]

    def get_trump_cards_in_hand(self, trump_suit):
        return self._get_cards_in_hand_with_suit(trump_suit)

    def get_demanded_suit_cards_in_hand(self, demanded_suit):
        return self._get_cards_in_hand_with_suit(demanded_suit)

    def _get_cards_in_hand_with_suit(self, suit):
        return [card for card in self.hand if card.suit == suit]

    def play_card(self, card, trick):
        self.take_card(card)
        self.add_card_to_trick(card, trick)

    def take_card(self, card):
        self.hand.remove(card)

    @staticmethod
    def add_card_to_trick(card, trick):
        trick.add_card(card)

    def chooses_to_start(self, card):
        return True

    def add_card_to_hand(self, card):
        self.hand.add_card(card.with_owner(self))

    def set_team_id(self, id):
        self.teamID = id

    def set_trump_suit(self, suit):
        self.hand = self.hand.to_ranked(suit)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)