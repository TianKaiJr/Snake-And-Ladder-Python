import os
import random
import networkx as nx # type: ignore
from termcolor import colored  # type: ignore

class SnakeNLadder:
    ladders={4:14,8:30,28:76,21:42,50:67,71:92,80:99}
    snakes={62:18,97:78,95:56,88:24,48:26,36:6,32:10}
    lkey=list(ladders.keys())
    skey=list(snakes.keys())

    print(colored('SNAKE & LADDER\n','light_magenta'))

    board=[]
    player_travel_path=[]

    def diceboard_graph(self):#diceboard graph type for BFS traversal
        self.diceboard()
        SnL=nx.DiGraph()
        for i in range(99):
            SnL.add_node(i+1)
        for i in range(99):
            SnL.add_edge(i+1,i+2)
        Lkeys=list(self.ladders.keys())
        Lvlas=list(self.ladders.values())
        Skeys=list(self.snakes.keys())
        Svlas=list(self.snakes.values())
        for i in range(len(self.ladders)):
            SnL.add_edge(Lkeys[i],Lvlas[i])
        for i in range(len(self.snakes)):
            SnL.add_edge(Svlas[i],Skeys[i])
        self.BFS_Traversal_Node_1to100(SnL)

    def BFS_Traversal_Node_1to100(self,SnL):
        shortest_path = nx.shortest_path(SnL, source=1, target=100)
        for node in shortest_path:
             print(node,'-> ',end='')

    def diceboard(self):#buiding the gameboard accordingly
        for i in range(10,0,-1):
            row=[]
            for j in range(i*10 if i%2==0 else (i*10)-9,(i*10)-10 if i%2==0 else (i*10)+1,-1 if i%2==0 else +1):
                row.append(j)
            self.board.append(row)

    def displayboard(self,bold):#display the board
        for i in range(10):
            for j in range(10):
                if bold==self.board[i][j]:
                    print(colored('%3d '% self.board[i][j],'red'),end='')
                else:
                    print('%3d '% self.board[i][j],end='')
            print('')

    def rolldice(self):#roll the dice for next movement 
        dice=random.randrange(1,6+1)
        print(f"Dice Rolled >> {dice}")
        return dice

    def salcalc(self,playerno,result=0,total_moves=0):
        """ calculate the ladder climb, snake swallow and normal movements for the player n"""
        self.diceboard()
        while(result!=100):
            roll='y' if input(colored('Roll the Die? (Press Enter) >>> ','green')) == '' else 'n'
            # os.system('cls')
            if roll=='y':
                if result==0:
                    begin=self.rolldice()
                    if begin!=1:
                        print(colored('Dice != 1','red'))
                        continue
                    elif begin==1:
                        result+=begin
                        total_moves+=1
                        self.player_travel_path.append(result)
                        print('Dice = 1\n',colored('Player Boarded\n','yellow'))
                else:
                    #after boarding
                    dice=self.rolldice()
                    if result+dice >100:#if the dice rolled makes the postion > 100 
                        total_moves+=1
                        continue
                    else:
                        result+=dice
                    total_moves+=1
                    self.player_travel_path.append(result)

                    if result in self.skey:
                        #if snake swallows
                        result=self.snakes[result]
                        self.player_travel_path.append(result)
                    if result in self.lkey:
                        #if ladder available
                        result=self.ladders[result]   
                        self.player_travel_path.append(result)
                    self.displayboard(result)#display the ladder after every update          
            elif roll=='n':
                break
        print(colored('Total Moves of Player %d = %d' % (playerno, total_moves), 'yellow'))
        print('Player Path >> ')
        for i in range(len(self.player_travel_path)):
            print(f"{self.player_travel_path[i]} -> ",end='')


def main():
    pno=int(input('Number of Players = '))
    player_list=['Player '+str(i+1) for i in range(pno)]
    print(player_list)
    player_object_list=[SnakeNLadder() for i in range(pno)]
    for i in range(pno):
        player_object_list[i].salcalc(playerno=i+1)
        print(colored('\nBFS Traversal Shortest Distance','cyan'))
        player_object_list[i].diceboard_graph()

main()