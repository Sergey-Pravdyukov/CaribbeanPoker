import numpy as np
from colorama import init 
import copy  
import random
import argparse
import math
from statistics import mode
from collections import Counter


global result
result =0
# Unicode suits characters
suits = {"spades": u'\u2660', 
         "hearts": u'\u2665', 
         "diamonds": u'\u2666', 
         "clubs": u'\u2663'}

Dictionary = dict()
Dictionary['1']=1
Dictionary['2']=2
Dictionary['3']=3
Dictionary['4']=4
Dictionary['5']=5
Dictionary['6']=6
Dictionary['7']=7
Dictionary['8']=8
Dictionary['9']=9
Dictionary['T']=10
Dictionary['J']=11
Dictionary['Q']=12
Dictionary['K']=13
Dictionary['A']=14

def allCroupierCardsWereDealed(croupiercard,PlayerHands):
    cardsToBeDealed =[turnHandIntoList(croupiercard)[0][0]+ x for x in ['D','H','S','C']]
    ListOfDealedCards= [turnHandIntoList(x) for x in PlayerHands]
    ListOfDealedCards.append(turnHandIntoList(croupiercard))
    ListOfDealedCards = [item for sublist in ListOfDealedCards for item in sublist]

    return set(cardsToBeDealed).issubset(ListOfDealedCards)

def genCardDeck():
    cardRanks = [str(x) for x in range(2, 10)] + ['T','J', 'Q', 'K', 'A']

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

def turnHandIntoList(playerHand):
    result=[]
    for i in playerHand:
        if i['suit']== u'\u2660':
            result.append(i['rank']+'S')
        if i['suit']== u'\u2665':
            result.append(i['rank']+'H')
        if i['suit']== u'\u2666':
            result.append(i['rank']+'D')
        if i['suit']== u'\u2663':
            result.append(i['rank']+'C')
    return result

def emulateGame(cardDeck, playersNum):
    cardsPerPlayer = 5
    workingCardDeck = copy.deepcopy(cardDeck)
    random.shuffle(workingCardDeck)
    croupierHand = workingCardDeck[:1]
    playerHands = []
    decisions =[]
    for i in range(playersNum):
        playerHands.append(workingCardDeck[cardsPerPlayer * (i + 1):cardsPerPlayer * (i + 2)])
    printCardDeck(croupierHand, "croupier hand")
    for (i, playerHand) in enumerate(playerHands):
        printCardDeck(playerHand, "player " + str(i) + " hand")
    for i in range(5):
        if DefineCombination(turnHandIntoList(playerHands[i])) > ("1Pair",[2,2,3,4,5]):
            decisions.append("bet")
        else:
            decisions.append("fold")
    if allCroupierCardsWereDealed(croupierHand,PlayerHands=playerHands) and turnHandIntoList(croupierHand)[0][0] not in ['K','A']:
        decisions = ['bet','bet','bet','bet','bet']
    print(decisions)
    croupierHand = workingCardDeck[0:playersNum]
    printCardDeck(croupierHand, "croupier hand")
    print()
    for ind,i in enumerate(playerHands):
        global result
        if decisions[ind]=='fold':
            print("Player"+ str(ind) + " is losing 5 dolars!")
            result -=5
        if decisions[ind]=='bet' and DefineCombination(turnHandIntoList(croupierHand)) < ('0High Card',[14,13,4,3,2]):
            print("Player"+ str(ind)+ " is winning 5 dolars")
            result +=5
        if DefineCombination(turnHandIntoList(croupierHand))>DefineCombination(turnHandIntoList(i)) and decisions[ind]=='bet' and DefineCombination(turnHandIntoList(croupierHand)) >= ('0High Card',[14,13,4,3,2]):
            print("Player"+ str(ind) + " is losing 15 dolars!")
            result -=15
        if DefineCombination(turnHandIntoList(croupierHand)) < DefineCombination(turnHandIntoList(i)) and decisions[ind] == 'bet' and DefineCombination(turnHandIntoList(croupierHand)) >= ('0High Card',[14,13,4,3,2]):
            if DefineCombination(turnHandIntoList(i))[0] == "2Two pair":
                print("Player"+ str(ind) + " is winning 25 dolars")
                result +=25
            elif DefineCombination(turnHandIntoList(i))[0] == "3Three of a kind":
                print("Player"+ str(ind) + " is winning 35 dolars")
                result +=35
            elif DefineCombination(turnHandIntoList(i))[0] == "4Straight":
                print("Player"+ str(ind) + " is winning 45 dolars")
                result +=45
            elif DefineCombination(turnHandIntoList(i))[0] == "5Flush":
                print("Player"+ str(ind) + " is winning 55 dolars")
                result +=55
            elif DefineCombination(turnHandIntoList(i))[0] == "6Full House":
                print("Player"+ str(ind) + " is winning 75 dolars")
                result +=75
            elif DefineCombination(turnHandIntoList(i))[0] == "7Quads":
                print("Player"+ str(ind) + " is winning 205 dolars")
                result +=205
            elif DefineCombination(turnHandIntoList(i))[0] == "8Straight Flush":
                print("Player"+ str(ind) + " is winning 505 dolars")
                result +=505
            elif DefineCombination(turnHandIntoList(i))[0] == "9Royal Flush":
                print("Player"+ str(ind) + " is winning 1005 dolars")
                result +=1005
            else:
                print("Player" + str(ind) + " is winning 15 dolars!")
                result +=15

