"""
  Original - Jan 22, 2010 - Gary Hollingshead

  Deck.py
  This contains the Deck class, which in turn contains cards for that deck.
  Each card is a list in the form:
  card["name", "description", "front_pic.png", "back_pic.png", Use_Function, 
  (Location_in_memory, "Deck_Name", "Location"), index_number]

  Updater: Gary Hollinghead, Feb 1, 2010
  Update: Changed Use and Discard to pass the card to the function of the card, 
    changed GetName to return just the name of the next card, addded a name to the deck
    and added it to a 2 part list for the location so each card knows where it belongs 
    and where it is now, added some MINOR functionality to drawcard as well

  Updater: Gary Hollingshead, Feb 3, 2010
  Update: Changed draw card to include an option to search for the next card of "type"
    where type is the name of the card or partial name of the card to search the deck
    for, added a Place variable which is the location of the deck in memory

  Updater: Gary Hollingshead, Feb 4, 2010
  Update: GetName has been removed as the card is passed around and one can just use it,
    Shuffle() has be implemented and should take care of any card that is in the discard
    pile, DrawCard() has been changed to only draw cards that are in the deck and then 
    add the person who drew it to the location. There is one thing that isn't handled, and
    that is if you search the deck and no cards are in the deck, you will shuffle the deck.
    However, if there are no cards in the discard pile, an infinite loop is garrented.

  Updater: Gary Hollingshead, Mar 1, 2010
  UpDate: Trimmed stuff up, including the called functions of the cards and changed
    the shuffle to include a card that says if the deck is empty. Also added a shufflediscard
    deck.

  Updater: Gary Hollingshead, Mar 8, 2010
  Update: Added named indexing for indexes used by the class
"""

import random
import SelectCard
import copy

class Deck:

    def __init__(self, name):
        self.ILocations = 5
        self.IName = 0
        self.IMemoryAddress = 0
        self.IDeckName = 1
        self.ICardPile = 2
        self.IFunction = 4
        self.IIndexCardList = 6
        self.Name = name
        self.CardList = []
        self.OrderList = []
        self.Bad = ["No cards to draw", "No cards to draw", "Dummy.jpg", "Dummy2.jpg", self.BadCard, [self, self.Name, "Deck"], -1]
#Two lists, the cardlist keeps track of the cards. This list never changes so the card always knows where it is. The second list, 
#orderlist, keeps an index into the card list. Using this second list, we can shuffle the numbers around and randomize the order 
#of the the cards without ever messing with them. The name just keeps track of the name of the deck, and the bad is a dummy card
# to be called when the deck is empty and there are no cards to draw



    def AddCard(self, Card):
        NewCard = copy.copy(Card)
        NewCard[self.IIndexCardList] = len(self.CardList)
        NewCard[self.ILocations] = [self, self.Name, "Deck"]
        self.CardList.append(NewCard)
        self.OrderList.append((len(self.CardList) - 1))
#This puts the index of the card in the card, and then sets its location. It puts the card on the cardlist and adds the index to 
#that card, which is always the end of the list



    def Shuffle(self):
        random.shuffle(self.OrderList)
#Uses the random library to shuffle a list... not much to it



    def ShuffleDiscard(self):
        Counter = 0 
        while (Counter < len(self.OrderList)):
            if (self.CardList[Counter][ILocations][self.ICardPile] == "Discard"):
                self.CardList[Counter][ILocations][self.ICardPile] = "Deck"
            Counter += 1
        self.Shuffle
