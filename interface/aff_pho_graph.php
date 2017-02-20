<!-- # PHONOCHROME :
# Colorize graphemes and calculate sets of contrasted colors using multiples Open Source libraries (Phonetisaurus, OpenFST,GoogleNgram, Colormaths, colorsys)
# 
# > Cette page permet un affichage des différentes graphies des phonèmes présents dans le dernier texte analysé par Phonochrome
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>. -->
<!DOCTYPE html>
<html lang="fr">
<head>
<title>Phonochrome v1 - Université Grenoble Alpes</title>
<meta charset="utf-8">
<link rel="stylesheet" href="style.css" type="text/css">
</head>
<body>
<div class="wrapper row1">
  <header id="header" class="clear">
    <div id="hgroup">
      <h1><a href="index.php">PHONOCHROME</a></h1>
    </div>
    <nav>
      <ul>
        <li><a href="index.php">Outil de colorisation</a></li>
        <li><a href="aff_pho_graph.php">Phonèmes & Graphies</a></li>
        <li><a href="aff_ressources.php">ressources</a></li>
        <li><a href="a_propos.php">à propos</a></li>
      </ul>
    </nav>
  </header>
</div>
<div class="wrapper row2">
  <div id="container" class="clear">
    <div id="homepage" class="clear">
<h2> II. Affichage des phonèmes et Graphies </h2>
<p> Cette page permet de récupérer les phonèmes, couleurs et graphies correspondant au dernier texte traité par Phonochrome. Il est a noté que :</p>
<ul>
  <li>Le texte traité est le dernier a avoir été analysé par Phonochrome.</li>
  <li>Les phonèmes n'étant pas présent dans le fichier de ressource de couleurs sont notés (UNK) et apparaissent en gris et en italique.</li>
  <li>Les graphies en doublon pour le même phonème sont supprimées.</li>
  <li>Le modèle d'affichage des résultat est le suivant : " PHONEME EN API : GRAPHIE1,GRAPHIE2... "</li>
</ul>

<?php

  // DECLARATION DES VARIABLES DE CHEMIN D'ACCES :
  //
  // emplacement du fichier de ressource de couleurs
  $emplacement_res_couleurs='/var/www/html/phonochrome/config/ressource_couleur.txt';
  //
  // emplacement du texte correctement phonetisé par Phonetisaurus/Phonochrome
  $emplacement_resultat_phonetise='../output/texte_phonetise.liste_graphies.txt';
  //
  // commande python3 pour lancer le script de recherche de graphies par phonèmes. Ici on part du principe que le script python est dans le même dossier que celui du PHP
  $cmd_python='python3 get_graph.py';

  print'<form action=""  method="post">';
  print'<input type="submit" name="lance_py" value="Lancer le traitement" />';
  print'</form>';

  // On lance le traitement uniquement si l'utilisateur presse le bouton correspondant
  if(isset($_POST['lance_py']))
  {
    // on affiche le résultat dans une div différente du reste
    print'<hr>';
    print'<h4> Résultats du traitement du dernier texte :</h4>';
    print'<hr>';
    print"<div style=\"background-color:black;color:grey;font-size:200%;line-height:50px;\">";
    // on lance le script python
    exec($cmd_python,$out,$status);
    // compteur qui servira à correctement afficher les diphtongues de deux couleurs différentes
    $cpt=0;
    // on met en mémoire le fichier de ressource de couleur dans un tableau avec en clé les phonèmes en API et en valeur les couleurs RGB au format hexadécimal
    $fichier_ressource_couleur = fopen($emplacement_res_couleurs, 'r');
    if ($fichier_ressource_couleur)
      {
        while (!feof($fichier_ressource_couleur))
        {
          // on ne traite pas les commentaires affichés avec une ligne commençant par un '#'
          $ligne = fgets($fichier_ressource_couleur);
          if(preg_match("/^(?:(?!".'^#'.").)*$/i",$ligne)) 
          {
            $ligne_explode = explode("=>", $ligne); // on sépare les codes couleurs des codes phonétiques SAMPA
            $phoneme_sampa = $ligne_explode[0];
            $couleur_correspondante = $ligne_explode[1];
            $tableau_regles_couleur[$phoneme_sampa]=$couleur_correspondante; //on associe chaque clé de phonème avec la valeur en couleur correspondante
          }
        }
      }
    fclose($fichier_ressource_couleur);

    // on traite le fichier de résultat de la phonétisation provenant de l'utilisation de Phonetisaurus sur la page index de Phonochrome
    // on ouvre en premier ce fichier, et on ne traite pas les lignes commençant par "#" car représentant ici espilon, ceci n'étant pas utile pour la suite
    // on crée ensuit deux tableaux, l'un avec les phonèmes en clé et les graphies en phonème, et le deuxième avec les graphies en valeur et les phonèmes en clé
    $fichier_pho_graph = fopen($emplacement_resultat_phonetise, 'r');
    if ($fichier_pho_graph)
      {
        while (!feof($fichier_pho_graph))
        {
          $ligne = fgets($fichier_pho_graph);
          if(preg_match("/^(?:(?!".'^#'.").)*$/i",$ligne)) 
          {
            $trait_ligne=explode(" => ",$ligne); 
            $tab_graph_pho[$trait_ligne[1]]=$trait_ligne[0];
            $tab_pho_graph[$trait_ligne[0]]=$trait_ligne[1];
          }
        }
      }
    fclose($fichier_pho_graph);

    // on filtre les deux tableaux avec la fonction array_filter
    $tab_pho_graph=array_filter($tab_pho_graph);
    $tab_graph_pho=array_filter($tab_graph_pho);
    // on parcourt le tableau de graphème=>phonème et si on trouve la clé dans le fichier de ressource de couleur on associe à la graphie la couleur correspondante
    foreach ($tab_graph_pho as $phoneme)
    {
      if(array_key_exists($phoneme, $tableau_regles_couleur))
      {
        // on détecte une diphtongue si le code hexa est "anormalement long", ce qui signifie qu'il y en a deux sur le modèle "#FFFFFF|#EEEEEE"
        if (strlen($tableau_regles_couleur[$phoneme])>9)                   
        {
          // on récupére les deux couleurs et on associe à la même graphie deux textes de style, l'un étant affiché dans la partie haute du texte et l'autre dans la partie basse
          // les graphies se superposent et donnent ainsi l'illusion d'avoir deux couleurs pour chaque graphies associées à des diphtongues
          $diphtongue=explode("|", $tableau_regles_couleur[$phoneme]);
          echo'<style type="text/css" media="screen">';
          echo'.half'.$cpt.'{font-size: 100%;position: relative;color:'.$diphtongue[0].';line-height: 1em;}';
          echo".half".$cpt.":before {position:absolute;content:''attr(title)'';color:".$diphtongue[1].";height:.6em;overflow: hidden;}";
          echo'</style>';
          echo'<span class="half'.$cpt.'" title='.$phoneme.'>'.$phoneme.' : </span>';
          echo'<span class="half'.$cpt.'" title='.$tab_pho_graph[$phoneme].'>'.$tab_pho_graph[$phoneme].'</span>';
          $cpt=$cpt+1;
          print("<br>");
        }
        else
          // si l'entrée n'est pas une diphtongue, on affiche le phonème et ses graphies avec la couleur correspondante dans le fichier de ressource
        {
          echo '<span style="color:',$tableau_regles_couleur[$phoneme],'">',$phoneme.' : </span>';
          echo '<span style="color:',$tableau_regles_couleur[$phoneme],'">',$tab_pho_graph[$phoneme],'</span>';
          print("<br>");
        }
      }
      else
        // si le phonème n'existe pas dans le fichier de ressource de couleur on l'indique en l'affichant en gris avec une marque (UNK) devant son entrée
      {
        print("(UNK) : ".$phoneme. " : ");
        echo '<i>'.$tab_pho_graph[$phoneme].'</i>';
        print("<br>");
      }
    }
  }
  print'</div>';
?>


    </div>
  </div>
</div>
<div class="wrapper row3">
  <div id="footer" class="clear">
    <section class="one_quarter">
      <h2 class="title">Liens utiles</h2>
      <nav>
        <ul>
          <li><a href="http://kinephones.u-grenoble3.fr/">Projet Kinéphone</a></li>
          <li><a href="http://lidilem.u-grenoble3.fr/">Innovalangues</a></li>
          <li><a href="http://enpa.innovalangues.net/">Lidilem</a></li>
          <li><a href="http://www.univ-grenoble-alpes.fr/">Université Grenoble Alpes</a></li>
        </ul>
      </nav>
    </section>
  </div>
</div>
<div class="wrapper row4">
  <footer id="copyright" class="clear">
    <p class="fl_left">2017 - Université Grenoble Alpes - Master 2 IdL <br> Concepteurs : Elena Melnikova et Sylvain Daronnat</p>
    <p class="fl_right">Powered by <a href="http://www.os-templates.com/" title="Free Website Templates">OS Templates</a><br><br><a href="#header"> [Revenir en haut de la page] </a></p>
  </footer>
</div>
</body>
</html>