class Evaluator:
    trump_data = {"S": {"name": "Seven", "rank": 0, "points": 0},
                  "E": {"name": "Eight", "rank": 1, "points": 0},
                  "N": {"name": "Nine", "rank": 6, "points": 14},
                  "T": {"name": "Ten", "rank": 4, "points": 10},
                  "J": {"name": "Jack", "rank": 7, "points": 20},
                  "Q": {"name": "Queen", "rank": 2, "points": 3},
                  "K": {"name": "King", "rank": 3, "points": 4},
                  "A": {"name": "Ace", "rank": 5, "points": 11}}

    non_trump_data = {"S": {"name": "Seven", "rank": 0, "points": 0},
                      "E": {"name": "Eight", "rank": 1, "points": 0},
                      "N": {"name": "Nine", "rank": 2, "points": 0},
                      "T": {"name": "Ten", "rank": 6, "points": 10},
                      "J": {"name": "Jack", "rank": 3, "points": 2},
                      "Q": {"name": "Queen", "rank": 4, "points": 3},
                      "K": {"name": "King", "rank": 5, "points": 4},
                      "A": {"name": "Ace", "rank": 7, "points": 11}}

    def __init__(self, trump_suit=None):
        self.trump_suit = trump_suit

    def set_trump_suit(self, suit):
        self.trump_suit = suit


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

    def winner(self, trick, who_started=0):
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
            player.get_new_card(deck.next_card())

    @staticmethod
    def reveal_next_card(deck):
        revealed_card = deck.next_card()
        return revealed_card

    @staticmethod
    def give_card_to_player(card, player):
        player.get_new_card(card)

    def distribute_remaining_cards_to_players(self, deck, players):
        for player in players:
            if len(player.hand) == 5:
                self.give_three_cards(deck, player)
            else:
                self.give_two_cards(deck, player)