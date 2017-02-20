#!/usr/bin/python
# -*- coding: utf-8 -*-
# PHONOCHROME :
# Colorize graphemes and calculate sets of contrasted colors using multiples Open Source libraries (Phonetisaurus, OpenFST,GoogleNgram, Colormaths, colorsys)
# 
# > Ce programme est un petit script permettant simplement de récupérer les phonèmes d'un corpus
# cet utilitaire est conçu pour traiter les corpus construits sur le modèle suivant : mot1 \tabulation p h o n è m es
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
def recup_phoneme(nom_fichier):

	# Nom du fichier tel que reçu par la fonction
	nom_sans_ext=nom_fichier

	# Emplacement du fichier d'entrée
	emplacement_fichier_entree="import_corpus/"

	# Emplacement du résultat de sortie
	emplacement_fichier_sortie="output/"

	# Nom complet du fichier d'entrée
	nom_fichier=nom_fichier+".txt"

	print("\n\tDébut de la séparation de tous les caractères par des espaces.")

	# On ouvre les fichiers en lecture et en écriture
	fichier = open(emplacement_fichier_entree+nom_fichier,'r',encoding='utf_8')
	fichier_ecriture = open(emplacement_fichier_sortie+nom_sans_ext+".col.api.txt",'w',encoding='utf_8')

	# On split sur les tabulation et on sauvegarde l'index[1] dans le fichier de résultat
	for ligne in fichier:
		try:
			split_tab=ligne.split("\t")
			fichier_ecriture.write(split_tab[1]+"\n")
		except:
			pass

	# On ferme les fichiers une fois le traitement fini
	fichier.close()
	fichier_ecriture.close()

	print("\n\tFin du traitement.")
	print("\nLe fichier contenant uniquement les phonème est disponible dans le dossier "+emplacement_fichier_sortie+" sous le nom de "+nom_sans_ext+".col.api.txt")
	