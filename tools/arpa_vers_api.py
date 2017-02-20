#!/usr/bin/python
# -*- coding: utf-8 -*-
# PHONOCHROME :
# Colorize graphemes and calculate sets of contrasted colors using multiples Open Source libraries (Phonetisaurus, OpenFST,GoogleNgram, Colormaths, colorsys)
# 
# > Ce programme est un script de normalisation ARPA vers API, il crée aussi un fichier contenant uniquement les mots en API du corpus en entrée.
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
import re

# Note : les emplacements des fichiers sont définis en partant de l'emplacement du main.py
def arpa_vers_api(nom_fichier):

	# Nom du fichier d'entrée tel que reçu par la fonction
	nom_sans_ext=nom_fichier

	# Emplacement du fichier d'entrée
	emplacement_fichier_entree="import_corpus/"

	# Nom complet du fichier d'entrée
	nom_fichier=nom_fichier+".txt"

	# emplacement du fichier de configuration nécessaire pour l'équivalence arpa/api
	emplacement_fichier_config="config/"

	# nom du fichier d'équivalences entre le format arpa et api
	nom_fichier_equivalences="equiv_arpa_api.txt"

	# nom du fichier où les résultats seront stockés
	emplacement_fichier_sortie="output/"

	# Ouverture des dictionnaires nécessaires au traitement
	dic_arpa_to_api={}

	reverse_dic_arpa_to_api={}

	print("\n\tDébut de la normalisation Arpabet vers API...")
	# Ouverture du fichier de configuration et mise en mémoire des équivalences arpa/api
	ressource_equiv_arpa_api = open(emplacement_fichier_config+nom_fichier_equivalences,'r',encoding='utf-8')

	# On traite chaque ligne ne commçant pas par un "#" qui représente un commentaire ou une information
	for ligne in ressource_equiv_arpa_api:
		if (re.search('^#',ligne)):
			pass # à améliorer, faire l'équivalent de celle en php
		else:
			# on sauvegarde les relations d'équivalence dans un dictionnaire avec en clé l'api et en valeur l'arpa (et on fait l'inverse pour le deuxième dictionnaire)
			split_arpa_api=ligne.strip().split('=>')
			symbole_arpa=split_arpa_api[0]
			symbole_api=split_arpa_api[1]
			dic_arpa_to_api[symbole_api]=symbole_arpa
			reverse_dic_arpa_to_api[symbole_arpa]=symbole_api

	# on ferme le fichier de ressource une fois le traitement terminé
	ressource_equiv_arpa_api.close()

	# On ouvre en lecture le corpus a traité et en écriture les fichier de résultat de normalisation complet + API seulement
	corpus_mot_arpa = open(emplacement_fichier_entree+nom_fichier,'r',encoding='utf-8')
	fichier_norma_api = open(emplacement_fichier_sortie+nom_sans_ext+".train",'w',encoding='utf_8')
	fichier_pho_api_only = open(emplacement_fichier_sortie+nom_sans_ext+".col.api.txt",'w',encoding='utf_8')

	for ligne in corpus_mot_arpa:
		# On isole les éléments à traiter : ici les phonèmes en arpa
		split_corpus_mot_arpa=ligne.strip().split('\t')
		corpus_mot=split_corpus_mot_arpa[0]
		corpus_arpa=split_corpus_mot_arpa[1]
		corpus_split_arpa=corpus_arpa.split(' ')
		fichier_norma_api.write("\n")
		fichier_pho_api_only.write("\n")
		fichier_norma_api.write(corpus_mot.lower()+"\t")

		for nbr_symb_arpa in corpus_split_arpa:
			# on écrit les correspondances trouvées dans un fichier de résultat
			fichier_norma_api.write(reverse_dic_arpa_to_api[nbr_symb_arpa]+" ")
			fichier_pho_api_only.write(reverse_dic_arpa_to_api[nbr_symb_arpa]+" ")

	fichier_norma_api.write("\n")
	fichier_pho_api_only.write("\n")

	# On ferme les différents fichiers ouverts, ceux de résultat et celui du corpus originel
	corpus_mot_arpa.close()
	fichier_norma_api.close()
	fichier_pho_api_only.close()

	print("\n\tFin de la normalisation Arpabet vers API.")
	print("\nLe fichier normalisé au format API et converti en minuscule est disponible dans le dossier "+emplacement_fichier_sortie+" sous le nom de "+nom_sans_ext+".train")
	print("\nLa liste des phonèmes en API de ce fichier est également disponible dans le dossier "+emplacement_fichier_sortie+" sous le nom de "+nom_sans_ext+".col.api.txt")
