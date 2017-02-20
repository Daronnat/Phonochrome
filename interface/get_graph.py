#!/usr/bin/python
# -*- coding: utf-8 -*-
# PHONOCHROME :
# Colorize graphemes and calculate sets of contrasted colors using multiples Open Source libraries (Phonetisaurus, OpenFST,GoogleNgram, Colormaths, colorsys)
# 
# > Script en python3 permettant de récupérer les graphies correspondant à chaque phonème d'un texte phonétisé par Phonochrome/Phonetisaurus
#
# Copyright (C) 2017  Elena Melnikova & Sylvain Daronnat - Grenoble Alpes University
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from collections import OrderedDict
import re

# foncton permettant de supprimer les valeurs en double/triple etc... d'un dictionnaire python
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

# Le nom ne comprend pas l'extension du fichier, celle-là doit être ".txt" et sera rajoutée par la suite
nom_fichier_entree ='texte_phonetise'
emplacement_sortie_phonochrome="/var/www/html/phonochrome/output/"

# ouverture du dictionnaire qui contient phonèmes en clés et graphies en valeurs
dic={}

# Ouverture en lecture du fichier traité par phonochrome et en écriture du futur fichier de résutlat
fichier_entree = open(emplacement_sortie_phonochrome+nom_fichier_entree+".txt",'r',encoding='utf-8')
fichier_sortie = open(emplacement_sortie_phonochrome+nom_fichier_entree+'.liste_graphies.txt','w',encoding='utf-8')

for ligne in fichier_entree:
	# on sépare les différents couples phonème/graphèmes
	list_couple=ligne.split(",")
for line in list_couple:
	# on supprime l'indication d'espilon (du vide) car non utile pour la suite
	ligne_clean=line.strip('##::##')
	# on supprime le | indiquant que plus caractères correspondent au même phonème
	ligne_clean = ligne_clean.replace("|", "")
	# on sépare les phonèmes des graphies
	list_graph_pho=ligne_clean.split("::")
	try:
		# dans le dictionnaire dic, si en clé le phonème n'existe pas il est créé et la graphie correspondante rajoutée en valeur, sinon si il existe on lui rajoute la nouvelle valeur
		graph=list_graph_pho[0]
		pho=list_graph_pho[1]
		if pho in dic:
			dic[pho]+=","+graph
		else:
			dic[pho]=graph
	except:
		pass	

# On écrit dans le fichier de résultat un message donnant une brêve explication sur le fichier créé
fichier_sortie.write("# Ce fichier contient la liste de toutes les graphies par phonème d'après le texte d'entrée suivant :"+"\n")
fichier_sortie.write("# "+nom_fichier_entree+"\n")

# on traite le dictionnaire afin de supprimer les graphies en double ou triple etc... pour chaque phonème en clé 
for elem in dic:
	values_dic=dic.get(elem)
	split_values_dic=values_dic.split(",")
	clean_dupli=remove_duplicates(split_values_dic)
	graphem_no_dupli_trait=str(clean_dupli)
	graphem_no_dupli=re.sub("\[|\]|'| |\"","",graphem_no_dupli_trait)

	# on sauvegarde les nouveaux résultats dans le fichier de résultat
	fichier_sortie.write(elem+" => "+graphem_no_dupli+"\n")

# on ferme le fichier d'entrée et de sortie
fichier_entree.close()
fichier_sortie.close()