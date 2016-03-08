"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

My ipython and jupyter are not working; I'm turning in the exercise as a file instead.

"""

import random


class Card(object):
    """Represents a standard playing card.
    
    Attributes:
      suit: integer 0-3
      rank: integer 1-13
    """

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7", 
              "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a human-readable string representation."""
        return "{0} of {1}".format(Card.rank_names[self.rank],
                                   Card.suit_names[self.suit])

    def __cmp__(self, other):
        """Compares this card to other, first by suit, then rank.

        Returns a positive number if this > other; negative if other > this;
        and 0 if they are equivalent.
        """
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return cmp(t1, t2)


class Deck(object):
    """Represents a deck of cards.

    Attributes:
      cards: list of Card objects.
    """
    
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def add_card(self, card):
        """Adds a card to the deck."""
        self.cards.append(card)

    def remove_card(self, card):
        """Removes a card from the deck."""
        self.cards.remove(card)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.

        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the cards in ascending order."""
        self.cards.sort()

    def move_cards(self, hand, num):
        """Moves the given number of cards from the deck into the Hand.

        hand: destination Hand object
        num: integer number of cards to move
        """
        for i in range(num):
            hand.add_card(self.pop_card())
    
    def deal_hands(self, num_hands, num_cards):
        """Return a list of new Hand objects dealt from the Deck.
        
        num_hands: number of Hands to return
        num_cards: number of Cards per Hand
        """
        hands = []
        for i in range(num_hands):
            h = Hand()
            self.move_cards(h,num_cards)
            hands.append(h)
        return hands



class Hand(Deck):
    """Represents a hand of playing cards."""
    
    def __init__(self, label=''):
        self.cards = []
        self.label = label


def find_defining_class(obj, method_name):
    """Finds and returns the class object that will provide 
    the definition of method_name (as a string) if it is
    invoked on obj.

    obj: any python object
    method_name: string method name
    """
    for ty in type(obj).mro():
        if method_name in ty.__dict__:
            return ty
    return None


# if __name__ == '__main__':
#     # Example of using find_defining_class to probe object inheritance
#     test_hand = Hand()
#     print "'shuffle' is a method of", find_defining_class(test_hand, 'shuffle')

#     # TODO: The following test code won't fully work until you define the deal_hands Deck method
#     deck = Deck()
#     deck.shuffle()
#     hands = deck.deal_hands(4, 5)
#     for i, hand in enumerate(hands):
#         print "Hand {}:".format(i)
#         hand.sort()
#         print hand




class PokerHand(Hand):

    def __init__(self):
        super(PokerHand,self).__init__()

        
    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def val_hist(self):
        """Builds a histogram of the ranks that appear in the hand.

        Stores the result in attribute ranks.
        """
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def has_pair(self):
        for val in self.ranks.values():
            if val>=2:
                return True
        return False

    def has_twopair(self):
        numPairs = 0
        for val in self.ranks.values():
            if val>=2:
                numPairs+=1
        return numPairs>=2

    def has_three(self):
        for val in self.ranks.values():
            if val>=3:
                return True
        return False

    def has_four(self):
        for val in self.ranks.values():
            if val>=4:
                return True
        return False

    def has_fullhouse(self):
        return self.has_twopair() and self.has_three()

    def has_straight(self):
        sortedHand = sorted(self.cards)
        numConsec = 0
        for i in range(len(sortedHand)-1):
            if sortedHand[i+1].rank-sortedHand[i].rank==1:
                numConsec+=1
            elif sortedHand[i+1].rank-sortedHand[i].rank>1:
                numConsec=0
            if numConsec>=5:
                return True
        return False

    def has_straightflush(self):
        sortedHand = sorted(self.cards)
        numConsec = 0
        consec_suit = sortedHand[0].suit
        for i in range(len(sortedHand)-1):
            if sortedHand[i+1].rank-sortedHand[i].rank==1 and sortedHand[i+1].suit==consec_suit:
                numConsec+=1
            elif sortedHand[i+1].rank-sortedHand[i].rank>1:
                numConsec=0
                consec_suit=sortedHand[i+1].suit
            if numConsec>=5:
                return True
        return False

    def classify(self):
        self.suit_hist()
        self.val_hist()
        
        if self.has_straightflush():
            self.label = 'Straight Flush'
        elif self.has_four():
            self.label = 'Four of a Kind'
        elif self.has_fullhouse():
            self.label = 'Full House'
        elif self.has_flush():
            self.label = 'Flush'
        elif self.has_straight():
            self.label = 'Straight'
        elif self.has_three():
            self.label = 'Three of a Kind'
        elif self.has_twopair():
            self.label = 'Two Pair'
        elif self.has_pair():
            self.label = 'Pair'
        else:
            self.label = 'None'



if __name__ == '__main__':
    # Create a new Deck
    deck = Deck()
    deck.shuffle()

    # Deal the cards and classify the hands. You'll need to add more tests as you create methods
    for i in range(7):
        print "Trial {}:".format(i)
        hand = PokerHand()
        deck.move_cards(hand, 7)  
        # Note: Why aren't we using the deal_hands Deck method you wrote? How could we modify it so that we _could_ use it?
        hand.sort()
        print hand
        hand.classify()
        print hand.label
        print ''