import numpy as np

from colorama import init 
  
# Unicode suits characters
suits = {"spades": u'\u2660', 
         "hearts": u'\u2665', 
         "diamonds": u'\u2666', 
         "clubs": u'\u2663'}

def genCardDeck():
    cardRanks = [str(x) for x in range(2, 11)] + ['J', 'Q', 'K', 'A']

    cardDeckArrays = list(map(lambda y: list(map(lambda x: "".join([x, y]), cardRanks)), list(suits.values())))
    cardDeckArray = np.concatenate(cardDeckArrays).tolist()
    cardDeck = list(map(lambda card: {"rank": card[0], "suit": card[1]} if len(card) == 2 else {"rank": card[0:2], "suit": card[2]} , cardDeckArray))

    return cardDeck

def printCardDeck(cardDeck):
    init() 
    blackColor = '\033[37m'
    redColor = '\033[91m'
    for card in cardDeck:
        color = blackColor if card["suit"] in [suits["spades"], suits["clubs"]] else redColor   
        print(color, card['rank'] + card['suit'])

if __name__ == '__main__':
    cardDeck = genCardDeck()
    printCardDeck(cardDeck)

    