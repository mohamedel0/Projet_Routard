

# -*- coding: utf-8 -*-
"""
Created on Fri May 15 01:16:04 2020

@author: mohamed
"""

from operator import itemgetter
import math
import random
from priority_dict import priority_dict 


################################## GRAPHES ###############################


graphe1= {
     'a': {'b': 2, 'c':3 , 'd': 31},
     'b': {'a':2 , 'd':9 , 'c':3 , 'e':7 , 'f' : 1},
     'c': {'b':3 , 'f': 10 },
     'd': {'a': 31, 'b' : 9 , 'e': 20 },
     'e': {'d': 20 , 'b' : 7 ,'f': 18}, 
     'f': {'b': 1 , 'c': 10  , 'e' : 18} 
    }


graphe2={
     'a': {'b': 4 , 'c': 2 , 'd': 10},
     'b': {'a':4 , 'c': 7 , 'd': 1},
     'c': {'a': 2 ,'b':7   , 'd': 3},
     'd': {'a': 10 , 'b' : 1 , 'c': 3  },
     }




################################### PRIM #################################


def Prim (G) :
    F= priority_dict() #une file F
    PERE=priority_dict() # une file PERE 
    sommetsG=list(G.keys()) #liste des sommets du graphe
    r=random.choice(sommetsG) # on affecte à r   un choix aletoire a partir de notre liste de sommets
    for u in sommetsG : 
        F[u]=math.inf # on affecte l'infini a tous les sommets de notre graphe
    
    F[r] = 0  #on affecte la clé (poids) 0 à notre racine
    PERE[r]='' #on affectte '' à son pere (pere de r) 

    
    while F : #tant que notre file est non-vide
       
        u=F.pop_smallest() # on retourne le minimum de F et on le supprime de notre file F
        
        
        for v in list(G[u].keys()): # ici on s'interesse aux adjacents de  u (touts les adjacents)
            if v in F and G[u][v] < F[v]: # si l'adjacent est à l'interieur de notre F et la distance entre u et v est inferieur strictement à la clé de v (poids de v )
                PERE[v]=u # pere de v devient u (en mettant bien sur dans notre file PERE qu on a déclaré au debut)
                F[v]= G[u][v] # puis la clé de v (poids) devient la distance entre u et v
    print('Sommet racine:', r)
    
    return PERE #on retourne notre file PERE qui contient les sommets avec leur peres 

#Prim(graphe1)



########################### DJIKSTRA #####################################
    



def Djikstra (G, si, sf) : #ma fonction prend en parametre un graphe et un sommet intial et un sommet final dont j ai besoin dans routard
    F=priority_dict()
    P={}
    sq=[]    
    
    sommetsG=list(G.keys()) #liste des sommets
    for u in sommetsG :
        F[u]= math.inf
        P[u]=''
    F[si] = 0 # on affecte au sommet initial la valeur 0
    while F: #tant que F est non vide
        min=F.smallest() # on affecte à min le plus petit element de notre File F
        poidsMin=F[min] #le poids de notre min
        F.pop_smallest() #on extrait le minimum de F 
        sommetsMin=list(G[min].keys()) # liste de sommets d'adjacents de min 
        for v in sommetsMin: # pour chaque éléments dans sommetsMin
            poidsArrete=G[min][v] #poids entre min (sommet ayant le poids minimu) et  v 
            if v in F and F[v] > poidsArrete + poidsMin : #RELACHER
                F[v] = poidsArrete + poidsMin
                P[v] = min
    sommet = sf # on affecte au variable sommet  sf
    while sommet != si: # tant que sommet ( sommet final) different de si (sommet initiale)
        sq.insert(0,sommet) # inserer à la premiere position sommet  dans la sequence sq
        sommet=P[sommet] # la variable sommet prend comme valeur le pere de notre sommet
    sq.insert(0,si) #insere à la premiere position si dans la sequence sq
    
    return sq # on retourne notre sequence (sq)

#Djikstra(graphe1 , 'a' , 'd')
    

########################## PREFIXE ##############################
    

    
def Prefixe(F): #j'explique ce que fait mon programme prefixe :  de base prim  retourne une file (sommet , pere )
#ensuite prefixe transforme cette file en ( sommet , liste de fils )  
#apres il recupere le sommet initial et il  l'ajoute à la  liste finale et il fais pareil pour les sommets fils jusqu'à ce qu'il  parcours tous les sommets fils

    L=[]
    p={}
    def prefixerec(m): 
        for s in F.keys():
            if s in F.values():
                p[s]= list(itemgetter(*[idx for idx,e in enumerate(list(F.values())) if e == s])(list(F.keys())))
            else:
                p[s]=[]
        if len(p[m])==0:
            L.append(m)
        else:
            L.append(m)
            for k in range (len(p[m])):
                for i in [p[m][k]]:
                    prefixerec(i)
        return L
    for s in F.keys():
        if len(F[s]) == 0:
            return prefixerec(s)
        
#Prefixe(Prim(graphe1))




################################# ROUTARD ####################################

def RoutardApprox(G):
     T = Prim (G) # on utilise notre fonction Prim car elle renvoie un arbre couvrant de poids minimum dont on a besoin
     rho=Prefixe(T) # on effectue prefixe sur notre arbre T (écrit dans le sujet)
     sigma=[]
     sigma.append(rho[0])# on ajoute à un notre liste sigma le premier élément de la séquence retournée par l'application de la fonction préfixe sur T
     
     for j in range(0,len(rho)-1): #pour chaque élément de rho allant de 0 jusqu'a n-1 ( nombre de sommets - 1)
         mu=Djikstra(G,rho[j],rho[j+1]) # on calcule le plus court chemin de j (sommet initiale ) à j+1 (sommet final) grace à notr fonction Djikstra
         mu.pop(0) # retirer le premier élément de mu (la séquence retournée par djikstra)
         sigma.extend(mu) # ajouter mu à la fin de sigma
         
     mu= Djikstra(G, rho[-1], rho [0]) # on calcule le plus court chemin entre le dernier et le premier éléments de rho
     mu.pop(0)  #retirer le premier élément de mu (la séquence retournée par djikstra)
     sigma.extend(mu)# ajouter mu à la fin de sigma
     
     print ('Sequence:', sigma)


     return sigma 
    
RoutardApprox(graphe1)
