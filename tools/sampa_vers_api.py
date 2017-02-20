#!/usr/bin/python
# -*- coding: utf-8 -*-
# PHONOCHROME :
# Colorize graphemes and calculate sets of contrasted colors using multiples Open Source libraries (Phonetisaurus, OpenFST,GoogleNgram, Colormaths, colorsys)
# 
# > Ce programme est un script de normalisation SAMPA vers API, il crée aussi un fichier contenant uniquement les mots en API du corpus en entrée.
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
import collections

# Note : les emplacements des fichiers sont définis en partant de l'emplacement du main.py
def sampa_vers_api(nom_fichier):

	# Nom du fichier d'entrée tel que reçu par la fonction
	nom_sans_ext=nom_fichier

	# Emplacement du fichier d'entrée
	emplacement_fichier_entree="import_corpus/"

	# Nom complet du fichier d'entrée
	nom_fichier=nom_fichier+".txt"

	# Emplacement du dossier de configuration de l'utilitaire
	emplacement_fichier_config="config/"

	# Nom du fichier d'équivalence arpa vers api
	nom_fichier_equivalences="equiv_arpa_api.txt"

	# Nom du dossier où le fichier de résultat sera créé
	emplacement_fichier_sortie="output/"

	# Ouverture des deux dictionnaires qui permettront la réalisation de la conversion
	dic_sampa_to_api={}

	reverse_dic_sampa_to_api={}

	print("\n\tDébut de la normalisation Sampa vers API...")

	# Ouverture du fichier de configuration
	ressource_equiv_sampa_api = open(emplacement_fichier_config+nom_fichier_equivalences,'r',encoding='utf-8')

	# Mise en mémoire de la correspondance des symboles arpa et api
	# Les lignes commençant par "#" ne sont pas prises en compte dans le fichier de ressource
	for ligne in ressource_equiv_sampa_api:
		if (re.search('^#',ligne)):
			pass
		else:
			# on sauvegarde les relations d'équivalence dans un dictionnaire avec en clé l'api et en valeur le sampa (et on fait l'inverse pour le deuxième dictionnaire)
			split_sampa_api=ligne.strip().split('=>')
			symbole_sampa=split_sampa_api[0]
			symbole_api=split_sampa_api[1]
			dic_sampa_to_api[symbole_api]=symbole_sampa
			reverse_dic_sampa_to_api[symbole_sampa]=symbole_api

	# Fermeture du fichier de configuration
	ressource_equiv_sampa_api.close()

	# Ouverture du corpus à traiter ainsi que des fichiers de résultats complet et avec API seulement
	corpus_mot_sampa = open(emplacement_fichier_entree+nom_fichier,'r',encoding='utf-8')
	fichier_norma_api = open(emplacement_fichier_sortie+nom_sans_ext+".train",'w',encoding='utf_8')
	fichier_pho_api_only = open(emplacement_fichier_sortie+nom_sans_ext+".col.api.txt",'w',encoding='utf_8')

	# On sépare le corpus en deux colonnes : mots et phonétique, utile par la suite pour créer deux fichiers de résultat
	for ligne in corpus_mot_sampa:
		split_corpus_mot_sampa=ligne.strip().split('\t')
		corpus_mot=split_corpus_mot_sampa[0]
		corpus_sampa=split_corpus_mot_sampa[1]
		fichier_norma_api.write(corpus_mot.lower()+"\t")

		# On essaye de faire correspondre caractère par caractère les phonèmes car sous le format SAMPA de lexique.org, 1 caractère = 1 phonème
		# Ceci nécessite une bonne segmentation du corpus d'entrée
		for c in corpus_sampa:
			c.strip(" ")
			for keys_sampa in reverse_dic_sampa_to_api:
				m=re.search(keys_sampa,c)
				if m:
					# si l'équivalence existe, on l'imprime dans le nouveau corpus avant de passer au reste
					get_pho_api=reverse_dic_sampa_to_api.get(m.group())
					fichier_norma_api.write(get_pho_api+" ")
					fichier_pho_api_only.write(get_pho_api+" ")

		fichier_norma_api.write("\n")
		fichier_pho_api_only.write("\n")

	# On ferme les fichiers en écriture et lecture
	corpus_mot_sampa.close()
	fichier_norma_api.close()
	fichier_pho_api_only.close()

	print("\n\tFin de la normalisation Sampa vers API.")
	print("\nLe fichier normalisé au format API et converti en minuscule est disponible dans le dossier "+emplacement_fichier_sortie+" sous le nom de "+nom_sans_ext+".train")
	print("\nLa liste des phonèmes en API de ce fichier est également disponible dans le dossier "+emplacement_fichier_sortie+" sous le nom de "+nom_sans_ext+".col.api.txt")
