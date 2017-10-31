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