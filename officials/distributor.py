class Distributor:
    def __init__(self):
        pass

    @staticmethod
    def shuffle(deck, seed=None):
        deck.shuffle(seed)

    def distribute_five_cards_to_players(self, deck, players):
        for player in players:
            self.give_two_cards(deck, player)
        for player in players:
            self.give_three_cards(deck, player)

    def give_two_cards(self, deck, player):
        self.give_n_cards(deck, player, 2)

    def give_three_cards(self, deck, player):
        self.give_n_cards(deck, player, 3)

    @staticmethod
    def give_n_cards(deck, player, n):
        for i in range(n):
            player.add_card_to_hand(deck.next_card())

    @staticmethod
    def reveal_next_card(deck):
        revealed_card = deck.next_card()
        return revealed_card

    @staticmethod
    def give_card_to_player(card, player):
        player.add_card_to_hand(card)

    def distribute_remaining_cards_to_players(self, deck, players):
        for player in players:
            if len(player.hand) == 5:
                self.give_three_cards(deck, player)
            else:
                self.give_two_cards(deck, player)