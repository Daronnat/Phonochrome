# -*- coding: utf-8 -*-
# PHONOCHROME :
# Colorize graphemes and calculate sets of contrasted colors using multiples Open Source libraries (Phonetisaurus, OpenFST,GoogleNgram, Colormaths, colorsys)
# 
# > Ce programme est un main aillant pour but de faciliter la manipulations des différents utilitaires qui constituent Phonochrome
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
import os
from tools.arpa_vers_api import arpa_vers_api
from tools.sampa_vers_api import sampa_vers_api
from tools.espace_entre_caracteres import espaces_entre_carac
from tools.recup_phoneme import recup_phoneme
from calcul_contrast.delta_e import calc_contrast_delta_e
import subprocess

print("\n*******************************************************************************************************************")
print("***                                               PHONOCHROME 1.0                                               ***")
print("***                  Projet Professionel - Master 2 IdL - Université Grenoble Alpes - 2016/2017                 ***")
print("***                                    Créé par Elena Melnikova et Sylvain Daronnat                             ***")
print("*******************************************************************************************************************")
print("\n")

# Variable contrôlant le choix fait par l'utilisateur
res_menu=0

while res_menu!=10:
	print("\n*******************************************************************************************************************\n")
	print("Veuillez sélectionner une option en choisissant le numéro correspondant et en appuyant sur 'entrée':\n")
	print("\n *** UTILITAIRES : ***\n")
	print("\t 1 - Importer un corpus au format de l'alphabet phonétique ARPABET")
	print("\t 2 - Importer un corpus au format de l'alphabet phonétique SAMPA")
	print("\t 3 - Séparer les lignes d'un fichier par des espaces")
	print("\t 4 - Récupérer uniquement la colonne des phonèmes d'un corpus déjà normalisé")
	print("\n *** TRAITEMENT DES RESSOURCES DE COULEUR & MODELES DE LANGUE : ***\n")
	print("\t 5 - Calculer de nouvelles couleurs contrastées sur la base d'un fichier de ressource de couleurs")
	print("\t 6 - Création d'un nouveau modèle de langue")
	print("\t 7 - Préparation de fichiers de ngram nécessaires pour le calcul de nouvelles couleurs (avec GoogleNgramLibrary)")
	print("\t 8 - Fusion de fichiers ngram nécessaires pour le calcul de nouvelles couleurs (avec GoogleNgramLibrary)")
	print("\n\t 10 - Quitter le programme")

	res_menu=int(input("? - "))

	if res_menu==1:
		# Lancement du script de normalisation arpabet vers API
		print(" [1] Importation d'un corpus qui est en alphabet phonétique ARPABET.")
		print(" RAPPEL : un corpus en entrée doit toujours être formaté suivant ce modèle : mot (tabulation) p h o n e m e s")
		print(" Exemple pour le mot 'abacco' en anglais : abaco	æ b ʌ k oʊ")
		print(" Insérez votre fichier au format TXT dans le dossier '/import_corpus' et entrez le nom de ce fichier sans préciser l'extension.")
		nom_fichier=input(" Exemple : entrez 'test' si le fichier s'appelle 'test.txt'. Ensuite appuyez sur 'entrée' \n>")
		arpa_vers_api(nom_fichier)
		
	elif res_menu==2:
		# Lancement du script de normalisation sampa vers API
		print(" [2] Importation d'un corpus qui est en alphabet phonétique SAMPA.")
		print(" RAPPEL : un corpus en entrée doit toujours être formaté suivant ce modèle : mot (tabulation) p h o n e m e s.")
		print(" Exemple pour le mot 'abacco' en anglais : abaco	æ b ʌ k oʊ.")
		print(" NOTES : ce script a été conçu spécialement pour le SAMPA de lexique.org, il se peut qu'il ne soit pas adapté à tous les types de SAMPA.")
		print(" Insérez votre fichier au format TXT dans le dossier '/import_corpus' et entrez le nom de ce fichier sans préciser l'extension.")
		nom_fichier=input(" Exemple : entrez 'test' si le fichier s'appelle 'test.txt'. Ensuite appuyez sur 'entrée' \n>")
		sampa_vers_api(nom_fichier)

	elif res_menu==3:
		# Lancement du script de normalisation sampa vers API
		print(" [3] Séparation des lignes d'un fichier par des espaces.")
		print(" Ce petit utilitaire a pour simple fonction de séparer les caractères d'une ligne par des espaces.")
		print(" Ceci peut s'avérer utile pour formater un texte. Il est à noter que tous les caractères d'une même ligne recevront le même traitement.")
		print(" NOTES : les marques de tabulation et de retour à la ligne sont conservées, un éditeur de texte peut vous aider à les remplacer par ce que vous préférez.")
		print(" Insérez votre fichier au format TXT dans le dossier '/import_corpus' et entrez le nom de ce fichier sans préciser l'extension.")
		nom_fichier=input(" Exemple : entrez 'test' si le fichier s'appelle 'test.txt'. Ensuite appuyez sur 'entrée' \n>")
		espaces_entre_carac(nom_fichier)

	elif res_menu==4:
		# Lancement du script de récupération de la colonne des phonèmes d'un corpus
		print(" [4] Récupération des phonèmes d'un corpus correctement formaté.")
		print(" RAPPEL : un corpus en entrée doit toujours être formaté suivant ce modèle : mot (tabulation) p h o n e m e s.")
		print(" Exemple pour le mot 'abacco' en anglais : abaco	æ b ʌ k oʊ.")
		print(" Insérez votre fichier au format TXT dans le dossier '/import_corpus' et entrez le nom de ce fichier sans préciser l'extension.")
		nom_fichier=input(" Exemple : entrez 'test' si le fichier s'appelle 'test.txt'. Ensuite appuyez sur 'entrée' \n>")
		recup_phoneme(nom_fichier)

	elif res_menu==5:
		# Lancement du script de calcul de contraste utilisant la distance delta E
		print(" [5] Calcule de nouvelles couleurs constrastées.")
		print(" Ici vous pourrez lancer le calcul d'un nouveau set de couleur contrasté sur la base d'une ressource de couleurs existante.")
		print(" NOTES : Pour que ce script fonctionne, assurez vous d'avoir toutes les dépendances nécessaires (voir manuel).")
		print(" le fichier de ressource de couleurs doit comprendre par ligne :")
		print(" - un symbole API suivit d'une flèche '=>' et d'une couleur au format hexadécimal pour les phonèmes simple")
		print(" - ou deux couleurs séparés d'un '|' pour les diphtongues. Exemple : ʊ=>#AE9A91 ou tʃ=>#BB2970|#019BCF")
		print(" Le fichier d'entrée pourra contenir des commentaires ou des informations annexes mais le début de ces lignes devra alors commencé par '#'.")
		print(" Le fichier de couleurs constrastées produit en sortie suivra ce même modèle mais avec en plus les couleurs au format RGB en commentaire.")
		print("\n Insérez votre fichier de ressource de couleur au format TXT dans le dossier '/config_couleur' et entrez le nom de ce fichier sans préciser l'extension.")
		nom_fichier_couleur=input(" Exemple : entrez 'test' si le fichier s'appelle 'test.txt'. Ensuite appuyez sur 'entrée' \n>")
		nom_fichier_ngram_arpa=input(" Insérez votre fichier de ressource de couleur au format ARPA dans le dossier '/config_ngram' et entrez le nom de ce fichier sans préciser l'extension.\n>")
		delta_e=input(" Indiquez l'objectif du Delta-E à atteindre (attention, une valeur trop haute peut être impossible à atteindre)\n>")
		calc_contrast_delta_e(nom_fichier_couleur,nom_fichier_ngram_arpa,delta_e)

	elif res_menu==6:
		# Entrainer un nouveau modèle de langue
		print(" [6] Constitution d'un nouveau modèle de langue.")
		print(" Ici vous pourrez ici créer un nouveau modèle de langue, peu importe quelle langue vous voulez traiter.")
		print(" NOTES : Pour que ce script fonctionne, assurez vous d'avoir toutes les dépendances nécessaires (voir manuel).")
		print(" Le corpus en entrée doit être formaté de la façon suivante : mot (tabulation) p h o n e m e s.")
		print(" Exemple pour le mot 'abacco' en anglais : abacco	æ b ʌ k oʊ.")
		print("\n Insérez votre fichier de ressource de couleur au format TXT dans le dossier '/import_corpus' et entrez le nom de ce fichier sans préciser l'extension.")
		nom_fichier=input(" Exemple : entrez 'test' si le fichier s'appelle 'test.txt'. Ensuite appuyez sur 'entrée' \n>")
		res_menu=0
		print("\n\t 1/3 - Alignement des graphies et des phonèmes du fichier à traiter...\n")
		cmd_1="phonetisaurus-align --input=import_corpus/"+nom_fichier+".txt --ofile=output_lang/"+nom_fichier+".corpus --seq1_del=false"
		process1 = subprocess.Popen(cmd_1.split(), stdout=subprocess.PIPE)
		process1.wait()
		print("\n\t 2/3 - Créations des statistiques ngram du corpus...\n")
		cmd_2="estimate-ngram -o 8 -t output_lang/"+nom_fichier+".corpus -wl output_lang/"+nom_fichier+".arpa"
		process2 = subprocess.Popen(cmd_2.split(), stdout=subprocess.PIPE)
		process2.wait()
		print("\n\t 3/3 - Création du modèle de langue final...\n")
		cmd_3="phonetisaurus-arpa2wfst --lm=output_lang/"+nom_fichier+".arpa --ofile=output_lang/"+nom_fichier+".fst"
		process3 = subprocess.Popen(cmd_3.split(), stdout=subprocess.PIPE)
		process3.wait()
		print(" Traitement terminé !")
		print(" Le fichier est disponible dans le dossier '/output_lang' sous le nom de "+nom_fichier+".fst")
		print(" Pour pouvoir l'utiliser avec Phonochrome V1 veuillez créer un dossier nommé "+nom_fichier+"\n dans le répertoire /res de Phonochrome et insérez le fichier "+nom_fichier+".fst dans ce même dossier,\n le fichier apparaitra alors dans les choix de colorisation possibles sur Phonochrome.")
		
	elif res_menu==7:
		# Créer les fichiers qui serviront à constituer un fichier de ngram au format ARPA permattant de calculer de nouvelles couleurs contrastées
		print(" [7] Préparation d'un fichier ngram .CNTS, étape nécessaire pour le calcul de nouvelles couleurs.")
		print(" Cette étape sert à créer un fichier de ngram qui servira de base au calcule de nouvelles couleurs contrastées.")
		print(" NOTES : cette étape nécessite en entrée un corpus comportant uniquement des phonèmes en API où les différents phonèmes sont séparés par des espaces.")
		print(" Exemple pour le mot 'abacco' en anglais : æ b ʌ k oʊ ")
		print("\n Insérez le fichier à traiter au format TXT dans le dossier '/import_corpus' et entrez le nom de ce fichier sans préciser l'extension.")
		nom_fichier=input(" Exemple : entrez 'test' si le fichier s'appelle 'test.txt'. Ensuite appuyez sur 'entrée' \n>")
		res_menu=0
		print("\n\t 1/3 - Génération de la table des symboles du fichier...\n")
		cmd_1="ngramsymbols < import_corpus/"+nom_fichier+".txt > output_lang/"+nom_fichier+".syms"
		process1 = subprocess.Popen(cmd_1, stdout=subprocess.PIPE, shell=True)
		process1.wait()
		print("\n\t 2/3 - Compilation de la table des symboles et du corpus en entrée...\n")
		cmd_2='farcompilestrings -unknown_symbol="<unk>" -symbols=output_lang/'+nom_fichier+'.syms -keep_symbols=1 import_corpus/'+nom_fichier+'.txt > output_lang/'+nom_fichier+'.far'
		process2 = subprocess.Popen(cmd_2, stdout=subprocess.PIPE, shell=True)
		process2.wait()
		print("\n\t 3/3 - Génération du fichier .CNTS...\n")
		cmd_3="ngramcount -order=5 output_lang/"+nom_fichier+".far > output_lang/"+nom_fichier+".cnts"
		process3 = subprocess.Popen(cmd_3, stdout=subprocess.PIPE, shell=True)
		process3.wait()
		print(" Traitement terminé !")
		print(" Le fichier CNTS est disponible dans le dossier '/output_lang' sous le nom de "+nom_fichier+".cnts")
		print(" Vous pouvez désormais l'utiliser avec l'option numéro 8 pour fusionner plusieurs de ces fichiers afin de créer une nouvelle ressource de ngram\n nécessaire durant création d'un fichier de ressource de couleur contrasté")

	elif res_menu==8:
		print(" [8] Fusion de fichiers .CNTS, et création du fichier ngram au format ARPA.")
		print(" Cette étape sert à créer un fichier de ngram qui servira de base au calcule de nouvelles couleurs contrastées.")
		print(" NOTES : cette étape nécessite en entrée un fichier .CNTS que vous pouvez créer à partir d'un corpus de phonème réalisable à partir de l'option numéro 7.")
		print("\n Insérez les fichiers à traiter à l'extension CNTS dans le dossier '/import_corpus' et entrez le nom de ces fichier sans préciser l'extension.")
		nom_fichier1=input(" Exemple : entrez 'test' si le fichier s'appelle 'test.cnts'. Ensuite appuyez sur 'entrée'. Insérez le nom du premier fichier CNTS\n>")
		nom_fichier2=input(" Insérez le nom du deuxième fichier CNTS\n>")
		print("\n\tFusion des deux fichiers en cours...")
		cmd_1="ngrammerge import_corpus/"+nom_fichier1+".cnts import_corpus/"+nom_fichier2+".cnts > output_lang/"+nom_fichier1+"_"+nom_fichier2+".merged"
		process1 = subprocess.Popen(cmd_1, stdout=subprocess.PIPE, shell=True)
		process1.wait()
		print(" Fusion terminée, le fichier est disponible dans le dossier output_lang/"+nom_fichier1+"_"+nom_fichier2+".merged")
		arpa=input(" Voulez-vous créer un fichier ARPA à partir du nouveau fichier que vous venez de créer ? Ce fichier servira de ressource au script de calcule de couleurs contrastées\n si vous n'avez pas fusionné tous les corpus que vous voulez utiliser vous pouvez sauter cette étape\n(Y/N)>")
		if arpa == 'Y' or arpa == 'y' or arpa == 'oui' or arpa == 'yes' or arpa == 'YES':
			cmd_2="ngrammake output_lang/"+nom_fichier1+"_"+nom_fichier2+".merged > output_lang/world.mod"
			print("\n\tCompilation du fichier créé par la fusion précédente...")
			process2 = subprocess.Popen(cmd_2, stdout=subprocess.PIPE, shell=True)
			process2.wait()
			print("\n\tCréation du fichier au format ARPA utile pour le calcule de contraste...")
			cmd_3='ngramprint --ARPA output_lang/world.mod > output_lang/world.ARPA'
			process3 = subprocess.Popen(cmd_3, stdout=subprocess.PIPE, shell=True)
			process3.wait()
			print("\nTraitement terminé, le fichier est disponible dans le dossier /output_lang sous le nom de 'world.ARPA'")
			res_menu==0
		else:
			res_menu==0

			