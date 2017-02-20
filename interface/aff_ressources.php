<!-- # PHONOCHROME :
# Colorize graphemes and calculate sets of contrasted colors using multiples Open Source libraries (Phonetisaurus, OpenFST,GoogleNgram, Colormaths, colorsys)
# 
# > Cette page permet simplement d'afficher de manière plus agréable le fichier de ressource de couleur présent dans le dossier approprié
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
      <h2>III. Affichage des ressources</h2>
      <p>Sur cette page vous trouverez les associations couleurs/phonèmes utilisé par le programme ainsi qu'un lien permettant d'aller explorer les modèles utilisés pour chaques langues.</p>

<?php

  // Emplacement du fichier de ressource de couleur
  $emplacement_res_couleurs='../config/ressource_couleur.txt';

  // le modèle d'affichage des ressource est toujours le même : une div de la couleur du phonème (2 couleurs si diphtongues), en 'titre' le phonème en API et le code hexadécimal correspondant en dernière ligné, le tout séparé des autres par une balise HTML 'hr'

  // on lit le fichier de ressource de couleur ligne par ligne
  $fichier_ressource_couleur = fopen($emplacement_res_couleurs, 'r');
  while (!feof($fichier_ressource_couleur))
    {
      # on ne prend pas en compte celles commençant par '#'
      $ligne = fgets($fichier_ressource_couleur);
      if(preg_match("/^(?:(?!".'^#'.").)*$/i",$ligne) && $ligne != "") 
        {
          // on récupère les phonèmes et leurs couleurs qui sont séparés par des '=>' dans le fichier de ressource
          $ligne_explode = explode("=>", $ligne); 
          $phoneme_sampa = $ligne_explode[0];
          $couleur_correspondante = $ligne_explode[1];
        
          // si deux couleurs sont présentes dans le fichier de ressource on l'indique en affichant une div dans une div, la première possèdant une couleur différente de la deuxième
          if (strlen($couleur_correspondante)>9)
            {
              $couleur_diphtongue=explode("|", $couleur_correspondante);
              echo"<h2>/$phoneme_sampa/ :</h2>";
              echo'<div style="background-color:',$couleur_diphtongue[1],';height:75px;width:75px;border:1px solid;"> <div style="background-color:',$couleur_diphtongue[0],';height:37px;width:75px;"></div></div>';
              echo'<b>Code hexadécimal :</b>',$couleur_diphtongue[0], ' (haut) <b>et</b> ' ,$couleur_diphtongue[1],'(bas)<br><hr>';
            }
          else
          // si le phonème n'est pas différent on affiche une div de la couleur qui lui correspondant
            {
              echo"<h2>/$phoneme_sampa/ :</h2>",'<div style="background-color:',$couleur_correspondante,';height:75px;width:75px;border:1px solid;"></div>';
              echo'<b>Code hexadécimal :</b>',$couleur_correspondante,'<br><hr>';
            }
        }
    }
  // on ferme le fichier de ressource de couleurs
  fclose($fichier_ressource_couleur);
  
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
