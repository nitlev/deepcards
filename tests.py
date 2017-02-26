import re
from io import StringIO

import pytest

from actors import Player, Team, GameCommentator, GameNightCommentator
from cards import Card, CardStack, Deck, Hand, Trick
from game import Game, GameNight
from officials import TrickEvaluator, Referee, Distributor


def regex_builder(cardstackname):
    reg = re.compile(cardstackname + "([\w,]*)")
    return reg


class TestCards:
    def test_card_should_initialize_correctly(self):
        card = Card("S", "A")
        assert card.suit == "S"
        assert card.value == "A"

    def test_card_initialization_should_fail_when_rank_is_unvalid(self):
        with pytest.raises(ValueError):
            Card(0, 42)

    def test_card_initialization_should_fail_when_suit_is_unvalid(self):
        with pytest.raises(ValueError):
            Card(8, 2)

    def test_to_string_function(self):
        assert str(Card("C", "A")) == "Ace of Clubs"
        assert str(Card("D", "K")) == "King of Diamonds"
        assert str(Card("H", "Q")) == "Queen of Hearts"
        assert str(Card("S", "J")) == "Jack of Spades"

    def test_repr_function(self):
        assert repr(Card("C", "A")) == "Ace of Clubs"
        assert repr(Card("D", "K")) == "King of Diamonds"
        assert repr(Card("H", "Q")) == "Queen of Hearts"
        assert repr(Card("S", "J")) == "Jack of Spades"


class TestCardStack:
    def test_pop_should_remove_one_card(self):
        stack = CardStack()
        stack.add_card(Card("C", "A"))
        stack.add_card(Card("D", "A"))
        l = len(stack.cards)
        for _ in range(2):
            card = stack.pop(0)
            assert isinstance(card, Card)
            assert len(stack.cards) == l - 1
            l -= 1

    def test_prints_correctly(self):
        stack = CardStack()
        stack.add_card(Card("C", "A"))
        regex = regex_builder("CardStack")
        assert regex.match(str(stack))

    def test_repr_correctly(self):
        stack = CardStack()
        stack.add_card(Card("C", "A"))
        regex = regex_builder("CardStack")
        assert regex.match(repr(stack))


class TestDeck:
    def test_deck_initialize_with_all_cards(self):
        deck = Deck()
        assert len(deck) == 32
        assert len(set(deck.cards)) == 32

    def test_shuffle_should_still_be_a_valid_deck(self):
        deck = Deck()
        deck.shuffle()
        assert len(deck) == 32
        assert len(set(deck.cards)) == 32

    def test_prints_correctly(self):
        deck = Deck()
        regex = regex_builder("Deck")
        assert regex.match(str(deck))

    def test_has_next_should_return_false_iff_deck_is_empty(self):
        deck = Deck()
        for _ in range(32):
            assert deck.has_next()
            _ = deck.next_card()
        assert deck.has_next() == False

    def test_two_decks_should_be_same_after_shuffle_given_same_seed(self):
        deck1 = Deck()
        deck2 = Deck()
        deck1.shuffle(seed=42)
        deck2.shuffle(seed=42)
        assert deck1 == deck2

    def test_two_decks_should_be_different_after_shuffle_given_different_seed(self):
        deck1 = Deck()
        deck2 = Deck()
        deck1.shuffle(seed=42)
        deck2.shuffle(seed=42*42)
        assert deck1 != deck2


