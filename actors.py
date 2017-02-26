import sys

from cards import Hand, Card, CardSet


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
            demanded_cards_in_hand = self.get_demanded_suit_cards_in_hand(demanded_suit)
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
        self.hand.add_card(card)

    def set_team_id(self, id):
        self.teamID = id

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Team:
    def __init__(self, team_id, player1, player2):
        self.id = team_id
        self.player1 = player1
        self.player2 = player2
        self.started = False
        self.won_last_turn = False
        self.set_team_id_to_members()
        self.won_cards = CardSet()
        self.current_game_points = 0
        self.game_night_points = 0

    def has_started(self, boolean):
        self.started = boolean

    def get_card(self, card):
        self.won_cards.add_card(card)

    def get_cards(self, cards):
        for card in cards:
            self.get_card(card)

    def set_team_id_to_members(self):
        self.player1.set_team_id(self.id)
        self.player2.set_team_id(self.id)

    def set_game_points(self, points):
        self.current_game_points = points
        self.game_night_points += points

    def throw_away_won_cards(self):
        self.won_cards = CardSet()

    def __str__(self):
        return "Team " + str(self.id) + ": " + str(self.player1) + " and " + str(self.player2)

    def __hash__(self):
        return hash(self.id)


class GameCommentator:
    def __init__(self, verbosity=1):
        self.verbosity = verbosity

    @staticmethod
    def comment_start_of_game(game, out=sys.stdout):
        out.write("\n")
        out.write("Game {}".format(game.id))
        out.write("\n")

    @staticmethod
    def comment_turn(game, trick, out=sys.stdout):
        comments = []
        for i in range(4):
            player = game.players[(game.last_trick_winner + i) % 4]
            card = trick[i]
            comments.append("{player} plays {card}".format(player=player, card=card))
        out.write(", ".join(comments) + ".")
        out.write("\n")

    @staticmethod
    def comment_start_of_turn(game, out=sys.stdout):
        out.write("{player} starts.".format(player=game.players[game.last_trick_winner]))
        out.write("\n")

    @staticmethod
    def comment_end_of_turn(game, out=sys.stdout):
        out.write("{player} wins.".format(player=game.players[game.last_trick_winner]))
        out.write("\n")

    @staticmethod
    def comment_end_of_game(game, out=sys.stdout):
        best_team = None
        best_score = 0
        out.write("\n")
        for team in game.teams:
            game_points = team.current_game_points
            out.write("Team {team_id}: {points} points.".format(team_id=team.id, points=game_points))
            out.write("\n")
            if game_points > best_score:
                best_score = game_points
                best_team = team.id
        out.write("Team {team_id} wins!".format(team_id=best_team))
        out.write("\n")

    @staticmethod
    def comment_distribution(game, out=sys.stdout):
        out.write("Trump suit will be {suit}.".format(suit=Card.suit_names[game.trump_suit]))
        out.write("\n")


class GameNightCommentator:
    def __init__(self, verbosity=1):
        self.verbosity = verbosity

    @staticmethod
    def introduce_game_night(game_night, out=sys.stdout):
        for team in game_night.teams:
            out.write("Team {}: {}, {}".format(team.id, team.player1, team.player2))
            out.write("\n")

    @staticmethod
    def comment_end_of_game_night(game_night, out=sys.stdout):
        best_team = None
        best_score = 0
        out.write("\n")
        for team in game_night.teams:
            night_points = team.game_night_points
            out.write("Team {team_id}: {points} points.".format(team_id=team.id, points=night_points))
            out.write("\n")
            if night_points > best_score:
                best_score = night_points
                best_team = team.id
        out.write("Team {team_id} wins!".format(team_id=best_team))
        out.write("\n")


