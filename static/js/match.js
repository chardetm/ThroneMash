let id_match = 0;

// Affiche l'indicateur de chargement, cache le match (pas encore chargé), demande un nouveau match
function nouveauMatch() {
    $('#ligne-chargement').show();
    $('#ligne-match').hide();
    $.getJSON("/api/matchs_en_cours/nouveau", afficherMatch);
}

// Met à jour la page avec les données du nouveau match reçues, cache l'indicateur de chargement et affiche le match
function afficherMatch(match) {
    id_match = match["id"];
    $("#nom1").html(match["personnage1"]["nom"]);
    $("#nom2").html(match["personnage2"]["nom"]);
    $("#acteur1").html(match["personnage1"]["acteur"]);
    $("#acteur2").html(match["personnage2"]["acteur"]);
    $("#image1").css("background-image", `url('${match["personnage1"]["image"]}')`);
    $("#image2").css("background-image", `url('${match["personnage2"]["image"]}')`);
    $('#ligne-chargement').hide();
    $('#ligne-match').show();
}

// Envoie le résultat du match au serveur et demande un nouveau match
function faireChoix(choix) {
    if (id_match !== 0) {
        $.post("/api/matchs", {id_match_en_cours: id_match, gagnant: choix});
        id_match = 0;
        nouveauMatch();
    }
}

// Clic sur l'image de gauche : choix 1
$('#card1').click(function () {
    faireChoix(1);
});

// Clic sur l'image de droite : choix 2
$('#card2').click(function () {
    faireChoix(2);
});

// Gestion des touches du clavier
$("body").keydown(function(e) {
    if (e.keyCode === 37) {        // flèche gauche
        faireChoix(1);
    } else if (e.keyCode === 39) { // flèche droite
        faireChoix(2);
    }
});

// Au chargement : on lance un nouveau match
$(function() {
    nouveauMatch();
});
