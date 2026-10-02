from random import shuffle
import gc
def Blackjack(PlayerList=[],Strategy=[],HandList=[],decks=0):
    while len(PlayerList)<=1:
        print(f"Invalid player count, please input a valid number of players.")
        try:
            players=int(input("How many players are there?\n"))
        except:
            pass
    while len(HandList)!=len(PlayerList) and len(HandList)!=0:
        print(f"Invalid hands, please input a valid number of hands.")
        try:
            HandList=int(input("what are the hands?\n"))
        except:
            pass
    while decks<=0 or float(decks)!=decks:
        print(f"Invalid deck count, please input a valid number of decks.")
        try:
            decks=int(input("How many decks are there?\n"))
        except:
            pass
    global PlayerCount
    global DeckCount
    PlayerCount=len(PlayerList)
    DeckCount=decks
    players=PlayerList
    global PlayerOrder
    global hands
    global scores
    global statuses
    global PlayerOddsTable
    global AI
    start="Y"
    while start!="N":
        print(HandList)
        PlayerOrder={}
        hands={}
        scores={}
        statuses={}
        PlayerOddsTable={}
        AI={}
        Setup(players,PlayerCount,Strategy,HandList)
        game(players)
def Setup(players=[],PlayerCount=0,Strategy="",HandList=[]):
    for order in range(0,PlayerCount):
        PlayerOrder[players[order]]=order
        hands[players[order]]=HandList[order] #Issue here or downstream
        scores[players[order]]=Score(HandList[order])
        statuses[players[order]]="active"
        PlayerOddsTable[players[order]]=[]
        AI[players[order]]=Strategy[order]
def game(players=[]):
    global deck
    global Round
    global Mystery
    global MysteryCard
    deck=Deck()
    NumberOfCards=[]
    for player in players:
        NumberOfCards.append(len(hands[player]))
        for card in hands[player]:
            (deck.deck).remove(card)
            (deck.cards)[[card][0]]=(deck.cards)[[card][0]]-1
    Round=max(NumberOfCards)
    deck.shuffle()
    global status
    status="uncertain"
    while status=="uncertain":
        Round+=1
        for player in players:
            if len(hands[player])<Round:
                if statuses[player]=="active":
                    if Round>2:
                        if player=="dealer" and Round==3:
                            hands[player].append(MysteryCard)
                            Mystery=0
                            del MysteryCard
                        CurrentOdds(player,PlayerOrder)
                        move=Move(player)
                        if move=="Hit":
                            statuses[player]="active"
                        if move=="Stay":
                            statuses[player]="inactive"
                    if statuses[player]=="active":
                        if player=="dealer" and Round==2:
                            MysteryCard=deck.dealCard()
                            Mystery=1
                        else:
                            card=deck.dealCard()
                            hands[player].append(card)
                            # print(HandList) incorrect
                scores[player]=Score(hands[player])
                if scores[player]>21:
                    statuses[player]="inactive"
                    print(f"{player} busted.")
                status="Concluded"
                for name in players:
                    if len(hands[name])>=Round-1 and (len(hands[name])>=Round or player!="dealer") or statuses[name]=="inactive":
                        print(f"{name}'s hand: {hands[name]}\t{name}'s score: {Score(hands[name])}")
                    else:
                        print(f"{name}'s hand: {hands[name]},[???,???]\t{name}'s score: {Score(hands[name])}+???")
        for player in players:
            if statuses[player]=="active" and scores["dealer"]<=21:
                status="uncertain"
                
    offset=0
    for player in players:
        if player!="dealer":
            if scores[player]<=21 and scores["dealer"]<=21:
                if scores[player]>scores["dealer"]:
                    print(f"dealer scored {scores['dealer']} but {player} scored more with {scores[player]}, {player} wins.")
                    statuses[player]="Victory"
                    offset-=1
                if scores[player]==scores["dealer"]:
                    print(f"{player} and dealer both scored {scores[player]}, they tied.")
                    statuses[player]="Tie"
                if scores[player]<scores["dealer"]:
                    print(f"{player} only scored {scores[player]} while the dealer scored higher with {scores['dealer']}, dealer wins.")
                    statuses[player]="Defeat"
                    offset+=1
            elif scores[player]<=21:
                print(f"dealer busted with a score of {scores['dealer']}, {player} wins")
                statuses[player]="Victory"
                offset-=1
            else:
                print(f"{player} scored {scores[player]} and busted.")
                statuses[player]="Defeat"
                offset+=1
    if offset>0:
        statuses["dealer"]="Victory"
        print(f"The dealer has {offset} more wins than losses, dealer wins.")
    if offset==0:
        statuses["dealer"]="Tie"
        print(f"The dealer has the same number of wins as losses.")
    if offset<0:
        statuses["dealer"]="Defeat"
        print(f"The dealer has {-offset} more losses than wins, dealer loses.")  
    start=input(f"Would you like to play again?\n Y or N:")
    while start!="N" and start!="Y":
        start=input("{start} is not an answer. Y or N:")
    if start=="N":
        print(f"Thanks for playin, please come again.")


