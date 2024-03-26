import pygame
import random
import time

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (192, 192, 192)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)

# Dimensions de la fenêtre et de la grille
LARGEUR_FENETRE = 400
HAUTEUR_FENETRE = 400
TAILLE_GRILLE = 10  # Taille de la grille doit être divisible par le nombre de lignes et de colonnes
TAILLE_CELLULE = LARGEUR_FENETRE // TAILLE_GRILLE

# Niveaux de difficulté
FACILE = {'lignes': 8, 'colonnes': 8, 'mines': 10}
MOYEN = {'lignes': 12, 'colonnes': 12, 'mines': 20}
DIFFICILE = {'lignes': 16, 'colonnes': 16, 'mines': 40}

# Chargement de l'image du bouton de menu
bouton_menu_image = pygame.image.load("C:/Users/micka/OneDrive/Documents/Démineur/Graphics/exit.png")


class Cellule:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revelee = False
        self.minee = False
        self.adjacent_mines = 0
        self.drapeau = False
        self.interrogation = False
        self.images = {
            'bombe': pygame.image.load('C:/Users/micka/OneDrive/Documents/Démineur/Graphics/bomb_bloc.png'),
            'drapeau': pygame.image.load('C:/Users/micka/OneDrive/Documents/Démineur/Graphics/flag.png'),
            'interrogation': pygame.image.load('C:/Users/micka/OneDrive/Documents/Démineur/Graphics/idk bloc.png'),
            'blanc': pygame.image.load('C:/Users/micka/OneDrive/Documents/Démineur/Graphics/white-bloc.png')
        }

    def afficher(self, ecran):
        rect = pygame.Rect(self.y * TAILLE_CELLULE, self.x * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE)
        if self.revelee:
            if self.minee:
                ecran.blit(self.images['bombe'], rect)
            elif self.adjacent_mines > 0:
                afficher_texte(ecran, str(self.adjacent_mines),
                               self.y * TAILLE_CELLULE + TAILLE_CELLULE // 3,
                               self.x * TAILLE_CELLULE + TAILLE_CELLULE // 3)
        elif self.drapeau:
            ecran.blit(self.images['drapeau'], rect)
        elif self.interrogation:
            ecran.blit(self.images['interrogation'], rect)
        else:
            ecran.blit(self.images['blanc'], rect)


class Demineur:
    def __init__(self, difficulte):
        self.difficulte = difficulte
        self.lignes = difficulte['lignes']
        self.colonnes = difficulte['colonnes']
        self.mines = difficulte['mines']
        self.grille = [[Cellule(x, y) for y in range(self.colonnes)] for x in range(self.lignes)]
        self.generer_mines()
        self.calculer_adjacent_mines()
        self.fin_de_jeu = False
        self.temps_debut = time.time()
        self.clic_droit_count = 0
        self.gagne = False  # Ajout de la variable pour suivre l'état du jeu

    def generer_mines(self):
        positions_mines = random.sample(range(self.lignes * self.colonnes), self.mines)
        for pos in positions_mines:
            ligne = pos // self.colonnes
            colonne = pos % self.colonnes
            self.grille[ligne][colonne].minee = True

    def calculer_adjacent_mines(self):
        for x in range(self.lignes):
            for y in range(self.colonnes):
                cellule = self.grille[x][y]
                if not cellule.minee:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if (0 <= x + dx < self.lignes and 0 <= y + dy < self.colonnes and
                                    self.grille[x + dx][y + dy].minee):
                                cellule.adjacent_mines += 1

    def reveler_cellule(self, cellule):
        if cellule.revelee or cellule.drapeau:
            return
        cellule.revelee = True
        if cellule.minee:
            self.fin_de_jeu = True
        elif cellule.adjacent_mines == 0:
            self.reveler_cases_voisines(cellule.x, cellule.y)

    def reveler_cases_voisines(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < self.lignes and 0 <= y + dy < self.colonnes:
                    cellule = self.grille[x + dx][y + dy]
                    if not cellule.revelee:
                        self.reveler_cellule(cellule)
                        if cellule.adjacent_mines == 0:
                            self.reveler_cases_voisines(cellule.x, cellule.y)

    def placer_drapeau(self, cellule):
        if not cellule.revelee and not self.fin_de_jeu:
            if self.clic_droit_count % 3 == 0:
                cellule.drapeau = not cellule.drapeau
                cellule.interrogation = False
            elif self.clic_droit_count % 3 == 1:
                if cellule.drapeau:
                    cellule.drapeau = False
                cellule.interrogation = not cellule.interrogation
            else:
                cellule.drapeau = False
                cellule.interrogation = False
            self.clic_droit_count += 1

    def verifier_victoire(self):
        for ligne in self.grille:
            for cellule in ligne:
                if not cellule.revelee and not cellule.minee:
                    return False
        return True

    def reinitialiser(self):
        self.grille = [[Cellule(x, y) for y in range(self.colonnes)] for x in range(self.lignes)]
        self.generer_mines()
        self.calculer_adjacent_mines()
        self.fin_de_jeu = False
        self.temps_debut = time.time()
        self.clic_droit_count = 0
        self.gagne = False



def afficher_texte(ecran, texte, x, y, taille_police=30, couleur=NOIR):
    font = pygame.font.Font(None, taille_police)
    surface_texte = font.render(texte, True, couleur)
    rect_texte = surface_texte.get_rect()
    rect_texte.topleft = (x, y)
    ecran.blit(surface_texte, rect_texte)


def afficher_temps(ecran, temps, x, y, taille_police=30, couleur=NOIR):
    heures = temps // 3600
    minutes = (temps % 3600) // 60
    secondes = temps % 60
    temps_formatte = "{:02}:{:02}:{:02}".format(heures, minutes, secondes)
    afficher_texte(ecran, temps_formatte, x, y, taille_police, couleur)


def afficher_bouton_rejouer(ecran):
    bouton_rejouer_image = pygame.image.load(
        "C:/Users/micka/OneDrive/Documents/Démineur/Graphics/relance.png")
    afficher_texte(ecran, "Appuyer pour rejouer", 80, 330, couleur=BLEU)
    ecran.blit(bouton_rejouer_image, (150, 350))  # Modifier les coordonnées selon votre disposition


def main():
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption("Démineur")

    horloge = pygame.time.Clock()

    jeu = Demineur(FACILE)

    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                return
            elif evenement.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                ligne = y // TAILLE_CELLULE
                colonne = x // TAILLE_CELLULE
                if evenement.button == 1:  # Clic gauche
                    if 150 <= x <= 250 and 350 <= y <= 400:  # Si les coordonnées de clic sont sur le bouton
                        jeu.reinitialiser()  # Réinitialiser le jeu
                    else:
                        jeu.reveler_cellule(jeu.grille[ligne][colonne])
                elif evenement.button == 3:  # Clic droit
                    jeu.placer_drapeau(jeu.grille[ligne][colonne])
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_r:  # Réinitialiser le jeu
                    jeu.reinitialiser()

        ecran.fill(BLANC)

        # Affichage de la grille
        for x in range(jeu.lignes):
            for y in range(jeu.colonnes):
                cellule = jeu.grille[x][y]
                cellule.afficher(ecran)

        # Temps écoulé
        if not jeu.fin_de_jeu and not jeu.gagne:  # Vérification si le jeu est en cours
            temps_ecoule = int(time.time() - jeu.temps_debut)
        afficher_temps(ecran, temps_ecoule, 10, HAUTEUR_FENETRE - 30)

        # Afficher le bouton "Rejouer"
        afficher_bouton_rejouer(ecran)

        # Afficher le bouton de menu
        ecran.blit(bouton_menu_image, (LARGEUR_FENETRE - bouton_menu_image.get_width(), 0))

        if jeu.fin_de_jeu:
            afficher_texte(ecran, "Perdu !", 50, HAUTEUR_FENETRE // 10, couleur=ROUGE)
            jeu.gagne = True  # Arrêter le temps lorsque le joueur perd
            pygame.display.flip()
        elif jeu.verifier_victoire():
            afficher_texte(ecran, "Gagné !", 50, HAUTEUR_FENETRE // 10, couleur=VERT)
            jeu.gagne = True  # Arrêter le temps lorsque le joueur gagne
            pygame.display.flip()

        pygame.display.flip()
        horloge.tick(30)


if __name__ == "__main__":
    main()
