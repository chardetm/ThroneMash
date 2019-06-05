from database.database import db


class Personnage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    acteur = db.Column(db.Text)
    image = db.Column(db.Text)
    elo = db.Column(db.Float)

    def serialize(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "acteur": self.acteur,
            "image": self.image,
            "elo": self.elo
        }


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_gagnant = db.Column(db.Integer, db.ForeignKey(Personnage.id))
    ancien_elo_gagnant = db.Column(db.Float)
    nouvel_elo_gagnant = db.Column(db.Float)
    id_perdant = db.Column(db.Integer, db.ForeignKey(Personnage.id))
    ancien_elo_perdant = db.Column(db.Float)
    nouvel_elo_perdant = db.Column(db.Float)

    def serialize(self):
        return {
            "id": self.id,
            "id_gagnant": self.id_gagnant,
            "ancien_elo_gagnant": self.ancien_elo_gagnant,
            "nouvel_elo_gagnant": self.nouvel_elo_gagnant,
            "id_perdant": self.id_perdant,
            "ancien_elo_perdant": self.ancien_elo_perdant,
            "nouvel_elo_perdant": self.nouvel_elo_perdant
        }


class MatchEnCours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_personnage1 = db.Column(db.Integer, db.ForeignKey(Personnage.id))
    id_personnage2 = db.Column(db.Integer, db.ForeignKey(Personnage.id))

    def serialize(self):
        return {
            "id": self.id,
            "id_personnage1": self.id_personnage1,
            "id_personnage2": self.id_personnage2
        }
