import random

import flask

from flask import Flask, json, request, abort, url_for

from database.database import db, init_database
from database.models import Personnage, Match, MatchEnCours
from init import remplir_db
from elo import CalculateurElo

# Constantes définies dans le fichier constantes.py
import constantes


# Configuration de l'application

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.test_request_context():
    init_database()
    remplir_db() # remplissage intial (voir init.py)

# On initialise le calculateur d'ELO dont on se servira (voir elo.py)
calculateur_elo = CalculateurElo(constantes.elo_k)


# Points d'entrée

# Page principale de match (HTML)
@app.route('/')
def match():
    return flask.Response(flask.render_template(
        "match.html.jinja2",
        js_path=url_for("static", filename="js/match.js"),
        css_path=url_for("static", filename="css/style.css"),
        active="match"
    ))


# Page de classement (HTML)
@app.route('/classement')
def classement():
    return flask.Response(flask.render_template(
        "classement.html.jinja2",
        js_path=url_for("static", filename="js/classement.js"),
        css_path=url_for("static", filename="css/style.css"),
        active="classement",
        subtitle=" : classement"
    ))


# Contenu du tableau de classement (partie de page HTML)
@app.route('/ajax/contenu_tableau_classement')
@app.route('/ajax/contenu_tableau_classement/<int:nb>')
@app.route('/ajax/contenu_tableau_classement/<int:start>/<int:nb>')
def contenu_tableau_classement(start=0, nb=1000):
    return flask.Response(flask.render_template(
        "contenu_tableau_classement.html.jinja2",
        classement=Personnage.query.order_by(Personnage.elo.desc()).offset(start).limit(nb).all()
    ))


# Contenu de la liste des derniers matchs (partie de page HTML)
@app.route('/ajax/contenu_liste_derniers_matchs')
@app.route('/ajax/contenu_liste_derniers_matchs/<int:nb>')
@app.route('/ajax/contenu_liste_derniers_matchs/<int:start>/<int:nb>')
def contenu_liste_derniers_matchs(start=0, nb=10):
    derniers_matchs = [m.serialize() for m in Match.query.order_by(Match.id.desc()).offset(start).limit(nb).all()]
    for m in derniers_matchs:
        m.update({
            "nom_gagnant": Personnage.query.filter_by(id=m["id_gagnant"]).first().nom,
            "nom_perdant": Personnage.query.filter_by(id=m["id_perdant"]).first().nom
        })
    return flask.Response(flask.render_template(
        "contenu_liste_derniers_matchs.html.jinja2",
        derniers_matchs=list(derniers_matchs)
    ))


# Liste des personnages (JSON)
@app.route('/api/personnages')
def get_personnages():
    return json.jsonify([p.serialize() for p in Personnage.query.all()])


# Liste des matchs en cours (JSON)
@app.route('/api/matchs_en_cours', methods=["GET"])
@app.route('/api/matchs_en_cours/<int:nb>')
@app.route('/api/matchs_en_cours/<int:start>/<int:nb>')
def get_matchs_en_cours(start=0, nb=1000):
    return json.jsonify([m.serialize() for m in MatchEnCours.query.order_by(MatchEnCours.id.desc()).offset(start).limit(nb).all()])


# Création d'un nouveau match, retour de l'ID du match et des informations sur les participants (JSON)
@app.route('/api/matchs_en_cours/nouveau')
def get_new_match():
    query1 = db.session.query(Personnage)
    nb_personnages = int(query1.count())
    personnage1 = query1.offset(int(nb_personnages * random.random())).first()

    query2 = db.session.query(Personnage)
    personnage2 = query2.filter(Personnage.id != personnage1.id).offset(int((nb_personnages-1) * random.random())).first()

    nouveau_match = MatchEnCours(id_personnage1=personnage1.id, id_personnage2=personnage2.id)
    db.session.add(nouveau_match)
    db.session.commit()

    return json.jsonify({
        "id": nouveau_match.id,
        "personnage1": personnage1.serialize(),
        "personnage2": personnage2.serialize()
    })


# Liste des derniers matchs (JSON)
@app.route('/api/matchs', methods=["GET"])
@app.route('/api/matchs/<int:nb>')
@app.route('/api/matchs/<int:start>/<int:nb>')
def get_matchs(start=0, nb=1000):
    return json.jsonify([m.serialize() for m in Match.query.order_by(Match.id.desc()).offset(start).limit(nb).all()])


# Réception du résultat d'un match (retour vide)
@app.route('/api/matchs', methods=["POST"])
def post_match():
    # On récupère toutes les infos
    id_match_en_cours = int(request.form["id_match_en_cours"])
    match_en_cours = MatchEnCours.query.filter_by(id=id_match_en_cours).first()
    numero_gagnant = int(request.form["gagnant"])
    id_g = match_en_cours.id_personnage1 if numero_gagnant == 1 else match_en_cours.id_personnage2
    id_p = match_en_cours.id_personnage1 if numero_gagnant == 2 else match_en_cours.id_personnage2
    gagnant = Personnage.query.filter_by(id=id_g).first()
    perdant = Personnage.query.filter_by(id=id_p).first()

    # Si le perdant ou le gagnant n'a pas pu être trouvé avec son ID, on renvoie une erreur 400 (bad request)
    if gagnant is None or perdant is None:
        abort(400)

    # On garde en mémoire l'ancien ELO des personnages et on calcule leur nouvel ELO
    ancien_elo_gagnant = gagnant.elo
    ancien_elo_perdant = perdant.elo
    gagnant.elo = calculateur_elo.gagne(gagnant.elo, perdant.elo)
    perdant.elo = calculateur_elo.perdu(perdant.elo, gagnant.elo)

    # On créer la nouvelle entrée Match
    match = Match(
        id_gagnant=id_g,
        ancien_elo_gagnant=ancien_elo_gagnant,
        nouvel_elo_gagnant=gagnant.elo,
        id_perdant=id_p,
        ancien_elo_perdant=ancien_elo_perdant,
        nouvel_elo_perdant=perdant.elo
    )

    # Mise à jour de la BDD : mise à jour des personnages (pour leur ELO), ajout du match, suppression du match en cours
    db.session.add(gagnant)
    db.session.add(perdant)
    db.session.add(match)
    db.session.delete(match_en_cours)
    db.session.commit()

    # Affichage dans le terminal du serveur du résultat du match (log)
    print("%s : +%d (%d -> %d), %s : -%d (%d -> %d)" %
          (gagnant.nom,
           gagnant.elo-ancien_elo_gagnant,
           ancien_elo_gagnant,
           gagnant.elo,
           perdant.nom,
           ancien_elo_perdant - perdant.elo,
           ancien_elo_perdant,
           perdant.elo))

    # On renvoie une réponse vide avec un code 200 (OK)
    return "", 200


if __name__ == '__main__':
    app.run()
