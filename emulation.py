import numpy as np
from colorama import init 
import copy  
import random
import argparse

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

def printCardDeck(cardDeck, message=None):
    init() 
    blackColor = '\033[37m'
    redColor = '\033[91m'
    if message is not None:
        print(blackColor, message + ":", end = " ")
    for card in cardDeck:
        color = blackColor if card["suit"] in [suits["spades"], suits["clubs"]] else redColor   
        print(color, card['rank'] + card['suit'], end=' ')
    print()

def emulateGame(cardDeck, playersNum):
    cardsPerPlayer = 5
    workingCardDeck = copy.deepcopy(cardDeck)
    random.shuffle(workingCardDeck)
    croupierHand = workingCardDeck[:cardsPerPlayer]
    playerHands = []
    for i in range(playersNum):
        playerHands.append(workingCardDeck[cardsPerPlayer * (i + 1):cardsPerPlayer * (i + 2)])
    printCardDeck(croupierHand, "croupier hand")
    for (i, playerHand) in enumerate(playerHands):
        printCardDeck(playerHand, "player " + str(i) + " hand")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--playersNum", type=int, default=5, choices=range(1, 10), help="Number of players exclude croupier.")
    args = parser.parse_args()

    cardDeck = genCardDeck()
    printCardDeck(cardDeck)
    emulateGame(cardDeck, args.playersNum)

    