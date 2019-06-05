import urllib.request

from flask import json

from database.models import Personnage
from database.database import db

import constantes


# Appelle l'API "api.got.show" pour obtenir la liste des personnages étant apparus dans un nombre minimum d'épisodes
def recuperer_infos_personnages(nb_apparences_min):
    # On récupère les infos en ligne
    api_url = "https://api.got.show/api/show/characters"
    liste_personnages = json.loads(urllib.request.urlopen(api_url).read())

    # On simplifie la liste : on ne garde que les personnages qui sont apparus un certain nombre de fois, et on garde
    # uniquement leur nom, leur acteur et une URL d'image
    ma_liste = []
    for personnage in liste_personnages:
        if len(personnage["appearances"]) >= nb_apparences_min:
            ma_liste.append({
                "nom": personnage["name"],
                "acteur": personnage["actor"],
                "image": personnage["image"]
            })

    return ma_liste


# Récupère les infos des personnages et les ajoute à la base de données si cette dernière est vide
def remplir_db():
    if Personnage.query.first() is None:  # Si la base de données est vide
        print("Base de données vide, récupération de la liste de personnages...")
        infos_personnages = recuperer_infos_personnages(constantes.nb_apparences_min)
        for infos_perso in infos_personnages:
            personnage = Personnage(
                nom=infos_perso["nom"],
                acteur=infos_perso["acteur"],
                image=infos_perso["image"],
                elo=constantes.elo_initial
            )
            db.session.add(personnage)

        db.session.commit()

        # On affiche dans la console du serveur le nombre de personnages ajoutés
        print("%d personnages ajoutés !" % len(infos_personnages))

    else: # Si la base de données n'est pas vide
        print("Chargement de la base de données existante...")
