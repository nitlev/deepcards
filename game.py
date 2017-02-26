from actors import GameCommentator, GameNightCommentator, Team
from cards import Deck, Trick


class Game:
    """A game of belote"""

    def __init__(self, game_id, team1: Team, team2: Team, deck, evaluator,
                 distributor, referee, who_starts=0, seed=None):
        self.id = game_id
        self.teams = {team1, team2}
        players = [team1.player1, team2.player1, team1.player2, team2.player2]
        self.players = [players[(who_starts + i) % 4] for i in range(4)]
        self.deck = deck
        self.evaluator = evaluator
        self.distributor = distributor
        self.referee = referee
        self.trump_suit = None
        self.played = True
        self.last_trick_winner = 0
        self.seed = seed

    def play(self):
        for turn in range(8):
            trick = self.play_one_turn()
            winning_team = self.evaluate_turn(trick)
            winning_team.get_cards(trick)
            if turn == 7:  # Last Turn
                winning_team.won_last_turn = True
        return 0

    def play_one_turn(self):
        trick = Trick()
        for i in range(4):
            player = self.who_plays_now(i)
            player.play(trick, self.trump_suit)
        return trick

    def who_plays_now(self, i):
        return self.players[(self.last_trick_winner + i) % 4]

    def distribute_cards_and_choose_trump(self):
        revealed_card = self.perform_first_distribution_and_reveal_card()
        no_one_started = self.first_round_calls(revealed_card)
        if no_one_started:
            no_one_started = self.second_round_calls(revealed_card)
        if no_one_started:
            print("Game not played")
            self.played = False
        else:
            self.distributor.distribute_remaining_cards_to_players(self.deck,
                                                                   self.players)

    def perform_first_distribution_and_reveal_card(self):
        self.distributor.shuffle(self.deck, self.seed)
        self.distributor.distribute_five_cards_to_players(self.deck,
                                                          self.players)
        revealed_card = self.distributor.reveal_next_card(self.deck)
        return revealed_card

    def first_round_calls(self, revealed_card):
        no_one_started = True
        for player in self.players:
            if player.chooses_to_start(revealed_card):
                self.set_starting_team_from_player(player)
                self.set_trump_suit(revealed_card.suit)
                self.distributor.give_card_to_player(revealed_card, player)
                no_one_started = False
                break
        return no_one_started

    def second_round_calls(self, revealed_card):
        no_one_started = True
        for player in self.players:
            trump_suit = player.announce_trump_or_pass()
            if trump_suit is not None:
                self.set_starting_team_from_player(player)
                self.set_trump_suit(trump_suit)
                self.distributor.give_card_to_player(revealed_card, player)
                no_one_started = False
                break
        return no_one_started

    def set_starting_team_from_player(self, player):
        starting_team = self.get_team_by_id(player.teamID)
        starting_team.has_started(True)

        non_starting_team = self.get_other_team_by_id(player.teamID)
        non_starting_team.has_started(False)

    def set_trump_suit(self, suit):
        self.trump_suit = suit
        self.evaluator.set_trump_suit(suit)
        self.referee.set_trump_suit(suit)

    def get_team_by_id(self, team_id):
        return [team for team in self.teams if team.id == team_id][0]

    def get_other_team_by_id(self, team_id):
        """Returns the team which id is NOT team_id"""
        return [team for team in self.teams if team.id != team_id][0]

    def evaluate_turn(self, trick):
        winner = self.evaluator.winner(trick,
                                       who_started=self.last_trick_winner)
        self.last_trick_winner = winner
        winning_player = self.players[winner]
        winning_team = self.get_team_by_id(winning_player.teamID)
        return winning_team

    def count_points(self):
        for team in self.teams:
            points = self.referee.count_team_points(team)
            team.set_game_points(points)

    def close(self):
        for team in self.teams:
            team.throw_away_won_cards()


class CommentedGame(object):
    def __init__(self, game):
        self.game = game
        self.commentator = GameCommentator()
        self.commentator.comment_start_of_game(self.game)

    def distribute_cards_and_choose_trump(self):
        self.game.distribute_cards_and_choose_trump()
        self.commentator.comment_distribution(self)

    def play_one_turn(self):
        self.commentator.comment_start_of_turn(self)
        trick = self.game.play_one_turn()
        self.commentator.comment_turn(self, trick)
        return trick

    def evaluate_turn(self, trick):
        winning_team = self.game.evaluate_turn(trick)
        self.commentator.comment_end_of_turn(self)
        return winning_team

    def count_points(self):
        self.game.count_points()
        self.commentator.comment_end_of_game(self)


class GameNight:
    def __init__(self, team1, team2, evaluator, distributor, referee):
        self.teams = [team1, team2]
        self.which_player_starts = 0
        self.evaluator = evaluator
        self.distributor = distributor
        self.referee = referee
        self.number_of_games_played = 0
        self.game_type = Game

    def play(self):
        while max([team.game_night_points for team in self.teams]) < 1000:
            deck = Deck()
            game = self.game_type(self.number_of_games_played, self.teams[0],
                                  self.teams[1], deck, self.evaluator,
                                  self.distributor, self.referee,
                                  self.number_of_games_played % 4)
            game.distribute_cards_and_choose_trump()
            game.play()
            game.count_points()
            game.close()
            self.number_of_games_played += 1


class CommentedGameNight(object):
    def __init__(self, game):
        self.game = game
        self.game_type = CommentedGame
        self.commentator = GameNightCommentator()

    def start(self):
        self.commentator.introduce_game_night(self.game)

    def play(self):
        self.game.play()
        self.commentator.comment_end_of_game_night(self.game)
