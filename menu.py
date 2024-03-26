#  Importation des modules pygame et sys.
import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)

# Taille de la fenêtre
taille_fenetre = (626, 334)

# Définition de la classe MenuItem
class Element(pygame.sprite.Sprite):
    # Un constructeur (__init__) qui initialise l'élément avec du texte et une position. 
    def __init__(self, text, position):
        # Appelle le constructeur de la classe Sprite
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None, 36)
        # Utilise la méthode render de l'objet font pour générer une surface (image) contenant le texte de l'élément. 
        self.image = self.font.render(self.text, True, BLANC)
        self.rect = self.image.get_rect()
        # pour positionner l'élément (ou sprite) à l'endroit spécifié par la variable position
        self.rect.topleft = position
        

# Cette fonction crée le menu principal du jeu en générant un groupe de sprites d'éléments de menu. 
def creation_menu():
    elements_menu = ['Commencer', 'Options', 'Quitter']
    menu_sprites = pygame.sprite.Group()
    for index, item in enumerate(elements_menu):
        element_menu = Element(item, (250, 110 + index * 50))
        menu_sprites.add(element_menu)
    return menu_sprites

# Similaire à la fonction creation_menu(), cette fonction crée un groupe de sprites pour le menu des options,
# avec des éléments représentant différents niveaux de difficulté et une option de retour.
def elements_option():
    elements_options = ['Facile', 'Normal', 'Difficile', 'Retour']
    menu_sprites = pygame.sprite.Group()
    # Cette boucle parcourt la liste elements_options en récupérant à la fois l'index de chaque élément et l'élément lui-même.
    for index, item in enumerate(elements_options):
        # L'index est utilisé pour calculer la position verticale de chaque élément afin qu'ils soient espacés verticalement.
        element_menu = Element(item, (260 , 90 + index * 50))
        menu_sprites.add(element_menu)
    return menu_sprites

# Fonction principale
def menu_principal():
    # Création de la fenêtre
    screen = pygame.display.set_mode(taille_fenetre)
    pygame.display.set_caption("Jeu du Démineur")

    # Chargement de l'image d'arrière-plan
    background_image = pygame.image.load("C:/Users/micka/OneDrive/Documents/Démineur/Graphics/demineur.png").convert()
    background_rect = background_image.get_rect()

    # Définition du titre
    font = pygame.font.SysFont('Lexend', 60)
    titre_texte = font.render("Démineur", True, BLANC)
    titre_rect = titre_texte.get_rect(center=(taille_fenetre[0] / 2, 50))

    # Création du menu principal
    menu = creation_menu()

    # Variables pour garder une trace de l'état du menu
    menu_actif = "principal"
    menu_options = None

    # Boucle principale
    running = True
    while running:
        # Gestion des événements
        # Ces événements incluent les pressions de touches, les mouvements de la souris, les clics, et l'événement QUIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
               
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Si clic gauche
                # Vérifier si un bouton a été cliqué
                if menu_actif == "principal":
                    # parcourt tous les éléments du menu principal pour vérifier si l'un d'eux a été cliqué.
                    for item in menu:
                        # vérifie si la position du clic de la souris correspond à la zone de collision de l'élément du menu sur lequel l'utilisateur a cliqué.
                        if item.rect.collidepoint(event.pos):
                            # Si l'élément du menu cliqué est "Commencer", le programme affiche "Commencement du jeu..." 
                            if item.text == 'Commencer':
                                print("Commencement du jeu...")
                            elif item.text == 'Options':
                                # Afficher le menu Options
                                menu_options = elements_option()
                                menu_actif = "options"
                            elif item.text == 'Quitter':
                                # Si l'élément du menu cliqué est "Quitter", le programme se termine en appelant pygame.quit(),
                                # pour quitter Pygame proprement, suivi de sys.exit() pour terminer le script Python.
                                pygame.quit()
                                sys.exit()
                elif menu_actif == "options":
                    for item in menu_options:
                        if item.rect.collidepoint(event.pos):
                            if item.text == 'Facile':
                                print("Difficulté réglée sur facile.")
                            elif item.text == 'Normal':
                                print("Difficulté réglée sur normale.")
                            elif item.text == 'Difficile':
                                print("Difficulté réglée sur difficile.")
                            elif item.text == 'Retour':
                                menu_actif = "principal"

        # Affichage de l'arrière-plan et du titre
        screen.blit(background_image, background_rect)
        screen.blit(titre_texte, titre_rect)

        # Affichage du menu actif
        if menu_actif == "principal":
            menu.draw(screen)
        elif menu_actif == "options":
            menu_options.draw(screen)

        # Mise à jour de l'affichage
        pygame.display.flip()

    pygame.quit()
    sys.exit()
    
# Appel de la fonction principal
if __name__ == "__main__":
    menu_principal()