class TestHand:
    def test_hand_should_initializes_empty(self):
        hand = Hand()
        assert len(hand) == 0

    def test_hand_with_duplicates_is_rejected(self):
        with pytest.raises(ValueError):
            Hand([Card("C", "E"), Card("C", "E")])

    def test_hand_with_too_many_cards_is_rejected(self):
        with pytest.raises(ValueError):
            too_many_cards = [Card(0, i) for i in range(8)] + [Card("D", "S")]
            Hand(too_many_cards)

    def test_add_valid_card_should_result_in_new_hand(self):
        hand = Hand([Card("C", "E")])
        hand.add_card(Card("C", "T"))
        assert hand.cards == Hand([Card("C", "E"), Card("C", "T")]).cards

    def test_add_duplicate_card_should_raise_valueerror(self):
        hand = Hand([Card("C", "E")])
        with pytest.raises(ValueError):
            hand.add_card(Card("C", "E"))

    def test_add_too_many_cards_should_raise_valueerror(self):
        hand = Hand([Card("C", value) for value in Card.value_names])
        with pytest.raises(ValueError):
            hand.add_card(Card("D", "S"))

    def test_prints_correctly(self):
        hand = Hand()
        hand.add_card(Card("C", "A"))
        hand.add_card(Card("D", "A"))
        regex = regex_builder("Hand")
        assert regex.match(str(hand))


class TestPlayer:
    def test_player_should_introduce_himself_politely(self):
        player = Player("John Doe")
        assert str(player) == "John Doe"
        assert repr(player) == "John Doe"

    def test_player_should_initialize_with_no_hand(self):
        player = Player()
        assert len(player.hand) == 0

    def test_player_should_use_starting_strategy(self):
        deck = Deck()
        player = Player(starting_strategy=lambda: True)
        # with this strategy, the player choose always start
        # no matter the card he's being offered
        for card in deck:
            assert player.chooses_to_start(card)

    def test_player_should_return_card_in_hand_when_chooses_card(self):
        player = Player()
        card = Card("C", "S")
        player.add_card_to_hand(card)
        chosen_card = player.choose_card(Trick(), 0)
        assert chosen_card in player.hand

    def test_get_trump_card_should_return_trump_only(self):
        player = Player()
        cards = [Card("C", "S"), Card("D", "S"), Card("H", "S"), Card("S", "S"), Card("C", "E"), Card("D", "T"),
                 Card("H", "J"), Card("S", "Q")]
        for card in cards:
            player.add_card_to_hand(card)
        for suit in range(4):
            for card in player.get_trump_cards_in_hand(suit):
                assert card.suit == suit

    def test_get_demanded_suit_card_in_hand_should_return_demanded_suit_cards_only(self):
        player = Player()
        cards = [Card("C", "S"), Card("D", "S"), Card("H", "S"), Card("S", "S"), Card("C", "E"), Card("D", "T"),
                 Card("H", "J"), Card("S", "Q")]
        for card in cards:
            player.add_card_to_hand(card)
        for suit in range(4):
            for card in player.get_demanded_suit_cards_in_hand(suit):
                assert card.suit == suit

    def test_player_hand_should_be_smaller_after_playing(self):
        player = Player()
        card = Card("C", "S")
        trick = Trick()
        player.add_card_to_hand(card)
        l = len(player.hand)
        player.play_card(card, trick)
        assert len(player.hand) == l - 1

    def test_player_should_give_card_to_trick_when_playing(self):
        player = Player()
        card = Card("C", "S")
        trick = Trick()
        player.add_card_to_hand(card)
        player.play(trick, 0)
        assert len(trick) == 1


class TestDistributor:
    def setup_method(self, method):
        self.players = [Player(), Player(), Player(), Player()]
        self.deck = Deck()
        self.croupier = Distributor()

    def test_players_should_have_five_cards_in_hand(self):
        for player in self.players:
            assert len(player.hand) == 0

        self.croupier.distribute_five_cards_to_players(self.deck, self.players)
        for player in self.players:
            assert len(player.hand) == 5

    def test_player_should_have_two_more_cards(self):
        self.croupier.give_two_cards(self.deck, self.players[0])
        assert len(self.players[0].hand) == 2

    def test_player_should_have_three_more_cards(self):
        self.croupier.give_three_cards(self.deck, self.players[0])
        assert len(self.players[0].hand) == 3

    def test_deck_should_have_12_cards_after_first_distribution(self):
        self.croupier.distribute_five_cards_to_players(self.deck, self.players)
        assert len(self.deck) == 12