def Score(hand=[]):
    score=0
    above=0
    for card in hand:
        if card[0] in ["2","3","4","5","6","7","8","9","10"]:
            score+=int(card[0])
        elif card[0] in ["J","Q","K"]:
            score+=10
        elif card[0]in ["A"]:
            score+=11
            above+=1
        else:
            score+=card[0]
    while score>21 and above>0:
        score-=10
        above-=1
    return(score)

def CardOdds(card="",CardsTaken=0):
#     print(deck.cards[card],len(deck.deck),CardsTaken,Mystery)
    return(deck.cards[card]/(len(deck.deck)-CardsTaken))

def TurnsTillPlayer(player="",target=""):
    turns=0
    running=1
    while running==1:
        for players in PlayerOrder:
            if PlayerOrder[players]==PlayerOrder[player] and statuses[players]=="active":
                if players==target:
                    running=0
                else:
                    turns+=1
        for players in PlayerOrder:
            if PlayerOrder[players]>PlayerOrder[player] and statuses[players]=="active":
                if players==target:
                    running=0
                else:
                    turns+=1
        for players in PlayerOrder:
            if PlayerOrder[players]<PlayerOrder[player] and statuses[players]=="active":
                if players==target:
                    running=0
                else:
                    turns+=1
        running=0
    return(turns)

def BustedOdds(player=""):
    current=0
    if Score(hands[player])>21:
        current=1
    return(current)

def BustsOdds(player=""): 
    New=0
    if player!="dealer": #Given they hit
        for card in deck.cards:
            hands[player].insert(-1,[card])
            if Score(hands[player])>21:
                New+=CardOdds(card) #Need to find odds when we know that a certain card must have disappeared
            try:
                hands[player].remove([card])
            except:
                pass
    if player=="dealer" and Score(hands[player])<17 and Mystery==0:
        for card in deck.cards:
            hands[player].insert(-1,[card])
            if Score(hands[player])>21:
                New+=CardOdds(card)
            try:
                hands[player].remove([card])
            except:
                pass
    if player=="dealer" and Mystery==1:
        for Dcard1 in deck.cards:
            Odds1=CardOdds(Dcard1)
            hands[player].insert(-1,[Dcard1])
            deck.cards[Dcard1]-=1
            if Score(hands[player])<17:
                for Dcard2 in deck.cards:
                    hands[player].insert(-1,[Dcard2])
                    Odds2=CardOdds(Dcard2,1)
                    if Score(hands[player])>21:
                        New+=Odds1*Odds2
                    try:
                        hands[player].remove([Dcard2])
                    except:
                        pass
            deck.cards[Dcard1]+=1
            try:
                hands[player].remove([Dcard1])
            except:
                pass
    return(New)

