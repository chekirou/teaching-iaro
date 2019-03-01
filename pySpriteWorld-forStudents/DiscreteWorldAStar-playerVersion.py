# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo
import heapq

import random 
import numpy as np
import sys

# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----
def heuristique(p1, p2):
	(x1, y1) = p1
	(x2, y2) = p2
	return abs(x1-x2) + abs(y1-y2)
class Node:
    def __init__(self,row,col, parent = None,cost=0,depl=None, p= None):
        self.parent = parent
        self.childNodes, self.cost, self.row = [], cost, row
        self.depl = depl
        self.col ,self.imm = col, str(row)+ str(col)
        self.p = p
        self.h = heuristique((row, col), self.p)        
		    
    def AddChild(self, cost,depl): 
        n = Node(self.row + depl[0],self.col + depl[1], self, cost,depl,self.p)
        self.childNodes.append(n)
        return n

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s
	








# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)
	
    init()
    

    
    #-------------------------------
    # Building the matrix
    #-------------------------------
       
           
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
        
    
    #-------------------------------
    # Building the best path with A*
    #-------------------------------
    """ nodeInit = Noeud(p.init,0,None)
    frontiere = [(nodeInit.g+p.h_value(nodeInit.etat,p.but),nodeInit)] 
    reserve = {}        
    bestNoeud = nodeInit
    
    while frontiere != [] and not p.estBut(bestNoeud.etat):              
        (min_f,bestNoeud) = heapq.heappop(frontiere)         
    # Suppose qu'un noeud en réserve n'est jamais ré-étendu 
    # Hypothèse de consistence de l'heuristique
    # ne gère pas les duplicatas dans la frontière
    
        if p.immatriculation(bestNoeud.etat) not in reserve:            
            reserve[p.immatriculation(bestNoeud.etat)] = bestNoeud.g #maj de reserve
            nouveauxNoeuds = bestNoeud.expand(p)            
            for n in nouveauxNoeuds:
                f = n.g+p.h_value(n.etat,p.but)
                heapq.heappush(frontiere, (f,n))              
    # Afficher le résultat                    
    return"""
    print(initStates[0][0])
    racine = Node (initStates[0][0], initStates[0][1], p=goalStates[0])
    frontiere = [(racine.h+racine.cost,racine)]
    reserve = {}
    bestNoeud = racine
    while frontiere != [] and not (bestNoeud.row,bestNoeud.col)==goalStates[0]:              
        (min_f,bestNoeud) = heapq.heappop(frontiere)#comment gerer
        if bestNoeud.imm not in reserve: 
            reserve[bestNoeud.imm] = bestNoeud.cost #maj de reserve
            newNodes = [bestNoeud.AddChild(1, i) for i in [(0,1),(0,-1),(1,0),(-1,0)]]
            for n in newNodes:
                f = n.cost+ n.h
                heapq.heappush(frontiere, (f, n))
    
    if (bestNoeud.row,bestNoeud.col)==goalStates[0]:
        res = []		
        r= bestNoeud
        while(r.parent != None):
            res.append(r.depl)
            r = r.parent
           
      
	

    
    reversed(res)
    print(res)    
    #-------------------------------
    # Moving along the path
    #-------------------------------
        
    # bon ici on fait juste un random walker pour exemple...
    

    row,col = initStates[0]
    #row2,col2 = (5,5)

    for i in range(iterations):
    
    
        x_inc,y_inc = res.pop(0)
        next_row = row+x_inc
        next_col = col+y_inc
        if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=20 and next_col>=0 and next_col<=20:
            player.set_rowcol(next_row,next_col)
            print ("pos 1:",next_row,next_col)
            game.mainiteration()

            col=next_col
            row=next_row

            
        
            
        # si on a  trouvé l'objet on le ramasse
        if (row,col)==goalStates[0]:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print ("Objet trouvé!", o)
            break
        '''
        #x,y = game.player.get_pos()
    
        '''

    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


