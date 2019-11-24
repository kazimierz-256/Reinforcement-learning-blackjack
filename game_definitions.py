from enum import Enum, auto


class Card(Enum):
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    QUEEN = auto()
    KING = auto()
    JACK = auto()
    ACE = auto()


class Action(Enum):
    HIT = auto()
    STAND = auto()


card_values = {
    Card.TWO: [2],
    Card.THREE: [3],
    Card.FOUR: [4],
    Card.FIVE: [5],
    Card.SIX: [6],
    Card.SEVEN: [7],
    Card.EIGHT: [8],
    Card.NINE: [9],
    Card.TEN: [10],
    Card.QUEEN: [10],
    Card.KING: [10],
    Card.JACK: [10],
    Card.ACE: [1, 11],
}


bust_from = 22


class Status(Enum):
    PLAYER_WON = auto()
    DEALER_WON = auto()
    DRAW = auto()
    STILL_PLAYING = auto()