def OddsIfStays(player=""):
    PlayerStaysAheadOdds=0
    PlayerStaysTiedOdds=0
    PlayerStaysBehindOdds=0
    if player!="dealer" and Mystery==0:
        if Score(hands[player])>Score(hands["dealer"]):
            PlayerStaysAheadOdds+=1
        if Score(hands[player])==Score(hands["dealer"]):
            PlayerStaysTiedOdds+=1
        if Score(hands[player])<Score(hands["dealer"]):
            PlayerStaysBehindOdds+=1
    elif player!="dealer" and Mystery==1:
        for Dcard in deck.cards:
            Odds1=CardOdds(Dcard)
            hands["dealer"].insert(-1,[Dcard])
            if Score(hands[player])>Score(hands["dealer"]):
                PlayerStaysAheadOdds+=Odds1
            if Score(hands[player])==Score(hands["dealer"]):
                PlayerStaysTiedOdds+=Odds1
            if Score(hands[player])<Score(hands["dealer"]):
                PlayerStaysBehindOdds+=Odds1
            try:
                hands["dealer"].remove([Dcard])
            except:
                pass
    return(PlayerStaysAheadOdds,PlayerStaysTiedOdds,PlayerStaysBehindOdds)

def OddsIfStay(player=""): #Given dealer hit
    PlayerStayAheadOdds=0
    PlayerStayTiedOdds=0
    PlayerStayBehindOdds=0
    if player!="dealer" and Mystery==0: #Stay Regardless of Bust
        if Score(hands["dealer"])<17:
            for Dcard in deck.cards:
                hands["dealer"].insert(-1,[Dcard])
                if Score(hands[player])>Score(hands["dealer"]):
                    PlayerStayAheadOdds+=CardOdds(Dcard)
                if Score(hands[player])==Score(hands["dealer"]):
                    PlayerStayTiedOdds+=CardOdds(Dcard)
                if Score(hands[player])<Score(hands["dealer"]):
                    PlayerStayBehindOdds+=CardOdds(Dcard)
                try:
                    hands["dealer"].remove([Dcard])
                except:
                    pass
        else:
            if Score(hands[player])>Score(hands["dealer"]):
                PlayerStayAheadOdds+=1
            if Score(hands[player])==Score(hands["dealer"]):
                PlayerStayTiedOdds+=1
            if Score(hands[player])<Score(hands["dealer"]):
                PlayerStayBehindOdds+=1
    elif player!="dealer" and Mystery==1:
        for Dcard1 in deck.cards:
            Odds1=CardOdds(Dcard1)
            hands["dealer"].insert(-1,[Dcard1])
            deck.cards[Dcard1]-=1
            if Score(hands["dealer"])<17:
                for Dcard2 in deck.cards:
                    Odds2=CardOdds(Dcard2,1)
                    hands["dealer"].insert(-1,[Dcard2])
                    if Score(hands[player])>Score(hands["dealer"]):
                        PlayerStayAheadOdds+=Odds1*Odds2
                    if Score(hands[player])==Score(hands["dealer"]):
                        PlayerStayTiedOdds+=Odds1*Odds2
                    if Score(hands[player])<Score(hands["dealer"]):
                        PlayerStayBehindOdds+=Odds1*Odds2
                    try:
                        hands["dealer"].remove([Dcard2])
                    except:
                        pass
            else:
                if Score(hands[player])>Score(hands["dealer"]):
                    PlayerStayAheadOdds+=Odds1
                if Score(hands[player])==Score(hands["dealer"]):
                    PlayerStayTiedOdds+=Odds1
                if Score(hands[player])<Score(hands["dealer"]):
                    PlayerStayBehindOdds+=Odds1
            deck.cards[Dcard1]+=1
            try:
                hands["dealer"].remove([Dcard1])
            except:
                pass
    return(PlayerStayAheadOdds,PlayerStayTiedOdds,PlayerStayBehindOdds)

