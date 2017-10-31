import re
from io import StringIO

import pytest

from cards import Card, CardStack, Deck, Hand, Trick, Trump, NonTrump, CardSet
from cards.trump import RankedCard
from commentators import GameCommentator, RoundCommentator
from game import Game, Round
from officials import Distributor, Referee
from players import Player, Team


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

    def test_cards_can_cast_themselves_to_ranked_cards(self):
        card = Card("C", "A")
        ranked_card = card.to_ranked("C")
        assert isinstance(ranked_card, Trump)
        assert ranked_card == Trump(card)
        card = Card("H", "A")
        ranked_card = card.to_ranked("C")
        assert isinstance(ranked_card, NonTrump)
        assert ranked_card == NonTrump(card)

    def test_with_owner_return_new_card_with_owner(self):
        player = Player()
        card = Card("C", "A")
        new_card = card.with_owner(player)
        assert new_card.owner is player


class TestCardSet:
    def test_set_of_ranked_cards_can_add_points(self):
        cardset = CardSet()
        cardset.add_card(Trump(Card("C", "J")))
        cardset.add_card(NonTrump(Card("H", "J")))
        cardset.add_card(NonTrump(Card("D", "A")))
        assert cardset.total_points == 20 + 2 + 11


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

    def test_hand_can_cast_itself_to_new_ranked(self):
        hand = Hand()
        hand.add_card(Card("C", "A"))
        hand.add_card(Card("D", "A"))
        new_hand = hand.to_ranked("C")
        for card in new_hand:
            assert isinstance(card, RankedCard)

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

    def test_player_should_have_only_ranked_cards_after_setting_trump(self):
        player = Player()
        cards = [Card("C", "S"), Card("D", "S"), Card("H", "S"),
                 Card("S", "S"), Card("C", "E"), Card("D", "T"),
                 Card("H", "J"), Card("S", "Q")]
        for card in cards:
            player.add_card_to_hand(card)
        player.set_trump_suit("C")
        for new_card in player.hand:
            assert isinstance(new_card, RankedCard)

    def test_player_should_set_owner_on_his_cards(self):
        player = Player()
        cards = [Card("C", "S"), Card("D", "S"), Card("H", "S"),
                 Card("S", "S"), Card("C", "E"), Card("D", "T"),
                 Card("H", "J"), Card("S", "Q")]
        for card in cards:
            player.add_card_to_hand(card)
        for card in player.hand:
            assert card.owner is player


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


class TestRound:
    def setup_method(self, method):
        team1 = Team(0, Player("Alex"), Player("Thibaud"))
        team2 = Team(1, Player("Marie"), Player("Veltin"))
        deck = Deck()
        distributor = Distributor()
        referee = Referee()
        self.round = Round(0, team1, team2, deck, distributor,
                           referee, seed=36)

    def test_players_should_have_no_hand_at_beginning(self):
        for player in self.round.players:
            assert len(player.hand) == 0

    def test_players_should_have_8_cards_after_distribution(self):
        self.round.distribute_cards_and_choose_trump()
        for player in self.round.players:
            assert len(player.hand) == 8

    def test_all_cards_should_be_ranked_after_distribution(self):
        self.round.distribute_cards_and_choose_trump()
        for player in self.round.players:
            for card in player.hand:
                assert isinstance(card, RankedCard)

    def test_first_distribution_should_reveal_card(self):
        revealed_card = self.round.perform_first_distribution_and_reveal_card()
        assert isinstance(revealed_card, Card)

    def test_players_should_have_5_cards_in_hand_after_first_distribution(self):
        _ = self.round.perform_first_distribution_and_reveal_card()
        for player in self.round.players:
            assert len(player.hand) == 5

    def test_deck_should_be_empty_after_distribution(self):
        self.round.distribute_cards_and_choose_trump()
        assert len(self.round.deck) == 0

    def test_players_should_have_8_minus_n_cards_in_hand_after_n_turns(self):
        self.round.distribute_cards_and_choose_trump()
        for i in range(8):
            self.round.play_one_turn()
            for player in self.round.players:
                assert len(player.hand) == 8 - (i + 1)

    def test_teams_should_have_32_cards_total_after_game_has_been_played(self):
        self.round.distribute_cards_and_choose_trump()
        print(self.round.get_team_by_id(0).player1.hand[0].owner)
        self.round.play()
        assert len(self.round.get_team_by_id(0).won_cards) + len(self.round.get_team_by_id(1).won_cards) == 32

    def test_total_points_at_the_end_should_be_162(self):
        self.round.distribute_cards_and_choose_trump()
        self.round.play()
        self.round.count_points()
        assert sum([team.current_game_points for team in self.round.teams]) == 162

    def test_play_should_not_fail(self):
        self.round.distribute_cards_and_choose_trump()
        assert self.round.play() == 0