#This goes through the list of cards and "returns" any card that has a location of "discard" to the "deck", and then calls shuffle


    def DrawCard(self, DrawnBy, CardName="none"):
        if(type(DrawnBy != "str") and CardName == "none"):
            if(DrawnBy.Type == "Player"):
                #If it is a player drawing the card.  Check for specials
                if(self.Name == "Common" and DrawnBy.Name == "Bob Jenkins"):
                    card1 = self.DrawCardInternal(DrawnBy, "none")
                    card2 = self.DrawCardInternal(DrawnBy, "none")
                    ans = SelectCard.browseList("Choose a card to draw",[card1, card2])
                    if(ans == card1):
                        self.DiscardCard(card2)
                    else:
                        self.DiscardCard(card1)
                    return ans
                elif(self.Name == "Unique" and DrawnBy.Name == "Monterey Jack"):
                    card1 = self.DrawCardInternal(DrawnBy, "none")
                    card2 = self.DrawCardInternal(DrawnBy, "none")
                    ans = SelectCard.browseList("Choose a card to draw",[card1, card2])
                    if(ans == card1):
                        self.DiscardCard(card2)
                    else:
                        self.DiscardCard(card1)
                    return ans
                elif(self.Name == "Skill" and DrawnBy.Name == "Amanda Sharpe"):
                    card1 = self.DrawCardInternal(DrawnBy, "none")
                    card2 = self.DrawCardInternal(DrawnBy, "none")
                    ans = SelectCard.browseList("Choose a card to draw",[card1, card2])
                    if(ans == card1):
                        self.DiscardCard(card2)
                    else:
                        self.DiscardCard(card1)
                    return ans
                elif(self.Name == "Spell" and DrawnBy.Name == "Dexter Drake"):
                    card1 = self.DrawCardInternal(DrawnBy, "none")
                    card2 = self.DrawCardInternal(DrawnBy, "none")
                    ans = SelectCard.browseList("Choose a card to draw",[card1, card2])
                    if(ans == card1):
                        self.DiscardCard(card2)
                    else:
                        self.DiscardCard(card1)
                    return ans
                elif((self.Name == "Common" or self.Name == "Unique" or self.Name == "Spell")
                     and DrawnBy.Name == "Ashcan Pete"):
                    card1 = self.DrawCardInternal(DrawnBy, "none")
                    card2 = self.DrawDiscardCard(DrawnBy, "none")
                    if(card2[0] == "No cards to draw"):
                        return card1
                    else:
                        ans = SelectCard.browseList("Choose a card to draw",[card1, card2])
                        if(ans == card1):
                            self.DiscardCard(card2)
                        else:
                            self.DiscardCard(card1)
                        return ans
        return self.DrawCardInternal(DrawnBy, CardName)
                    
                
    def DrawCardInternal(self, DrawnBy, CardName):
        Name = CardName
        Counter = 0
        Location = self.CardList[self.OrderList[Counter]][self.ILocations][self.ICardPile]
        if(CardName != "none"):
            Name = self.CardList[self.OrderList[Counter]][self.IName]
        while (Location != "Deck" or Name != CardName):
            Counter += 1
            if (Counter == (len(self.OrderList))):
                return self.Bad
            Location = self.CardList[self.OrderList[Counter]][self.ILocations][self.ICardPile]
            if(CardName != "none"):
                Name = self.CardList[self.OrderList[Counter]][self.IName]
        self.CardList[self.OrderList[Counter]][self.ILocations][self.ICardPile] = DrawnBy
        RCard = self.CardList[self.OrderList[Counter]]
        TempVar = self.OrderList.pop(Counter)
        self.OrderList.append(TempVar)
        #Calls the card on draw function
        print "Drawing: ", RCard[0]
        RCard[self.IFunction](RCard, "draw")
        return copy.copy(RCard)
#First, we go through the deck, in order of the orderlist, and check for a card that is in the "deck". If we don't find one, we
#pass back a dummy card that lets us know there is no free cards in the deck. If we do find one, we change the location to the
#person/thing that drew the card. We then pop that number off the orderlist and put it at the end of the orderlist. Finally,
#we return the card

    def DrawDiscardCard(self, DrawnBy, CardName):
        Name = CardName
        Counter = 0
        Location = self.CardList[self.OrderList[Counter]][self.ILocations][self.ICardPile]
        if(CardName != "none"):
            Name = self.CardList[self.OrderList[Counter]][self.IName]
        while (Location != "Discard" or Name != CardName):
            Counter += 1
            if (Counter == (len(self.OrderList))):
                return self.Bad
            Location = self.CardList[self.OrderList[Counter]][self.ILocations][self.ICardPile]
            if(CardName != "none"):
                Name = self.CardList[self.OrderList[Counter]][self.IName]
        self.CardList[self.OrderList[Counter]][self.ILocations][self.ICardPile] = DrawnBy
        RCard = self.CardList[self.OrderList[Counter]]
        TempVar = self.OrderList.pop(Counter)
        self.OrderList.append(TempVar)
        #Calls the card on draw function
        print "Drawing: ", RCard[0]
        RCard[self.IFunction](RCard, "draw")
        return copy.copy(RCard)



    def UseCard(self, UCard, usage="use"):
        UCard[self.IFunction](UCard, usage)



    def DiscardCard(self, DCard, usage="discard"):
        DCard[self.IFunction](DCard, usage)
#these two functions just call function associated with the card, and pass it either "use" or "discard" to indicate
#weither or not it is being used or discarded, however, due to some cards needing a bit of flexiblilty, a card can be 
#called with something other then use or discard



    def BadCard(self, Card, Use):
        print Card[0]
        print Card[2]