def OddsIfHits(player=""):
    PlayerHitsAheadOdds=0
    PlayerHitsTiedOdds=0
    PlayerHitsBehindOdds=0
    if player!="dealer" and Mystery==0:
        for Hcard in deck.cards:
            hands[player].insert(-1,[Hcard])
            if Score(hands[player])>Score(hands["dealer"]):
                PlayerHitsAheadOdds+=CardOdds(Hcard)
            if Score(hands[player])==Score(hands["dealer"]):
                PlayerHitsTiedOdds+=CardOdds(Hcard)
            if Score(hands[player])<Score(hands["dealer"]):
                PlayerHitsBehindOdds+=CardOdds(Hcard)
            try:
                hands[player].remove([Hcard])
            except:
                pass
    if player!="dealer" and Mystery==1:
        for Hcard in deck.cards:
            Odds1=CardOdds(Hcard)
            hands[player].insert(-1,[Hcard])
            deck.cards[Hcard]-=1
            for Dcard in deck.cards:
                Odds2=CardOdds(Dcard,1)
                hands["dealer"].insert(-1,[Dcard])
                if Score(hands[player])>Score(hands["dealer"]):
                    PlayerHitsAheadOdds+=Odds1*Odds2
                if Score(hands[player])==Score(hands["dealer"]):
                    PlayerHitsTiedOdds+=Odds1*Odds2
                if Score(hands[player])<Score(hands["dealer"]):
                    PlayerHitsBehindOdds+=Odds1*Odds2
                try:
                    hands["dealer"].remove([Dcard])
                except:
                    pass
            deck.cards[Hcard]+=1
            try:
                hands[player].remove([Hcard])
            except:
                pass
    return(PlayerHitsAheadOdds,PlayerHitsTiedOdds,PlayerHitsBehindOdds)

def OddsIfHit(player=""): #Given they hit
    PlayerHitAheadOdds=0
    PlayerHitTiedOdds=0
    PlayerHitBehindOdds=0
    if player!="dealer" and Mystery==0:
        for Hcard in deck.cards: #Hit Regardless of Bust
            Odds1=CardOdds(Hcard)
            hands[player].insert(-1,[Hcard])
            deck.cards[Hcard]-=1
            if Score(hands["dealer"])<17:
                for Dcard in deck.cards:
                    Odds2=CardOdds(Dcard,1)
                    hands["dealer"].insert(-1,[Dcard])
                    if Score(hands[player])>Score(hands["dealer"]):
                        PlayerHitAheadOdds+=Odds1*Odds2 #CardsTaken=len(players)-PlayerOrder[player]
                    if Score(hands[player])==Score(hands["dealer"]):
                        PlayerHitTiedOdds+=Odds1*Odds2
                    if Score(hands[player])<Score(hands["dealer"]):
                        PlayerHitBehindOdds+=Odds1*Odds2
                    try:
                        hands["dealer"].remove([Dcard])
                    except:
                        pass
            else:
                if Score(hands[player])>Score(hands["dealer"]):
                    PlayerHitAheadOdds+=Odds1
                if Score(hands[player])==Score(hands["dealer"]):
                    PlayerHitTiedOdds+=Odds1
                if Score(hands[player])<Score(hands["dealer"]):
                    PlayerHitBehindOdds+=Odds1
            deck.cards[Hcard]+=1        
            try:
                hands[player].remove([Hcard])
            except:
                pass
    if player!="dealer" and Mystery==1:
        for Hcard in deck.cards: #Hit Regardless of Bust
            Odds1=CardOdds(Hcard)
            hands[player].insert(-1,[Hcard])
            deck.cards[Hcard]-=1
            if Score(hands["dealer"])<17:
                for Dcard1 in deck.cards:
                    Odds2=CardOdds(Dcard1,1)
                    hands["dealer"].insert(-1,[Dcard1])
                    deck.cards[Dcard1]-=1
                    if Score(hands["dealer"])<17:
                        for Dcard2 in deck.cards:
                            Odds3=CardOdds(Dcard2,2)
                            hands["dealer"].insert(-1,[Dcard2])
                            if Score(hands[player])>Score(hands["dealer"]):
                                PlayerHitAheadOdds+=Odds1*Odds2*Odds3 #CardsTaken=len(players)-PlayerOrder[player]
                            if Score(hands[player])==Score(hands["dealer"]):
                                PlayerHitTiedOdds+=Odds1*Odds2*Odds3
                            if Score(hands[player])<Score(hands["dealer"]):
                                PlayerHitBehindOdds+=Odds1*Odds2*Odds3
                            try:
                                hands["dealer"].remove([Dcard2])
                            except:
                                pass
                    else:
                        if Score(hands[player])>Score(hands["dealer"]):
                            PlayerHitAheadOdds+=Odds1*Odds2
                        if Score(hands[player])==Score(hands["dealer"]):
                            PlayerHitTiedOdds+=Odds1*Odds2
                        if Score(hands[player])<Score(hands["dealer"]):
                            PlayerHitBehindOdds+=Odds1*Odds2
                    deck.cards[Dcard1]+=1        
                    try:
                        hands["dealer"].remove([Dcard1])
                    except:
                        pass
            else:
                if Score(hands[player])>Score(hands["dealer"]):
                    PlayerHitAheadOdds+=Odds1
                if Score(hands[player])==Score(hands["dealer"]):
                    PlayerHitTiedOdds+=Odds1
                if Score(hands[player])<Score(hands["dealer"]):
                    PlayerHitBehindOdds+=Odds1
            deck.cards[Hcard]+=1        
            try:
                hands[player].remove([Hcard])
            except:
                pass
    return(PlayerHitAheadOdds,PlayerHitTiedOdds,PlayerHitBehindOdds)

