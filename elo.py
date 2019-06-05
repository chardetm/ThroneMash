# Implémentation simplé du système ELO
# (voir https://fr.wikipedia.org/wiki/Classement_Elo)


class CalculateurElo:
    def __init__(self, k):
        self.k = k

    # Score attendu en fonction de l'ELO actuel des deux participants
    @staticmethod
    def _attendu(mon_classement, classement_opposant):
        return 1 / (1 + 10 ** ((classement_opposant - mon_classement) / 400))

    # Calcul de notre nouvel ELO en fonction de notre ELO actuel, de celui de notre opposant et du score effectif
    def avec_score(self, mon_classement, classement_opposant, score):
        expected = self._attendu(mon_classement, classement_opposant)
        return mon_classement + self.k * (score - expected)

    # Calcul de notre nouvel ELO suite à une victoire en fonction de notre ELO actuel et de celui de notre opposant
    def gagne(self, mon_classement, classement_opposant):
        return self.avec_score(mon_classement, classement_opposant, 1)

    # Calcul de notre nouvel ELO suite à une défaite en fonction de notre ELO actuel et de celui de notre opposant
    def perdu(self, mon_classement, classement_opposant):
        return self.avec_score(mon_classement, classement_opposant, 0)
