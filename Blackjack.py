#!/usr/bin/env python
# coding: utf-8

# In[8]:


import random 
from IPython.display import clear_output

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        # Note this only happens once upon creation of a new Deck
        self.all_cards = [] 
        for suit in suits:
            for rank in ranks:
                # This assumes the Card class has already been defined!
                self.all_cards.append(Card(suit,rank))
                
    def shuffle(self):
        # Note this doesn't return anything
        random.shuffle(self.all_cards)
        
    def deal_one(self):
        # Note we remove one card from the list of all_cards
        return self.all_cards.pop()    
    
    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.all_cards:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

class Hand:
    
    def __init__(self):
        # A new player has no cards
        self.all_cards = [] 
        self.value = 0
        self.aces = 0
        
    
    def add_cards(self,card):
        self.all_cards.append(card)
        self.value += card.value
        if card.rank ==  'Ace':
            self.aces += 1
            
    def adjust_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    
    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.all_cards:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return deck_comp

class Chips:
    
    def __init__(self):
        self.total = 100
        
    def win(self, bet):
        self.total += bet
        
    def lose(self, bet):
        self.total -= bet
        
    def __str__(self):
        return "Player chips: " + str(self.total)
        


# In[6]:


def show_hand(hand):
    for card in hand.all_cards:
        print(card, end =", ")

def take_bets():
    while True:
        try:
            bet = int(input("How much would you like to bet?"))
            if bet < 1:
                print("Bet has to be 1 chip or more!")
                continue
        except:
            print("Please enter an integer!")
        else:
            print(f"Bet is {bet} chips \n")
            return bet
            break

def take_insurance(bet):
    print("Dealer has an ace top card! Offering insurance")
    while True:
        try:
            insurance = int(input("How much would you like to insure? (Up to half your bet)"))
            if insurance < 1:
                print("Insurance cannot be negative!")
                continue
            if insurance > bet/2:
                print("Insurance cannot be more than half your bet!")
                continue
        except:
            print("Please enter an integer!")
        else:
            print(f"Insurance is {insurance} chips")
            return insurance
            break

def hit(deck, hand):
    card = (deck.deal_one())
    hand.add_cards(card)
    hand.adjust_ace()
    print(f"New card is: {card}")

    
def check_bust(hand):
    if hand.value > 21:
        return True
    else:
        return False

def compare_hands(player, dealer, player_chips, bet):
    print("Comparing hands!")
    print(f"Player hand has: {player}")
    print(f"Dealer hand has: {dealer}")
    if player.value == dealer.value:
        print("Both hands same value, stand-off!")
    if player.value > dealer.value:
        print(f"Player hand has {player.value} and dealer hand has {dealer.value}. Player wins!")
        player_chips.win(bet)
    else:
        print(f"Player hand has {player.value} and dealer hand has {dealer.value}. Dealer wins!")
        player_chips.lose(bet)
        
    
def dealer_peek(dealer, player, bet, insurance, chips, play):
    if dealer.all_cards[0].value == 10:
        print("Peeking hidden card!")
        if dealer.all_cards[1].rank == "Ace":
            print("Hidden card is ace. Dealer natural!")
            if player.value == 21:
                print("Player has natural. It's a stand-off!")
                play = False
            else:
                print("Player does not have a natural. Dealer wins!")
                player_chips.lose(bet)
                play = False
        else:
            print("Dealer does not have a natural. Play resuming.")

    if dealer.all_cards[0].rank == "Ace":
        print("Peeking hidden card!")
        if dealer.all_cards[1].value == 10:
            print(f"Hidden card is {dealer.all_cards[1]}")
            if insurance > 0:
                player_chips.win(insurance*2)
            if player.value == 21:
                print("Player has natural. It's a stand-off!")
                play = False
            else:
                print("Player does not have a natural. Dealer wins!")
                player_chips.lose(bet)
                play = False
        else:
            print("Dealer does not have a natural. Play resuming.")
        
def play_again():
    while True:
        choice = input("Play again? Y or N:")
            
        if choice.lower() == "y":
            choice = True
            clear_output()
            print("Restarting game")
            break
            
        if choice.lower() == "n":
            choice = False
            clear_output()
            print("Ending game")
            break
        
        else:
            print("Wrong option, please enter Y for yes or N for no")
            
    return choice


# In[10]:


play = True
new_deck=Deck()
new_deck.shuffle()

while play:
    player = Hand()
    dealer = Hand()
    

    #players makes bets in chips
    player_chips = Chips()
    bet = take_bets()
    insurance = 0

    player.add_cards(new_deck.deal_one())
    print(f"First player card: {player.all_cards[0]}")
    dealer.add_cards(new_deck.deal_one())
    print(f"First dealer card: {dealer.all_cards[0]}")
    
    if dealer.all_cards[0].rank == "Ace":
        insurance = take_insurance(bet)
  
    player.add_cards(new_deck.deal_one())
    print(f"Second player card: {player.all_cards[1]}")
        
    dealer.add_cards(new_deck.deal_one())
    print("Second dealer card: HIDDEN")

    if (dealer.all_cards[0].value == 10) or (dealer.all_cards[0].rank == "Ace"):
        dealer_peek(dealer, player, bet, insurance, player_chips, play)

    while True:
        choice = input("\nHit or stand (H/S)? H for hit, S for stand: ")
        if choice.lower() == 'h':
            hit(new_deck, player)
            print(f"Player hand has:{player}")
            if check_bust(player):
                print(f"Player hand value is{player.value}")
                print("Player busts!")
                player_chips.lose(bet)
                break
            else:
                continue
        elif choice.lower() == 's':
            print("Player standing, dealer's play")
            break
        else:
            print("Please type H or S for hit or stand!")
    
    if check_bust(player):
        play = play_again()
        continue
        
    print(f"Dealer flipping hidden card, hidden card is {dealer.all_cards[1]}")
    
    if dealer.value >=17:
        print(f"Dealer hand is {dealer.value} points, dealer stands")
        compare_hands(player, dealer, player_chips, bet)
        play = False
            
    while dealer.value < 17:
        print("Dealer hand is less than 17 points, dealer hits")
        hit(new_deck, dealer)
        print(f"Dealer hand: {dealer}")

        if check_bust(dealer):
            print ("Dealer busts, Player wins!")
            player_chips.win(bet)
            play = False
            break
            
        if dealer.value >= 17:
            print(f"Dealer hand is {dealer.value} points, dealer stands")
            compare_hands(player, dealer, player_chips, bet)
            play = False
            break
            
    play = play_again()


# In[ ]:




