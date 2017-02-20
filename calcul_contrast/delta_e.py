#!/usr/bin/python
# -*- coding: utf-8 -*-
# PHONOCHROME :
# Colorize graphemes and calculate sets of contrasted colors using multiples Open Source libraries (Phonetisaurus, OpenFST,GoogleNgram, Colormaths, colorsys)
# 
# > Ce programme permet de trouver un set de couleur contrasté sur la base d'une ressource de couleur existante ainsi que d'un fichier de ressource ngram
#	au format arpa
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
import sys
import webcolors
from collections import OrderedDict
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor
from colormath.color_conversions import convert_color
from datetime import datetime

# Note : les emplacements des fichiers sont définis en partant de l'emplacement du main.py
# Fonction permettant facilement de passer du format hexadécimal aux valeurs R,G,B d'une couleur
def rgb_to_hex(red, green, blue):
	    """Return color as #rrggbb for the given color values."""
	    return '#%02x%02x%02x' % (red, green, blue)

def calc_contrast_delta_e(ressource_couleur,ngram_arpa,delta_e):

	# Nom des fichiers en entrée tels que reçus par la fonction
	nom_res_sans_ext=ressource_couleur
	nom_ngram_sans_ext=ngram_arpa
	# Nom des fichiers complets
	nom_res_complet=ressource_couleur+".txt"
	nom_ngram_complet=ngram_arpa+".arpa"
	# Emplacement du fichier d'entrée de ressources de couleur
	emplacement_res_couleur="config_couleur/"
	# Emplacement du fichier d'entrée de ressources de bigram au format ARPA
	emplacement_res_ngram="config_ngram/"
	# Nom du dossier où le nouveau fichier de ressources de couleur sera créé
	emplacement_fichier_sortie="output_couleur/"
	# Delta E à atteindre pour chaque couleurs et ses contextes droits les plus fréquents
	delta_e_goal=int(delta_e)
	# Déclaration du premier dictionnaire qui contiendra les ressources de couleur en entrée
	dic_pho={}
	# Déclaration de différentes variables utiles pour la suite du traitement
	bigram_match=""
	dic_pho_color={}
	dic_nouv_coul_contrast={}
	# servira à compter le nombre d'opérations nécessaires (test de couples de couleurs) avant de trouver un set de couleur contrasté
	cpt_nbr_operations=0
	# Si ces valeurs sont à "True" alors durant le test de couple de couleurs les valeurs seront augmentés de 1, sinon elles sont à "False" alors elles seront réduites de 1
	increase_r=True
	increase_g=True
	increase_b=True

	# On ouvre le fichier contenant les ressources de couleur
	# L'utilisation de l'encodage UTF8 SANS BOM est conseillée, les marques BOM aillant causé des problèmes durant la lecture du fichier de ressource de couleur
	fichier_ressource_couleur = open(emplacement_res_couleur+nom_res_complet,'r',encoding='utf_8')
	print("\n\tEtape 1 : Mise en mémoire du fichier de ressource de couleurs.")
	print("\tTraitement...")
	for ligne in fichier_ressource_couleur:
		# On traite seulement les lignes qui ne commencent pas par une marque '#' de commentaire
		if (re.search('^#',ligne)):
			pass
		else:
			# Ce 'try' permet nottament d'éliminer les erreurs suite à la présence d'une marque BOM invisible
			try:
				# on sépare les couleurs des phonèmes en splitant sur =>
				split_pho_couleur=ligne.split("=>")
				pho_ressource=split_pho_couleur[0]
				hex_color=split_pho_couleur[1]

				# Si le caractère | est trouvé, c'est que le phonème est une diphtongue, on traite les diphtongue seulement à la fin de ce fichier (en concaténant les nouvelles couleurs des phonèmes qui la compose)
				if(re.search("\|",hex_color)):
					pass
				else:
					# on transpose la couleur hexadécimal en RGB grace à la fonction correspondante
					trans_hex_to_rgb=webcolors.hex_to_rgb(hex_color)
					# on passe d'un tuple à un string afin de pouvoir la traiter
					rgb_tuple_to_string=str(trans_hex_to_rgb)
					# on sélectionne seulement les chiffres contenus dans cette couleur
					get_number=re.findall("\d+\.\d+|\d+|\d+\.\d+",rgb_tuple_to_string)
					# on associe une lettre en variable à chaque valeur de couleur qui constituent un code RGB
					r=int(get_number[0])
					g=int(get_number[1])
					b=int(get_number[2])
					# on les convertis en pourcentage pour pouvoir utiliser le toolkit de conversion Colormaths par la suite
					r_percent=r/255
					g_percent=g/255
					b_percent=b/255
					# on transpose la couleur RGB en couleur de l'espace LAB
					rgb = sRGBColor(r_percent,g_percent,b_percent)
					lab = convert_color(rgb, LabColor)
					# on insère ces nouvelles données dans un tableau avec en clé le phonème et en valeur la couleur LAB correspondante
					dic_pho[pho_ressource]=lab
			except:
				pass
	# on ferme le fichier de ressource
	fichier_ressource_couleur.close()
	print("\tFin de la mise en mémoire des ressources.")

	# on ouvre le fichier de bigram de phonème au format ARPA
	fichier_ngram_phoneme = open(emplacement_res_ngram+nom_ngram_complet,'r',encoding='utf_8')
	print("\n\tEtape 2 : Traitement du fichier de bigram, calcule de la distance entre chaque couleur des phonèmes du corpus." )
	print("\tTraitement...")
	for ligne in fichier_ngram_phoneme:
		# on sélectionne uniquement les lignes traitant de bigram, et non celles de 1gram, 3gram, 4gram etc...
		pattern="(.*)\t(.*)\s(.*)\t(.*)"
		if (re.match(pattern,ligne)):
			# on supprime les retours à la ligne
			bigram_match=ligne.strip("\n")
			# on isole les phonèmes dans ces bigram
			split_bigram_pho=re.split("\t|\s",bigram_match)
			# on attribut une variable à ces phonèmes afin de pouvoir plus facilement les traiter par la suite
			pho_a = split_bigram_pho[1]
			pho_b = split_bigram_pho[2]
			# on va chercher la couleur correspondant à ces phonèmes dans le tableau créé précédemment
			color_pho_a=dic_pho.get(pho_a,"UNK")
			color_pho_b=dic_pho.get(pho_b,"UNK")
			# on ne traite que les phonèmes dont la couleur est présente dans le fichier de ressource de couleur
			if(color_pho_a != "UNK" and color_pho_b != "UNK"):
				# le delta E est une mesure de distance entre plusieurs couleurs qui comprend plusieurs méthodes et applications, dans ce programme nous
				# allons utiliser le delta E CMC 2000 qui est celui utilisé actuellement en infographie et dans l'industrie de plusieurs secteurs
				
				# on calcule le delta E entre ces deux couleurs
				calc_delta_e = delta_e_cie2000(color_pho_a, color_pho_b, Kl=1, Kc=1, Kh=1)
				# on associe la couleur du phonème a en valeur à son phonème correspondant en clé d'un nouveau tableau
				dic_pho_color[pho_a]=color_pho_a
				# si la distance Delta E est inférieure à celle fixée par l'utilisateur, on commence la recherche d'une nouvelle couleur
				if (calc_delta_e < delta_e_goal):
					# on transforme le code couleur LAB du phonème A en string pour pouvoir le traiter par la suite
					str_col_a = str(color_pho_a)
					# on recherche les chiffres présent dans ce code couleur
					x=re.findall("\d+\.\d+|\d+|-\d+\.\d+",str_col_a)
					# on incrémente la variable qui gardera une trace du dernier calcule de Delta E avec la valeur du premier calcul du delta E
					new_calc_delta = calc_delta_e
					# on converti les int en float
					new_lab_l=float(x[0])
					new_lab_a=float(x[1])
					new_lab_b=float(x[2])
					# on fixe les valeurs minimales et maximales de chaque future valeur RGB à respectivement 0 et 255
					# R
					r_min=0
					r_max=255
					# G
					g_min=0
					g_max=255
					# B
					b_min=0
					b_max=255
					# on reconvertis les valeurs LAB en RGB pour pouvoir faire des test sur les valeurs RGB, plus facilement manipulables que les valeurs LAB
					new_lab = LabColor(new_lab_l,new_lab_a,new_lab_b)
					new_rgb = convert_color(new_lab, sRGBColor)
					# on défini le nouveau code RGB à tester
					rgb_a_tester=str(new_rgb)
					# comme précédemment, on récupèr les valeurs R G et B dans la string precedemment créé
					trouver_val_rgb=re.findall("\d+\.\d+|\d+|-\d+\.\d+",rgb_a_tester)
					# on reconvertit les string en float
					new_r_float=float(trouver_val_rgb[0])
					new_g_float=float(trouver_val_rgb[1])
					new_b_float=float(trouver_val_rgb[2])
					# on convertit les float en int pour pouvoir les incrémenter plus facilement par la suite
					r_a_tester=int(new_r_float*255)
					g_a_tester=int(new_g_float*255)
					b_a_tester=int(new_b_float*255)
					# tant que le delta E n'est pas atteind on effectue les calculs suivants pour R, G ou B :
					# si il est supérieur à 0 et inférieur à 255 on commence par l'incrémenter de 1 et sauvegarde la nouvelle valeur
					# dès qu'il atteint son maximum on arrête de l'incrémenter et on le réduit à chaque test de 1
					# le tout se répéte à chaque couleur tant que le Delta E n'est pas satisfait
					while new_calc_delta < delta_e_goal:
						# Couleur R :
						if (increase_r == True):
							if (r_a_tester >= r_min and r_a_tester < r_max):
								r_a_tester=r_a_tester+1
							elif(r_a_tester >= r_max):
								r_a_tester=r_a_tester-1
								increase_r=False
						elif (increase_r == False):
							if (r_a_tester <= r_max and r_a_tester > r_min):
								r_a_tester=r_a_tester-1
							elif(r_a_tester <= r_min):
								r_a_tester=r_a_tester+1
								increase_r=True
						# Couleur G :
						if (increase_g == True):
							if (g_a_tester >= g_min and g_a_tester < g_max):
								g_a_tester=g_a_tester+1
							elif((g_a_tester >= g_max)):
								g_a_tester=g_a_tester-1
								increase_g=False

						elif (increase_g == False):
							if (g_a_tester <= g_max and g_a_tester > g_min):
								g_a_tester=g_a_tester-1
							elif(g_a_tester <= g_min):
								g_a_tester=g_a_tester+1
								increase_g=True
						# Couleur B :
						if (increase_b == True):
							if (b_a_tester >= b_min and b_a_tester < b_max):
								b_a_tester=b_a_tester+1
							elif((b_a_tester >= b_max)):
								b_a_tester=b_a_tester-1
								increase_b=False
						elif (increase_b == False):
							if (b_a_tester <= b_max and b_a_tester > b_min):
								b_a_tester=b_a_tester-1
							elif(b_a_tester <= b_min):
								b_a_tester=b_a_tester+1
								increase_b=True
						# On passe les nouvelles valeurs RGB en pourcentages pour pouvoir les convertir dans l'espace LAB
						x=r_a_tester/255
						y=g_a_tester/255
						z=b_a_tester/255
						# on convertis le nouveau RGB ainsi créé
						rgb_nouveau = sRGBColor(x,y,z)
						new_color_1 = convert_color(rgb_nouveau, LabColor)
						# on test cette couleur avec celle du phonème b en contexte droit du bigram
						new_calc_delta = delta_e_cie2000(new_color_1, color_pho_b, Kl=1, Kc=1, Kh=1)
						# on compte le nombre d'opérations pour l'afficher par la suite
						cpt_nbr_operations=cpt_nbr_operations+1
						# si le delta E est atteint avec ces nouvelles valeurs on sauvegarde dans un nouveau tableau la nouvelle couleur, sinon on recommence le traitement depuis le début
						if new_calc_delta >= delta_e_goal:
							new_best_color_a = new_color_1
							dic_pho_color[pho_a]=new_best_color_a
							dic_nouv_coul_contrast[pho_a]=new_best_color_a
	# une fois le traitement fini on ferme le fichier de bigram
	fichier_ngram_phoneme.close()
	print("\tFin du calcul des nouvelles couleurs contrastées. Nombre de combinaisons de couleurs testées :",cpt_nbr_operations)
	print("\n\tEtape 3 : création du fichier de ressource final")
	print("\tTraitement...")
	# on fusionne les deux dictionnaire : le premier (plus anciens) de ressource de couleur et le deuxième contenant les nouvelles valeurs, ceci afin de conserver les valeurs qui n'ont pas été modifiées
	fusion_dic1_dic2 = {}
	fusion_dic1_dic2.update(dic_pho)
	fusion_dic1_dic2.update(dic_nouv_coul_contrast)
	# ouverture d'un autre dictionnaire qui sera utile par la suite
	dic3={}
	# on ouvre de nouveau le fichier de couleur
	fichier_ressource_couleur = open(emplacement_res_couleur+nom_res_complet,'r',encoding='utf_8')
	# on répété le même traitement qu'au début du programme pour les ressources de couleur mais cette fois-ci pour les diphtongues avec les valeurs nouvellement calculées
	# en effet on considère ici les diphtongues comme une concaténation de plusieurs caractères et non comme des phonèmes à part entières, elles doivent ainsi prendre les
	# valeurs de couleurs nouvellement calculées
	for elements in fichier_ressource_couleur:
		# on saute les lignes qui sont des commentaires
		if (re.search('^#',elements)):
			pass
		else:
			try:
				# on recherche la marque | indiquant une diphtongue
				if(re.search("\|",elements)):
					# on sépare les phonèmes des codes couleurs sur le symbole '=>'
					get_diph=elements.split("=>")
					get_two_pho=list(get_diph[0])
					get_two_colors=get_diph[1].split("|")
					# on associe la nouvelle couleur correspondant à chaque diphtongue trouvé dans le dictionnaire contenant les valeurs fraichement calculés
					color_diph_a=fusion_dic1_dic2.get(get_two_pho[0],"UNK")
					color_diph_b=fusion_dic1_dic2.get(get_two_pho[1],"UNK")
					# on insére le tout dans un nouveau dictionnaire qui sera utile par la suite
					dic3[get_two_pho[0]+get_two_pho[1]]=str(color_diph_a)+"|"+str(color_diph_b)
			except:
				pass 
	# on referme le fichier de ressource de couleur
	fichier_ressource_couleur.close()
	# on met à jour le dictionnaire contenant les couleurs precedemment calculés avec les valeurs des diphtongues
	fusion_dic1_dic2_dic3={}
	fusion_dic1_dic2_dic3.update(fusion_dic1_dic2)
	fusion_dic1_dic2_dic3.update(dic3)
	# on tri le dictionnaire ainsi créé
	fusion_dic1_dic2_dic3=OrderedDict(fusion_dic1_dic2_dic3)
	# on associe au nom du nouveau fichier de ressources de couleurs sa date de création
	temps=datetime.now().strftime('%d-%m-%Y_%H-%M')
	# création du fichier de ressource de couleur contrasté
	nouveau_fichier_ressource = open(emplacement_fichier_sortie+"nouveau_set_couleur_"+temps+".txt",'w',encoding='utf_8')
	# on affiche quelques commentaires en début de fichier
	nouveau_fichier_ressource.write('# Set de couleur le plus contrasté possible pour chaque phonèmes suivant son contexte droite le plus fréquent\n')
	nouveau_fichier_ressource.write('# modèle :\n')
	nouveau_fichier_ressource.write('# phonème en API => code hexadécimal correspondant\n')
	nouveau_fichier_ressource.write('# ou phonème (diphtongue) en API> => code hexadécimal correspondant 1|code hexadécimal 2\n')
	nouveau_fichier_ressource.write('# (dans ce fichier les lignes démarrant par "#" ne sont pas prises en compte par le programme)\n')
	nouveau_fichier_ressource.write('#\n')
	# on ouvre le dictionnaire à jour contenant les nouvelles valeurs de chaque phonème et des diphtongues
	for phonemes in fusion_dic1_dic2_dic3:
		color_test=fusion_dic1_dic2_dic3.get(phonemes,"UNK")
		# on ne traite dans cette partie que les diphtongues
		if len(phonemes)>1 :
			if (re.search('\|',str(color_test))):
				if(re.search('UNK',str(color_test))):
					pass
				else:
					# toute la prochaine partie du traitement de ce 'else' va consister à :
					# convertir les valeurs LAB en RGB de chaque phonème trouvé,
					# convertir les valeurs RGB en hexadécimal
					# sauvegarder le résultat dans le nouveau fichier de ressource de couleur
					get_the_diph=str(color_test).split("|")
					diph1_color=get_the_diph[0]
					diph2_color=get_the_diph[1]

					trouver_chiffres_diph1=re.findall("\d+\.\d+|\d+|-\d+\.\d+",diph1_color)
					trouver_chiffres_diph2=re.findall("\d+\.\d+|\d+|-\d+\.\d+",diph2_color)

					LabColor_diph1= LabColor(trouver_chiffres_diph1[0],trouver_chiffres_diph1[1],trouver_chiffres_diph1[2])
					LabColor_diph2= LabColor(trouver_chiffres_diph2[0],trouver_chiffres_diph2[1],trouver_chiffres_diph2[2])

					diph1_couleur_rgb=convert_color(LabColor_diph1, sRGBColor)
					diph2_couleur_rgb=convert_color(LabColor_diph2, sRGBColor)

					diph_1_str_rgb=str(diph1_couleur_rgb)
					diph_2_str_rgb=str(diph2_couleur_rgb)

					trouver_chiffres_diph1=re.findall("\d+\.\d+|\d+|-\d+\.\d+",diph_1_str_rgb)
					trouver_chiffres_diph2=re.findall("\d+\.\d+|\d+|-\d+\.\d+",diph_2_str_rgb)

					diph_1_rgb_r=float(trouver_chiffres_diph1[0])
					diph_1_rgb_g=float(trouver_chiffres_diph1[1])
					diph_1_rgb_b=float(trouver_chiffres_diph1[2])
					diph_2_rgb_r=float(trouver_chiffres_diph2[0])
					diph_2_rgb_g=float(trouver_chiffres_diph2[1])
					diph_2_rgb_b=float(trouver_chiffres_diph2[2])

					diph_1_rgb_r_255=(diph_1_rgb_r*255)
					diph_1_rgb_g_255=(diph_1_rgb_g*255)
					diph_1_rgb_b_255=(diph_1_rgb_b*255)
					diph_2_rgb_r_255=(diph_2_rgb_r*255)
					diph_2_rgb_g_255=(diph_2_rgb_g*255)
					diph_2_rgb_b_255=(diph_2_rgb_b*255)

					diph_1_rgb_int_r=int(diph_1_rgb_r_255)
					diph_1_rgb_int_g=int(diph_1_rgb_g_255)
					diph_1_rgb_int_b=int(diph_1_rgb_b_255)
					diph_2_rgb_int_r=int(diph_2_rgb_r_255)
					diph_2_rgb_int_g=int(diph_2_rgb_g_255)
					diph_2_rgb_int_b=int(diph_2_rgb_b_255)
					diph_1_couleur_hex=rgb_to_hex(diph_1_rgb_int_r,diph_1_rgb_int_g,diph_1_rgb_int_b)
					diph_2_couleur_hex=rgb_to_hex(diph_2_rgb_int_r,diph_2_rgb_int_g,diph_2_rgb_int_b)
					nouveau_fichier_ressource.write(phonemes+'=>'+diph_1_couleur_hex+"|"+diph_2_couleur_hex+'\n')
					nouveau_fichier_ressource.write("# rgb("+str(diph_1_rgb_int_r)+','+str(diph_1_rgb_int_g)+','+str(diph_1_rgb_int_b)+")"+"|"+"rgb("+str(diph_2_rgb_int_r)+','+str(diph_2_rgb_int_g)+','+str(diph_2_rgb_int_b)+")"+"\n")
					nouveau_fichier_ressource.write("#\n")
		else:
			# idem pour les phonèmes 'simples', on va convertir les valeurs de couleur LAB en RGB, puis en hexadécimal et sauvegarder le tout dans le fichier de résultat
			couleur_lab=fusion_dic1_dic2_dic3.get(phonemes,"UNK")
			couleur_rgb = convert_color(couleur_lab, sRGBColor)
			str_rgb=str(couleur_rgb)

			trouver_chiffres=re.findall("\d+\.\d+|\d+|-\d+\.\d+",str_rgb)

			rgb_r=float(trouver_chiffres[0])
			rgb_g=float(trouver_chiffres[1])
			rgb_b=float(trouver_chiffres[2])

			rgb_r_255=(rgb_r*255)
			rgb_g_255=(rgb_g*255)
			rgb_b_255=(rgb_b*255)

			rgb_int_r=int(rgb_r_255)
			rgb_int_g=int(rgb_g_255)
			rgb_int_b=int(rgb_b_255)

			couleur_hex=rgb_to_hex(rgb_int_r,rgb_int_g,rgb_int_b)

			nouveau_fichier_ressource.write(phonemes+'=>'+couleur_hex+'\n')
			nouveau_fichier_ressource.write("# rgb("+str(rgb_int_r)+','+str(rgb_int_g)+','+str(rgb_int_b)+")"+"\n")
			nouveau_fichier_ressource.write("#\n")

	# on ferme le fichier de ressource une dernière fois, marquant la fin du traitement.
	nouveau_fichier_ressource.close()
	print("\tFin de l'enregistrement du nouveau fichier de ressource de couleurs.")
	print("\n\tLe fichier de ressource contrasté est disponible dans le dossier /"+emplacement_fichier_sortie+" sous le nom de 'nouveau_set_couleur' suivi de sa date de création.txt")