class TestTrick:
    def test_winner_should_return_correct_index_without_offset(self):
        trick = Trick(cards=[Card("C", "E"), Card("C", "T"), Card("C", "J"), Card("C", "Q")]).to_ranked("C")
        assert trick.winner == Card("C", "J")
        trick = Trick(cards=[Card("C", "E"), Card("D", "T"), Card("H", "J"), Card("S", "Q")]).to_ranked("C")
        assert trick.winner == Card("C", "E")
        trick = Trick(cards=[Card("D", "E"), Card("D", "T"), Card("H", "J"), Card("S", "Q")]).to_ranked("C")
        assert trick.winner == Card("D", "T")
        trick = Trick(cards=[Card("D", "E"), Card("C", "T"), Card("C", "J"), Card("H", "Q")]).to_ranked("C")
        assert trick.winner == Card("C", "J")
        trick = Trick(cards=[Card("D", "E"), Card("H", "T"), Card("S", "J"), Card("H", "Q")]).to_ranked("C")
        assert trick.winner == Card("D", "E")


class TestReferee:
    def setup_method(self, method):
        self.referee = Referee()

    def test_referee_should_compute_team_score(self):
        team = Team(0, Player(), Player())
        cards = [Card("C", "E"), Card("C", "N"), Card("C", "J")]
        trick = Trick(cards).to_ranked("C")
        team.get_cards(trick)
        assert self.referee.count_team_points(team) == 34
        team.started = True
        assert self.referee.count_team_points(team) == 0


class TestGameCommentator:
    def setup_method(self, method):
        team1 = Team(0, Player("Alex"), Player("Thibaud"))
        team2 = Team(1, Player("Marie"), Player("Veltin"))
        deck = Deck()
        distributor = Distributor()
        referee = Referee()
        self.game = Round(0, team1, team2, deck, distributor, referee)
        self.output = StringIO()
        self.commentator = RoundCommentator(1, stream=self.output)

    def test_commentator_should_introduce_game(self):
        self.commentator.comment_start_of_round(self.game)
        assert self.output.getvalue().strip() == """Game 0"""

    def test_commentator_should_announce_cards(self):
        regex = re.compile(r"([\w]+ plays [\w]+ of [\w]+(, )*){4}.")
        self.game.distribute_cards_and_choose_trump()
        trick = self.game.play_one_turn()
        self.commentator.comment_turn(self.game, trick)
        comment = self.output.getvalue().strip()
        assert regex.match(comment) is not None

    def test_commentator_should_comment_end_of_turn(self):
        regex = re.compile(r"[\w]+ wins.")
        self.game.distribute_cards_and_choose_trump()
        self.game.play_one_turn()
        self.commentator.comment_end_of_turn(self.game)
        comment = self.output.getvalue().strip()
        assert regex.match(comment) is not None

    def test_commentator_should_comment_end_of_game(self):
        regex = re.compile(r"(Team \w+: \d{1,3} points.\n){2}Team \w+ wins!")
        self.game.distribute_cards_and_choose_trump()
        self.game.play()
        self.game.count_points()
        self.commentator.comment_end_of_round(self.game)
        comment = self.output.getvalue().strip()
        assert regex.match(comment) is not None

    def test_commentator_should_comment_distribution(self):
        regex = re.compile(r"Trump suit will be (Clubs|Hearts|Diamonds|Spades).")
        self.game.distribute_cards_and_choose_trump()
        self.commentator.comment_distribution(self.game)
        comment = self.output.getvalue().strip()
        assert regex.match(comment) is not None


