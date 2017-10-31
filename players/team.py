from cards import CardSet


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
        return "Team " + str(self.id) + ": " + str(
            self.player1) + " and " + str(self.player2)

    def __hash__(self):
        return hash(self.id)