def CurrentOdds(VIP="",PlayerOrder={}):
    PlayerOdds=0
    DealerOdds=0
    PlayerBustedOdds=0
    DealerBustedOdds=0
    PlayerBustsOdds=0
    DealerBustsOdds=0
    PlayerHitsAheadOdds=0
    PlayerHitsTiedOdds=0
    PlayerHitsBehindOdds=0
    PlayerHitAheadOdds=0
    PlayerHitTiedOdds=0
    PlayerHitBehindOdds=0
    PlayerStaysAheadOdds=0
    PlayerStaysTiedOdds=0
    PlayerStaysBehindOdds=0
    PlayerStayAheadOdds=0
    PlayerStayTiedOdds=0
    PlayerStayBehindOdds=0
    for player in PlayerOrder:
        DealerBustedOdds=BustedOdds("dealer")
        DealerBustsOdds=BustsOdds("dealer")
        PlayerBustedOdds=BustedOdds(player)
        PlayerBustsOdds=BustsOdds(player)
        (PlayerHitAheadOdds,PlayerHitTiedOdds,PlayerHitBehindOdds)=OddsIfHit(player)
        (PlayerStayAheadOdds,PlayerStayTiedOdds,PlayerStayBehindOdds)=OddsIfStay(player)
        if player!="dealer" and player==VIP:
            print(DealerBustsOdds)
            PlayerHitWinsOdds=(1-PlayerBustedOdds)*(1-PlayerBustsOdds)*((DealerBustedOdds)+(1-DealerBustedOdds)*((DealerBustsOdds)+(1-DealerBustedOdds)*(1-DealerBustsOdds)*(PlayerHitAheadOdds)))
            PlayerHitTiesOdds=(1-PlayerBustedOdds)*(1-PlayerBustsOdds)*(1-DealerBustedOdds)*(1-DealerBustsOdds)*(PlayerHitTiedOdds)
            PlayerHitLosesOdds=(PlayerBustedOdds)+(1-PlayerBustedOdds)*((PlayerBustsOdds)+(1-PlayerBustsOdds)*(1-DealerBustedOdds)*(1-DealerBustsOdds)*(PlayerHitBehindOdds))
            PlayerStayWinsOdds=(1-PlayerBustedOdds)*((DealerBustedOdds)+(1-DealerBustedOdds)*(DealerBustsOdds)+(1-DealerBustedOdds)*(1-DealerBustsOdds)*(PlayerStayAheadOdds))
            PlayerStayTiesOdds=(1-PlayerBustedOdds)*(1-DealerBustedOdds)*(1-DealerBustsOdds)*(PlayerStayTiedOdds)
            PlayerStayLosesOdds=(PlayerBustedOdds)+(1-PlayerBustedOdds)*(1-DealerBustedOdds)*(1-DealerBustsOdds)*(PlayerStayBehindOdds)
            PlayerOddsTable[player]=[PlayerHitWinsOdds,PlayerHitTiesOdds,PlayerHitLosesOdds,PlayerStayWinsOdds,PlayerStayTiesOdds,PlayerStayLosesOdds]
            print(f"Chance {player} will be winning next turn if they hit: {PlayerHitWinsOdds}\nChance {player} will be tied with the dealer next turn if they hit: {PlayerHitTiesOdds}\nChance {player} will be losing next turn if they hit: {PlayerHitLosesOdds}")
            print(f"Chance {player} will be winning next turn if they stay: {PlayerStayWinsOdds}\nChance {player} will be tied with the dealer next turn if they stay: {PlayerStayTiesOdds}\nChance {player} will be losing next turn if they stay: {PlayerStayLosesOdds}")
            print(f"{player}: {PlayerOddsTable[player]}")
            print()
        