class TestGameNightCommentator:
    def setup_method(self, method):
        team1 = Team(0, Player("Alex"), Player("Thibaud"))
        team2 = Team(1, Player("Marie"), Player("Veltin"))
        distributor = Distributor()
        referee = Referee()
        self.game_night = Game(team1, team2, distributor, referee, verbosity=1)
        self.commentator = GameCommentator(1)

    def test_commentator_should_introduce_game_night(self):
        output = StringIO()
        regex = re.compile(r"(Team \w+: \w*, \w*.\n*){2}")
        self.game_night.play()
        self.commentator.introduce_game(self.game_night, out=output)
        comment = output.getvalue().strip()
        assert regex.match(comment) is not None

    def test_commentator_should_annonce_game_night_winner(self):
        output = StringIO()
        regex = re.compile(r"(Team \w+: \d{1,4} points.\n){2}Team \w+ wins!")
        self.game_night.play()
        self.commentator.comment_end_of_game(self.game_night, out=output)
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


class TestTrumpCard:
    def test_get_trump_rank(self):
        assert Trump(Card("C", "S")).rank == 0
        assert Trump(Card("C", "E")).rank == 1
        assert Trump(Card("C", "Q")).rank == 2
        assert Trump(Card("C", "K")).rank == 3
        assert Trump(Card("C", "T")).rank == 4
        assert Trump(Card("C", "A")).rank == 5
        assert Trump(Card("C", "N")).rank == 6
        assert Trump(Card("C", "J")).rank == 7

    def test_get_non_trump_rank(self):
        assert NonTrump(Card("D", "S")).rank == 0
        assert NonTrump(Card("D", "E")).rank == 1
        assert NonTrump(Card("D", "N")).rank == 2
        assert NonTrump(Card("D", "J")).rank == 3
        assert NonTrump(Card("D", "Q")).rank == 4
        assert NonTrump(Card("D", "K")).rank == 5
        assert NonTrump(Card("D", "T")).rank == 6
        assert NonTrump(Card("D", "A")).rank == 7

    def test_get_trump_points(self):
        assert Trump(Card("C", "S")).points == 0
        assert Trump(Card("C", "E")).points == 0
        assert Trump(Card("C", "Q")).points == 3
        assert Trump(Card("C", "K")).points == 4
        assert Trump(Card("C", "T")).points == 10
        assert Trump(Card("C", "A")).points == 11
        assert Trump(Card("C", "N")).points == 14
        assert Trump(Card("C", "J")).points == 20

    def test_get_non_trump_points(self):
        assert NonTrump(Card("D", "S")).points == 0
        assert NonTrump(Card("D", "E")).points == 0
        assert NonTrump(Card("D", "N")).points == 0
        assert NonTrump(Card("D", "J")).points == 2
        assert NonTrump(Card("D", "Q")).points == 3
        assert NonTrump(Card("D", "K")).points == 4
        assert NonTrump(Card("D", "T")).points == 10
        assert NonTrump(Card("D", "A")).points == 11

    def test_highest_rank_should_win_when_same_suit(self):
        assert NonTrump(Card("D", "T")).is_higher_than(NonTrump(Card("D", "S")))
        assert NonTrump(Card("D", "A")).is_higher_than(NonTrump(Card("D", "S")))
        assert NonTrump(Card("H", "K")).is_higher_than(NonTrump(Card("H", "Q")))
        assert Trump(Card("C", "T")).is_higher_than(Trump(Card("C", "Q")))
        assert NonTrump(Card("H", "K")).is_higher_than(NonTrump(Card("H", "Q")))

    def test_trump_value_should_win_against_non_trump(self):
        assert Trump(Card("C", "E")).is_higher_than(NonTrump(Card("D", "S")))
        assert Trump(Card("C", "S")).is_higher_than(NonTrump(Card("H", "A")))
        assert Trump(Card("C", "K")).is_higher_than(NonTrump(Card("S", "Q")))