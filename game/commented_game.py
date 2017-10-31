from commentators.game_commentator import GameCommentator


class CommentedGame(object):
    def __init__(self, game):
        self.game = game
        self.commentator = GameCommentator()

    def start(self):
        self.commentator.introduce_game(self.game)

    def play(self):
        self.game.play()
        self.commentator.comment_end_of_game(self.game)