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
    cardRanks = [(str(x), str(x)) for x in range(2, 11)] + [('J', str(11)), ('Q', str(12)), ('K', str(13)), ('A', str(14))]

    cardDeckArrays = list(map(lambda y: list(map(lambda x: (x, y), cardRanks)), list(suits.values())))
    cardDeckArray = np.concatenate(cardDeckArrays).tolist()
    cardDeck = list(map(lambda card: {"rank": card[0][0], "suit": card[1], "numRank": card[0][1]} if len(card) == 2 else {"rank": card[0:2], "suit": card[2]} , cardDeckArray))

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

def getStatistics(croupierHand, playerHands):
    AKsum = 0
    specialRank = croupierHand[0]['rank']
    if (specialRank in ['K', 'A']):
        AKsum += 1
    specialRankNum = 1
    for hand in playerHands:
        for card in hand:
            if (card['rank'] in ['K', 'A']):
                AKsum += 1
            if (card['rank'] == specialRank):
                specialRankNum += 1
    
    totalSpecialRankNum = 4
    totalAKs = 8
    return (totalAKs - AKsum, totalSpecialRankNum - specialRankNum)

def emulateGame(cardDeck, playersNum, showCroupier):
    cardsPerPlayer = 5
    workingCardDeck = copy.deepcopy(cardDeck)
    random.shuffle(workingCardDeck)
    croupierHand = workingCardDeck[:cardsPerPlayer]
    playerHands = []
    for i in range(playersNum):
        playerHands.append(workingCardDeck[cardsPerPlayer * (i + 1):cardsPerPlayer * (i + 2)])

    printCardDeck(croupierHand[:1], "croupier hand")            # maybe move to def
    for (i, playerHand) in enumerate(playerHands):
        printCardDeck(playerHand, "player " + str(i) + " hand")
    if showCroupier == 1:
        printCardDeck(croupierHand, "croupier full hand")

    AKsum, specialRankNum = getStatistics(croupierHand, playerHands)
    print('A + K remains:', AKsum)
    print('Special cards remains:', specialRankNum)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--playersNum", type=int, default=5, choices=range(1, 10), help="Number of players exclude croupier.")
    parser.add_argument("-s", "--showCroupier", type=int, default=0, choices=range(0, 2), help="1 for showing full croupier hand. 0 otherwise.")
    args = parser.parse_args()

    cardDeck = genCardDeck()
    printCardDeck(cardDeck)
    # emulateGame(cardDeck, args.playersNum, args.showCroupier)

    