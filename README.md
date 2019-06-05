# Throne Mash

Une implémentation en Flask et Javascript (jQuery) d'un site de type "Face Mash" permettant de classer des
personnages de Game of Thrones. Le système ELO est utilisé pour le classement.

Le fichier `constantes.py` permet de personnaliser divers paramètres, tels que la configuration du classement ELO
et le nombre d'épisodes minimum dans lequel un personnage doit être apparu pour être ajouté à la liste.

Auteur : Maverick Chardet  
Licence : WTFPL  
Site : https://github.com/chardetm/ThroneMash

## Points d'intérêt pédagogiques

Javascript (jQuery) :

- **Montrer ou cacher un élément HTML**  
*`match.js`, fonction `nouveauMatch`*
- **Récupérer du JSON et appeler un callback pour le traiter**  
*`match.js`, fonction `nouveauMatch`*
- **Changer le contenu d'un élément HTML**  
*`match.js`, fonction `afficherMatch`*
- **Changer le style CSS d'un élément HTML**  
*`match.js`, fonction `afficherMatch`*
- **Faire une requête POST**  
*`match.js`, fonction `faireChoix`*
- **Réagir quand l'utilisateur clique sur un élément HTML**  
*`match.js`, événement `$('#card1').click`*
- **Réagir quand l'utilisateur appuie sur une touche**  
*`match.js`, événement `$("body").keydown`*
- **Exécuter une fonction Javascript au chargement**  
*`match.js`, fonction `$` (tout en bas)*
- **Mettre à jour le contenu d'un élément HTML en faisant un appel AJAX retournant
directement le nouveau contenu**  
*`classement.js`, fonction `rafraichir`*
- **Exécuter une fonction Javascript périodiquement**  
*`classement.js`, fonction `$` (tout en bas)*

Flask :

- **Remplir une BDD avec des données provenant d'une API externe**  
*`init.py`*
- **Retourner une partie de page HTML pour une utilisation en AJAX**  
*`app.py`, fonction `contenu_tableau_classement`*
- **Rendre des paramètres d'URL optionnels**  
*`app.py`, fonction `contenu_tableau_classement`*
- **Classer les réponses d'une requête BDD dans l'ordre descendant**  
*`app.py`, fonction `contenu_tableau_classement`*
- **Faire de la pagination lors d'une requête BDD (nb d'éléments sautés, nb d'éléments affichés)**  
*`app.py`, fonction `contenu_tableau_classement`*
- **Modifier les éléments renvoyés par la BDD avant de les passer à un template (avec sérialisation)**  
*`app.py`, fonction `contenu_liste_derniers_matchs`*  
*`database/models.py`, fonctions `serialize`*  
- **Retourner une représentation JSON du retour d'une requête BDD**  
*`app.py`, fonction `get_personnages`*  
*`database/models.py`, fonctions `serialize`*  
- **Recevoir une requête POST et récupérer les informations envoyées**  
*`app.py`, fonction `post_match`*  
- **Gérer une erreur**  
*`app.py`, fonction `post_match`*  
- **Renvoyer un code de réponse HTTP**  
*`app.py`, fonction `post_match`*  