def Move(player=""):
    if AI[player]=="dealer":
        if Score(hands[player])<17:
            return("Hit")
        else:
            return("Stay")
            
    if AI[player]=="winner": #playstyle
        if PlayerOddsTable[player][0]>=PlayerOddsTable[player][3]:
            return("Hit")
        else:
            return("Stay")
        
    if AI[player]=="Tier":
        if PlayerOddsTable[player][1]>=PlayerOddsTable[player][4]:
            return("Hit")
        else:
            return("Stay")
        
    if AI[player]=="loser":
        if PlayerOddsTable[player][2]>=PlayerOddsTable[player][5]:
            return("Hit")
        else:
            return("Stay")

    if AI[player]=="passive": #playstyle
        if 1-PlayerOddsTable[player][2]>PlayerOddsTable[player][2] and PlayerOddsTable[player][5]>0:
            return("Hit")
        else:
            return("Stay")

    if AI[player]=="cautious": #playstyle
        if PlayerOddsTable[player][5]>PlayerOddsTable[player][2]:
            return("Hit")
        else:
            return("Stay")
    
    if AI[player]=="gloryseeker": #playstyle
        if PlayerOddsTable[player][0]>0:
            return("Hit")
        else:
            return("Stay")
    
    if AI[player]=="aggressive": #playstyle
        if PlayerOddsTable[player][2]>0:
            return("Hit")
        else:
            return("Stay")
        

def FutureOdds(player="",DealerHand=[],PlayerCount=0,PotentialCards={},CardsTaken=0):
    print(f"{PlayerCount}")                    
























class Card():
    suits=["\u2663","\u2662","\u2661","\u2660"]
    ranks=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    def value(card,score=0):
        if len(card)>0:
            if card[0] in ["J","Q","K"]:
                return (10)
            elif card[0]!="A" or score>10:
                return (Card.ranks).index(card[0])+1
            else:
                return(11)
    
class Deck():
    def __init__(self):
        self.deck=[]
        self.cards={}
        for rank in Card.ranks:
            self.cards[rank]=0
            for suit in Card.suits:
                for each in range(0,DeckCount):
                    self.deck.append([rank,suit])
                    self.cards[rank]+=1
    def dealCard(self):
        try:
            self.cards[self.deck[-1][0]]-=1
            return((self.deck).pop())
        except:
            print("No more cards left, game over.")
            status="Concluded"
    def shuffle(self):
        shuffle(self.deck)
        
class Hand():
    def showHand(self):
        print(f"{self.name}:",end="\t")
        if self.name!="Dealer" or status!="uncertain":
            self.hand.sort(reverse=True,key=Card.value)
            for card in self.hand:
                print(f"{card[0]}{card[1]}",end="\t")
            print("\n")
        else:
            print(f"{self.hand[-1][0]}{self.hand[-1][1]}")
            print()
         


Blackjack(["Joe","Bob","Dale","dealer"],["aggresive","cautious","cautious","dealer"],[[],[],[],[]],3)

