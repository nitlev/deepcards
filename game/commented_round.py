from game.commentators.round_commentator import RoundCommentator
from game.round import AbstractRound


class CommentedRound(AbstractRound):
    def __init__(self, round):
        self.round = round
        self.commentator = RoundCommentator()
        self.commentator.comment_start_of_round(self.round)

    def play(self):
        for turn in range(8):
            trick = self.play_one_turn()
            winning_team = self.evaluate_turn(trick)
            winning_team.get_cards(trick)
            if turn == 7:  # Last Turn
                winning_team.won_last_turn = True
        return 0

    def play_one_turn(self):
        trick = self.round.play_one_turn()
        self.commentator.comment_turn(self.round, trick)
        return trick

    def evaluate_turn(self, trick):
        winning_team = self.round.evaluate_turn(trick)
        self.commentator.comment_end_of_turn(self.round)
        return winning_team

    def count_points(self):
        self.round.count_points()
        self.commentator.comment_end_of_round(self.round)

    def distribute_cards_and_choose_trump(self):
        self.round.distribute_cards_and_choose_trump()
        self.commentator.comment_distribution(self.round)

    def get_other_team_by_id(self, team_id):
        self.round.get_other_team_by_id(team_id)

    def set_starting_team_from_player(self, player):
        self.round.set_starting_team_from_player(player)

    def perform_first_distribution_and_reveal_card(self):
        self.round.perform_first_distribution_and_reveal_card()

    def second_round_calls(self, revealed_card):
        self.round.second_round_calls(revealed_card)

    def get_team_by_id(self, team_id):
        self.round.get_team_by_id(team_id)

    def set_trump_suit(self, suit):
        self.round.set_trump_suit(suit)

    def who_plays_now(self, i):
        self.round.who_plays_now(i)

    def close(self):
        self.round.close()

    def first_round_calls(self, revealed_card):
        self.round.first_round_calls(revealed_card)