class TestGame:
    def setup_method(self, method):
        team1 = Team(0, Player("Alex"), Player("Thibaud"))
        team2 = Team(1, Player("Marie"), Player("Veltin"))
        deck = Deck()
        evaluator = TrickEvaluator()
        distributor = Distributor()
        referee = Referee()
        self.game = Game(0, team1, team2, deck, evaluator, distributor, referee, seed=36)

    def test_players_should_have_no_hand_at_beginning(self):
        for player in self.game.players:
            assert len(player.hand) == 0

    def test_players_should_have_8_cards_after_distribution(self):
        self.game.distribute_cards_and_choose_trump()
        for player in self.game.players:
            assert len(player.hand) == 8

    def test_first_distribution_should_reveal_card(self):
        revealed_card = self.game.perform_first_distribution_and_reveal_card()
        assert isinstance(revealed_card, Card)

    def test_players_should_have_8_minus_n_cards_in_hand_after_first_distribution(self):
        revealed_card = self.game.perform_first_distribution_and_reveal_card()
        assert isinstance(revealed_card, Card)

    def test_deck_should_be_empty_after_distribution(self):
        self.game.distribute_cards_and_choose_trump()
        assert len(self.game.deck) == 0

    def test_players_should_have_8_minus_n_cards_in_hand_after_n_turns(self):
        self.game.distribute_cards_and_choose_trump()
        for i in range(8):
            self.game.play_one_turn()
            for player in self.game.players:
                assert len(player.hand) == 8 - (i + 1)

    def test_teams_should_have_32_cards_total_after_game_has_been_played(self):
        self.game.distribute_cards_and_choose_trump()
        self.game.play()
        assert len(self.game.get_team_by_id(0).won_cards) + len(self.game.get_team_by_id(1).won_cards) == 32

    def test_total_points_at_the_end_should_be_162(self):
        self.game.distribute_cards_and_choose_trump()
        self.game.play()
        self.game.count_points()
        assert sum([team.current_game_points for team in self.game.teams]) == 162

    def test_play_should_not_fail(self):
        self.game.distribute_cards_and_choose_trump()
        assert self.game.play() == 0


