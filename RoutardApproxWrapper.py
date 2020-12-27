# -*- coding: utf-8 -*- 


from RoutardApprox import RoutardApprox
import json

if __name__ == "__main__":

	for ficgraphe in ["graphe1.json","graphe2.json","graphe3.json"]:
		with open(ficgraphe, "r", encoding="utf-8") as fichier:
			G = json.load(fichier)

		cycle = RoutardApprox(G)
		