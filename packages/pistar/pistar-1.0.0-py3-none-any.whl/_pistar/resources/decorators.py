from _pistar.utilities.action_word import Keyword


def action_word(function):
    return Keyword()(function)