class TestTrickEvaluator:
    def setup_method(self, method):
        self.evaluator = TrickEvaluator("C")  # Trump suit is Clubs

    def test_get_trump_rank(self):
        assert self.evaluator.get_rank(Card("C", "S")) == 0
        assert self.evaluator.get_rank(Card("C", "E")) == 1
        assert self.evaluator.get_rank(Card("C", "Q")) == 2
        assert self.evaluator.get_rank(Card("C", "K")) == 3
        assert self.evaluator.get_rank(Card("C", "T")) == 4
        assert self.evaluator.get_rank(Card("C", "A")) == 5
        assert self.evaluator.get_rank(Card("C", "N")) == 6
        assert self.evaluator.get_rank(Card("C", "J")) == 7

    def test_get_non_trump_rank(self):
        assert self.evaluator.get_rank(Card("D", "S")) == 0
        assert self.evaluator.get_rank(Card("D", "E")) == 1
        assert self.evaluator.get_rank(Card("D", "N")) == 2
        assert self.evaluator.get_rank(Card("D", "J")) == 3
        assert self.evaluator.get_rank(Card("D", "Q")) == 4
        assert self.evaluator.get_rank(Card("D", "K")) == 5
        assert self.evaluator.get_rank(Card("D", "T")) == 6
        assert self.evaluator.get_rank(Card("D", "A")) == 7

    def test_highest_rank_should_win_when_same_suit(self):
        assert self.evaluator.is_higher(Card("D", "T"), Card("D", "S"))
        assert self.evaluator.is_higher(Card("D", "A"), Card("D", "S"))
        assert self.evaluator.is_higher(Card("H", "K"), Card("H", "Q"))
        assert self.evaluator.is_higher(Card("C", "T"), Card("C", "Q"))
        assert self.evaluator.is_higher(Card("H", "K"), Card("H", "Q"))

    def test_trump_value_should_win_against_non_trump(self):
        assert self.evaluator.is_higher(Card("C", "E"), Card("D", "S"))
        assert self.evaluator.is_higher(Card("C", "S"), Card("H", "A"))
        assert self.evaluator.is_higher(Card("C", "K"), Card("S", "Q"))

    def test_winner_should_return_correct_index_without_offset(self):
        assert self.evaluator.winner(Trick(cards=[Card("C", "E"), Card("C", "T"), Card("C", "J"), Card("C", "Q")])) == 2
        assert self.evaluator.winner(Trick(cards=[Card("C", "E"), Card("D", "T"), Card("H", "J"), Card("S", "Q")])) == 0
        assert self.evaluator.winner(Trick(cards=[Card("D", "E"), Card("D", "T"), Card("H", "J"), Card("S", "Q")])) == 1
        assert self.evaluator.winner(Trick(cards=[Card("D", "E"), Card("C", "T"), Card("C", "J"), Card("H", "Q")])) == 2
        assert self.evaluator.winner(Trick(cards=[Card("D", "E"), Card("H", "T"), Card("S", "J"), Card("H", "Q")])) == 0

    def test_winner_should_return_correct_index_with_offset(self):
        trick1 = Trick(cards=[Card("C", "E"), Card("C", "T"), Card("C", "J"), Card("C", "Q")])
        assert self.evaluator.winner(trick1, who_started=1) == 3
        trick2 = Trick(cards=[Card("C", "E"), Card("D", "T"), Card("H", "J"), Card("S", "Q")])
        assert self.evaluator.winner(trick2, who_started=2) == 2
        trick3 = Trick(cards=[Card("D", "E"), Card("D", "T"), Card("H", "J"), Card("S", "Q")])
        assert self.evaluator.winner(trick3, who_started=3) == 0
        trick4 = Trick(cards=[Card("D", "E"), Card("C", "T"), Card("C", "J"), Card("H", "Q")])
        assert self.evaluator.winner(trick4, who_started=1) == 3
        trick5 = Trick(cards=[Card("D", "E"), Card("H", "T"), Card("S", "J"), Card("H", "Q")])
        assert self.evaluator.winner(trick5, who_started=3) == 3


class TestReferee:
    def setup_method(self, method):
        self.referee = Referee("C")

    def test_referee_should_be_good_at_math(self):
        for suit in ["D", "H", "S"]:
            assert self.referee.cards_points([Card(suit, "E"), Card(suit, "N"), Card(suit, "J")]) == 2
        assert self.referee.cards_points([Card("C", "E"), Card("C", "N"), Card("C", "J")]) == 34

    def test_referee_should_compute_team_score(self):
        team = Team(0, Player(), Player())
        team.get_cards(Trick([Card("C", "E"), Card("C", "N"), Card("C", "J")]))
        assert self.referee.count_team_points(team) == 34
        team.started = True
        assert self.referee.count_team_points(team) == 0