def DefineCombination(l):
    list2 = list()
    for i in l:
        list2.append(i[0])

    list2 = list(map(lambda x: Dictionary[x],list2))
    list2 = sorted(list2)[::-1]
    c = Counter(item for item in list2)
    list2 = sorted(list2, key = lambda x: -c[x])


    if  set([11, 12, 13, 14, 10]) == set(list2) and len(set([l[0][1], l[1][1], l[2][1], l[3][1], l[4][1]])) == 1:
        return '9Royal Flush' ,list2
    if (set([14, 2, 3, 4, 5]) == set(list2) or set([6, 2, 4, 3, 5]) == set(list2) or set([6, 7, 3, 4, 5]) == set(list2) or set([7, 6, 8, 4, 5]) == set(list2) or set([7, 6, 8, 9, 5]) == set(list2) or set([7, 6, 8, 9, 10]) == set(list2) or set([7, 8, 9, 10, 11]) == set(list2) or set([11, 12, 8, 9, 10]) == set(list2) or set([11, 12, 13, 9, 10]) == set(list2) or set([11, 12, 13, 14, 10])== set(list2) ) and len(set([l[0][1],l[1][1],l[2][1],l[3][1],l[4][1]])) ==1:
        if set([14, 2, 3, 4, 5]) == set(list2):
            return '8Straight Flush' , [5,4,3,2,14]
        else:
            return '8Straight Flush' , list2
    if len(set([l[0][0],l[1][0],l[2][0],l[3][0],l[4][0]]))==2 and list2.count(mode(list2))==4 :
        return '7Quads' , list2
    if len(set([l[0][0],l[1][0],l[2][0],l[3][0],l[4][0]]))==2 and list2.count(mode(list2))==3 :
        return '6Full House' , list2
    if len(set([l[0][1],l[1][1],l[2][1],l[3][1],l[4][1]])) ==1:
        return '5Flush' , list2
    if set([14, 2, 3, 4, 5]) == set(list2) or set([6, 2, 4, 3, 5]) == set(list2) or set([6, 7, 3, 4, 5]) == set(list2) or set([7, 6, 8, 4, 5]) == set(list2) or set([7, 6, 8, 9, 5]) == set(list2) or set([7, 6, 8, 9, 10]) == set(list2) or set([7, 8, 9, 10, 11]) == set(list2) or set([11, 12, 8, 9, 10]) == set(list2) or set([11, 12, 13, 9, 10]) == set(list2) or set([11, 12, 13, 14, 10])== set(list2) :
        if set([14, 2, 3, 4, 5]) == set(list2):
            return '4Straight' , [5 ,4 ,3 ,2 ,14]
        else:
            return '4Straight' ,list2
    if len(set([l[0][0],l[1][0],l[2][0],l[3][0],l[4][0]]))==3 and list2.count(mode(list2))==3 :
        return '3Three of a kind' , list2
    if len(set([l[0][0],l[1][0],l[2][0],l[3][0],l[4][0]]))==3 and list2.count(mode(list2))==2 :
        return '2Two pair'  , list2
    if len(set([l[0][0],l[1][0],l[2][0],l[3][0],l[4][0]]))==4 :
        return "1Pair", list2
    if len(set([l[0][0],l[1][0],l[2][0],l[3][0],l[4][0]]))==5 and len(set([l[0][1],l[1][1],l[2][1],l[3][1],l[4][1]])) >1 :
        return "0High Card" , list2



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--playersNum", type=int, default=5, choices=range(1, 10), help="Number of players exclude croupier.")
    args = parser.parse_args()
    for i in range(100000):
        cardDeck = genCardDeck()
        printCardDeck(cardDeck)
        emulateGame(cardDeck, args.playersNum)

    print(result)
