<?php error_reporting( E_ALL ); ini_set( "display_errors", 1 ); ini_set('display_startup_errors', 1);?>
<!-- # PHONOCHROME :
# Colorize graphemes and calculate sets of contrasted colors using multiples Open Source libraries (Phonetisaurus, OpenFST,GoogleNgram, Colormaths, colorsys)
# 
# > Cette page est la page de présentation de Phonochrome, où l'outil de colorisation des graphies selon les phonèmes peut être utilisé
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
      <h2>I. Interface de colorisation</h2>
      <p>Sur cette page vous pourrez tester l'outil de colorisation en rentrant un texte dans le formulaire prévu à cet effet puis en choisissant la langue correspondante (si disponible) parmi celles prises en charge par le programme.</p>

<?php
  // L'utilisateur sélectionne la langue d'entrée du texte qu'il a inséré parmi celles disponibles dans le programme
  print"<h3>Choisissez la langue d'origine du texte</h3>";
  print "\n<form name=\"Colorisation_texte_utilisateur\" method=\"POST\" action=\"\">\n";
  print "<select name=\"langue\">";
  
  // le programme renvoit la même valeur pour le chemin d'accès au modèle de langue que celle utilisé dans la liste de choix, en résumé si le dossier s'appelle
  // 'english' le programme va chercher dans 'english' le fichier 'english.fst'
  
  // emplacement des dossiers et fichiers de ressources
  $emplacement_ressources="../res";
  if (is_dir($emplacement_ressources)) 
  {  
    if ($dh = opendir($emplacement_ressources)) 
    {
      while (($element = readdir($dh)) !== false) 
      {
        if ($element !=".." && $element != ".")
        {
          print "<option value=\"$element\">$element</option>\n";
        }
      }
      closedir($dh);
    }
  }
  print "</select>";

  // affichage du modèle de langue utilisé pour traiter le texte en entrée
  if(isset($_POST['langue']))
  {
    $select_lang = $_POST['langue'];
    echo "<br>Modèle de langue utilisé : ".$select_lang.".fst";
  }
  // L'utilisateur rentre le texte à coloriser ici, il peut choisir de le traiter ou de réinitialiser la page
  print "<textarea name=\"texte_entree\" id=\"texte_a_coloriser\" placeholder=\"Rentrez le texte à coloriser ici.\"></textarea>";
  print "\n\t<input type=\"submit\" name=\"colorisation_submit\" value=\"Coloriser le texte\" >\n";
  print "<input type=\"button\" onclick=\"document.location.href='index.php'\" value=\"Réinitialisation\">";
  print "</form>";
  if(isset($_POST['colorisation_submit']) && empty($_POST['texte_entree']))
  {
    print "<h5 id=\"warning_vide\">/!\ Attention, aucun texte n'a été détecté /!\</h5>\n";
  }
  
  // chargement des ressources de couleur en mémoire, les lignes commençant par "#" ne sont pas prises en compte et les codes couleurs sont au format hexadécimal
  $fichier_ressource_couleur = fopen('/var/www/html/phonochrome/config/ressource_couleur.txt', 'r');
  if ($fichier_ressource_couleur)
    {
      while (!feof($fichier_ressource_couleur))
      {
        $ligne = fgets($fichier_ressource_couleur);
        if(preg_match("/^(?:(?!".'^#'.").)*$/i",$ligne)) 
        {
          // on split sur l'élément séparateur '=>' car le modèle de représentation est : API=>#codehexa
          $ligne_explode = explode("=>", $ligne);
          $phoneme_sampa = $ligne_explode[0];
          $couleur_correspondante = $ligne_explode[1];
          //on associe chaque clé de phonème avec la valeur en couleur correspondante
          $tableau_regles_couleur[$phoneme_sampa]=$couleur_correspondante;
        }
      }
    }
  fclose($fichier_ressource_couleur);

  if (!empty($_POST['texte_entree']))
  {
    //on vide le contenu de l'ancien fichier traitee par le programme, ceci servira au programme de récupération des graphies par phonèmes
    $nothingness="";
    file_put_contents( '../output/texte_phonetise.txt',$nothingness);
    // ce compteur permettra de générer des micro fiches de style pour chaque diphtongue afin d'afficher des lettres de deux couleurs différentes
    $cpt=0;
    print"<div id=\"resultats\">\n";
    print"\t<h3>Résultats de la colorisation :</h3>\n";
    print"<br>\n";

    // début du calcul du temps d'execution du programme
    $timestamp_debut = microtime(true);
    // on passe le texte de l'utilisateur en minuscule, nos modèles de langue étant entrainés sur des corpus en minuscules et Phonetisaurus étant sensible à la casse
    $texte_utilisateur_non_formate = trim(strtolower($_POST['texte_entree']));

    // on tokénise le texte d'entrée de l'utilisateur afin d'envoyer comme argument à Phonétisaurus un seul token à la fois, il faut faire attention à backslahser certains éléments
    $tokenisation = preg_split("/( |\.|,|;|:|\?|\!)/",$texte_utilisateur_non_formate);

    foreach ($tokenisation as $token) 
          {
            // chemin d'accès de Phonetisaurus, prenant en entrée un token à la fois et le modèle de langue correspondant à celui choisit par l'utilisateur
            $cmd_phoneticize='python2 /var/www/html/phonochrome/Phonetisaurus/script/phoneticize.py -m /var/www/html/phonochrome/res/'.$select_lang.'/'.$select_lang.'.fst -w '.'"'.$token.'"';
            // on lance le traitement de Phonetisaurus (en ne passant pas par le binaire, car trop lent pour chaque mot)
            exec($cmd_phoneticize,$out,$status);

            // phase de normalisation
            // on réunit le résultat de la commande de phonetisaurus en plaçant une virgule entre chaque token traité
            $array_out_to_string = implode(",",$out);
            $pattern = '/<eps>/';
            $replacement = '##';
            // on supprime les symboles "<eps>" qui ne s'affichent pas en PHP/HTML et ne servent à rien pour la suite du programme
            $sanitized_output = preg_replace($pattern, $replacement, $array_out_to_string);

            // on sépare les tokens traités et normalisés suivant les virgules et
            $graphie_pho=explode(",",$sanitized_output);

            // on traite chaque élément (tokens) dans une boucle foreach
            foreach ($graphie_pho as $elem) 
            {
              // on ne traite que les lignes n'étant pas "epsilon" et donc ne commençant pas par "##" comme précisé plus haut
              if(preg_match("/^(?:(?!".'^#'.").)*$/i",$elem))
              {
                # on réunit les lettres qui doivent être colorisées de la même couleur car séparées par "|" dans Phonetisaurus
                $elem=str_replace("|","",$elem);
                # On sépare les graphies des phonèmes correspondant, ici séparés par "::" comme précisé dans le fichier de traitement de Phonetisaurus
                $sep_graph_pho=explode("::",$elem);

                // on vérifie que les valeurs existent pour les transférer à d'autres variables pour la suite
                if(isset($sep_graph_pho[0])) 
                {
                  $graphie=$sep_graph_pho[0];
                }
                else
                {
                  $graphie="";
                }

                if(isset($sep_graph_pho[1])) 
                {
                  $phoneme=$sep_graph_pho[1];
                }
                else
                {
                  $phoneme="";
                }

                // si le phonème indiqué par Phonétisaurus existe dans les ressource de couleur on commence le traitement d'associations des couleurs aux graphies
                if(array_key_exists($phoneme, $tableau_regles_couleur))
                {

                  if (strlen($tableau_regles_couleur[$phoneme])>9) 
                  {
                    $diphtongue=explode("|", $tableau_regles_couleur[$phoneme]);
                    // version où la diphtongue est affichée en surlignage et non de deux couleurs différentes
                    // echo '<span style="color:',$diphtongue[0],';text-decoration:underline;text-decoration-color:',$diphtongue[1],';">',$graphie,'</span>';
                    echo'<style type="text/css" media="screen">';
                    echo'.half'.$cpt.'{font-size: 100%;position: relative;color:'.$diphtongue[0].';line-height: 1em;}';
                    echo".half".$cpt.":before {position:absolute;content:''attr(title)'';color:".$diphtongue[1].";height:.6em;overflow: hidden;}";
                    echo'</style>';
                    echo'<span class="half'.$cpt.'" title='.$graphie.'>'.$graphie.'</span>';
                  }
                  else
                  {
                    echo '<span style="color:',$tableau_regles_couleur[$phoneme],'">',$graphie,'</span>';
                  }
                }
                else 
                { 
                  echo '<i>',$graphie,'</i>';
                } 

              }

            }
           print(" ");
        $cpt=$cpt+1;   
        $out="";
    // à modifier si besoin pour ne pas tout écraser à chaque remise de $out à zéro
    // file_put_contents( '../output/texte_phonetise.txt',$sanitized_output);
    $fichier_traite_phonetisaurus='../output/texte_phonetise.txt';
    $fichier_traite_ajout = fopen($fichier_traite_phonetisaurus, 'a+');

    fwrite($fichier_traite_ajout, $sanitized_output);
    fclose($fichier_traite_ajout);
    }

  $timestamp_fin = microtime(true);
  $difference_ms = $timestamp_fin - $timestamp_debut;
  $arrondir=round($difference_ms,2);
  print"<br>";
  print"</div>";
  echo '<p>Traitement effectué en <b>'.$arrondir.'</b> secondes.</p>';
  print'<form><input type="button" value="Voir les graphies et Phonèmes de ce texte" onclick="window.location.href=\'aff_pho_graph.php\'" /></form>';
  }

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