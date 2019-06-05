// Récupère le nouveau contenu du tableau et de la liste en faisant un appel AJAX
function rafraichir() {
    $("#contenu-tableau-classement").load("/ajax/contenu_tableau_classement");
    $("#contenu-liste-derniers-matchs").load("/ajax/contenu_liste_derniers_matchs");
}

// Au chargement, on récupère le contenu et on demande une mise à jour périodique
$(function() {
    rafraichir();
    setInterval(rafraichir, 2000); // toutes les 2 secondes
});
