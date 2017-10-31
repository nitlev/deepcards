from game.commentators import GameCommentator
from .game import Game


class CommentedGame(object):
    def __init__(self, game: Game):
        self.game = game
        self.commentator = GameCommentator()

    def start(self):
        self.commentator.introduce_game(self.game)

    def play(self):
        self.game.play()
        self.commentator.comment_end_of_game(self.game)