class TestGameCommentator:
    def setup_method(self, method):
        team1 = Team(0, Player("Alex"), Player("Thibaud"))
        team2 = Team(1, Player("Marie"), Player("Veltin"))
        deck = Deck()
        evaluator = TrickEvaluator()
        distributor = Distributor()
        referee = Referee()
        self.game = Game(0, team1, team2, deck, evaluator, distributor, referee)
        self.commentator = GameCommentator(1)

    def test_commentator_should_introduce_game(self):
        output = StringIO()
        self.commentator.comment_start_of_game(self.game, out=output)
        assert output.getvalue().strip() == """Game 0"""

    def test_commentator_should_announce_cards(self):
        output = StringIO()
        regex = re.compile(r"([\w]+ plays [\w]+ of [\w]+(, )*){4}.")
        self.game.distribute_cards_and_choose_trump()
        trick = self.game.play_one_turn()
        self.commentator.comment_turn(self.game, trick, out=output)
        comment = output.getvalue().strip()
        assert regex.match(comment) is not None

    def test_commentator_should_comment_start_of_turn(self):
        output = StringIO()
        regex = re.compile(r"[\w]+ starts.")
        self.game.distribute_cards_and_choose_trump()
        self.commentator.comment_start_of_turn(self.game, out=output)
        comment = output.getvalue().strip()
        assert regex.match(comment) is not None

    def test_commentator_should_comment_end_of_turn(self):
        output = StringIO()
        regex = re.compile(r"[\w]+ wins.")
        self.game.distribute_cards_and_choose_trump()
        self.game.play_one_turn()
        self.commentator.comment_end_of_turn(self.game, out=output)
        comment = output.getvalue().strip()
        assert regex.match(comment) is not None

    def test_commentator_should_comment_end_of_game(self):
        output = StringIO()
        regex = re.compile(r"(Team \w+: \d{1,3} points.\n){2}Team \w+ wins!")
        self.game.distribute_cards_and_choose_trump()
        self.game.play()
        self.game.count_points()
        self.commentator.comment_end_of_game(self.game, out=output)
        comment = output.getvalue().strip()
        assert regex.match(comment) is not None

    def test_commentator_should_comment_distribution(self):
        output = StringIO()
        regex = re.compile(r"Trump suit will be (Clubs|Hearts|Diamonds|Spades).")
        self.game.distribute_cards_and_choose_trump()
        self.commentator.comment_distribution(self.game, out=output)
        comment = output.getvalue().strip()
        assert regex.match(comment) is not None


class TestGameNightCommentator:
    def setup_method(self, method):
        team1 = Team(0, Player("Alex"), Player("Thibaud"))
        team2 = Team(1, Player("Marie"), Player("Veltin"))
        evaluator = TrickEvaluator()
        distributor = Distributor()
        referee = Referee()
        self.game_night = GameNight(team1, team2, evaluator, distributor, referee)
        self.commentator = GameNightCommentator(1)

    def test_commentator_should_introduce_game_night(self):
        output = StringIO()
        regex = re.compile(r"(Team \w+: \w*, \w*.\n*){2}")
        self.game_night.play()
        self.commentator.introduce_game_night(self.game_night, out=output)
        comment = output.getvalue().strip()
        assert regex.match(comment) is not None

    def test_commentator_should_annonce_game_night_winner(self):
        output = StringIO()
        regex = re.compile(r"(Team \w+: \d{1,4} points.\n){2}Team \w+ wins!")
        self.game_night.play()
        self.commentator.comment_end_of_game_night(self.game_night, out=output)
        comment = output.getvalue().strip()
        assert regex.match(comment) is not None


class TestTeam:
    def setup_method(self, method):
        self.team = Team(0, Player("Marie"), Player("Veltin"))
        self.team2 = Team(1, Player("Thibaud"), Player("Alex"))

    def test_team_should_know_if_it_started(self):
        assert not self.team.started
        self.team.has_started(False)
        assert not self.team.started
        self.team.has_started(True)
        assert self.team.started

    def test_team_should_have_one_more_card_after_get_card(self):
        self.team.get_card(Card("D", "E"))
        assert len(self.team.won_cards) == 1
        self.team.get_card(Card("D", "S"))
        assert len(self.team.won_cards) == 2

    def test_team_should_have_four_cards_after_winning_a_trick(self):
        self.team.get_cards(Trick([Card("D", "S"), Card("D", "E"), Card("D", "N"), Card("D", "T")]))
        assert len(self.team.won_cards) == 4
        self.team.get_cards(Trick([Card("C", "S"), Card("C", "E"), Card("C", "N"), Card("C", "T")]))
        assert len(self.team.won_cards) == 8

    def test_team_should_introduce_itself_properly(self):
        assert str(self.team) == "Team 0: Marie and Veltin"
        assert str(self.team2) == "Team 1: Thibaud and Alex"

    def test_team_members_should_know_team_id(self):
        assert self.team.player1.teamID == 0
        assert self.team.player2.teamID == 0
        assert self.team2.player1.teamID == 1
        assert self.team2.player2.teamID == 1
