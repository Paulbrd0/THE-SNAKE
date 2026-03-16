import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# Taille initiale
largeur = 600
hauteur = 400
fenetre = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)
pygame.display.set_caption("Snake Network Adventure")
clock = pygame.time.Clock()

# Couleurs
vert = (0, 255, 0)
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Police de base
base_font_size = 13
font = pygame.font.SysFont("TT rounds neue", base_font_size)

# -------- IMAGES --------
fond1 = pygame.image.load("images/fond1.png")
fond2 = pygame.image.load("images/fond2.png")
pomme_img_orig = pygame.image.load("images/pomme.png").convert_alpha()

# -------- SONS --------
eat_sound = pygame.mixer.Sound("sons/eat.wav")
gameover_sound = pygame.mixer.Sound("sons/gameover.wav")
pygame.mixer.music.load("sons/musique.wav")

# -------- FONCTION TEXTE MULTILIGNE CENTRÉ --------
def texte_centre_multiligne(lignes, y_start_ratio=None, espace_ratio=0.05):
    n = len(lignes)
    total_hauteur = n * espace_ratio * hauteur
    if y_start_ratio is None:
        y = (hauteur - total_hauteur) / 2  # centre vertical du bloc
    else:
        y = hauteur * y_start_ratio
    for ligne in lignes:
        texte_img = font.render(ligne, True, blanc)
        x = (largeur - texte_img.get_width()) // 2
        fenetre.blit(texte_img, (x, y))
        y += espace_ratio * hauteur

# -------- REDIMENSIONNEMENT --------
def redimensionner(new_largeur, new_hauteur):
    global largeur, hauteur, fenetre, font
    largeur, hauteur = new_largeur, new_hauteur
    fenetre = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)
    font = pygame.font.SysFont("Arial", max(base_font_size, largeur // 35))

# -------- INTRO --------
def intro():
    intro_running = True
    lignes = [
        "Bienvenue dans Snake Network Adventure",
        "Vous êtes un serpent explorant un réseau informatique",
        "à la recherche de données mystérieuses.",
        "Créé par : Ton Nom",
        "Classe : 1e NSI",
        "Date : 2026",
        "Appuyez sur une touche pour continuer"
    ]
    while intro_running:
        fenetre.fill(noir)
        texte_centre_multiligne(lignes, y_start_ratio=None, espace_ratio=0.07)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                intro_running = False
            elif event.type == pygame.VIDEORESIZE:
                redimensionner(event.w, event.h)

# -------- MENU --------
def menu():
    while True:
        fenetre.fill(noir)
        lignes = [
            "Snake Network Adventure",
            "1 - Jouer",
            "2 - Quitter",
            "3 - Explications",
            "4 - Crédits"
        ]
        texte_centre_multiligne(lignes, y_start_ratio=None, espace_ratio=0.1)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                redimensionner(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    jeu()
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_3:
                    explications()
                elif event.key == pygame.K_4:
                    credits()

# -------- EXPLICATIONS --------
def explications():
    while True:
        fenetre.fill(noir)
        lignes = [
            "Explications",
            "Réseau informatique :",
            "Un réseau informatique est un ensemble d'ordinateurs connectés",
            "pour échanger des informations. Exemples : LAN, Internet.",
            "Modèle client/serveur :",
            "Le client demande un service.",
            "Le serveur répond à la demande. Exemple : navigateur web et serveur.",
            "Python :",
            "Editeur de texte : écrire du code",
            "Interpréteur : exécute le code",
            "Console/Shell : lancer Python",
            "IDE : logiciel complet pour programmer (VS Code, PyCharm, Spyder)",
            "Appuyez sur M pour revenir au menu"
        ]
        texte_centre_multiligne(lignes, y_start_ratio=None, espace_ratio=0.05)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                menu()
            elif event.type == pygame.VIDEORESIZE:
                redimensionner(event.w, event.h)

# -------- CRÉDITS --------
def credits():
    while True:
        fenetre.fill(noir)
        lignes = [
            "C'était un jeu très similaire appelé Blockade. ",
            "Blockade a été créé par le fabricant de jeux Gremlin, ",
            "une société de jeux basée à San Diego. ",
            "Ils ont publié le jeu en 1976",
            "Crédits",
            "Créé par : code créé par Paul Berard avec l'aide de ChatGPT",
            "Classe : 1e NSI",
            "Année : 2026",
            "Merci d'avoir joué !",
            "Appuyez sur M pour revenir au menu"
        ]
        texte_centre_multiligne(lignes, y_start_ratio=None, espace_ratio=0.07)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                menu()
            elif event.type == pygame.VIDEORESIZE:
                redimensionner(event.w, event.h)

# -------- JEU --------
def jeu():
    serpent = [(100, 100)]
    direction = (1, 0)
    score = 0
    vitesse = 10
    pygame.mixer.music.play(-1)

    taille_bloc = max(20, largeur // 20)
    taille_pomme = int(taille_bloc * 2)
    pomme_img = pygame.transform.scale(pomme_img_orig, (taille_pomme, taille_pomme))
    pomme = (
    random.randrange(taille_bloc*2, largeur - taille_bloc*2, taille_bloc),
    random.randrange(taille_bloc*2, hauteur - taille_bloc*2, taille_bloc)
)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                redimensionner(event.w, event.h)
                taille_bloc = max(20, largeur // 20)
                taille_pomme = int(taille_bloc * 2)
                pomme_img = pygame.transform.scale(pomme_img_orig, (taille_pomme, taille_pomme))

        touches = pygame.key.get_pressed()
        if touches[pygame.K_UP] and direction != (0,1):
            direction = (0, -1)
        if touches[pygame.K_DOWN] and direction != (0,-1):
            direction = (0, 1)
        if touches[pygame.K_LEFT] and direction != (1,0):
            direction = (-1, 0)
        if touches[pygame.K_RIGHT] and direction != (-1,0):
            direction = (1, 0)

        tete = (serpent[0][0] + direction[0]*taille_bloc, serpent[0][1] + direction[1]*taille_bloc)
        serpent.insert(0, tete)

        if tete[0] < pomme[0] + taille_pomme and tete[0] + taille_bloc > pomme[0] and \
           tete[1] < pomme[1] + taille_pomme and tete[1] + taille_bloc > pomme[1]:
            score += 1
            eat_sound.play()
            pomme = (
    random.randrange(taille_bloc*2, largeur - taille_bloc*2, taille_bloc),
    random.randrange(taille_bloc*2, hauteur - taille_bloc*2, taille_bloc)
)
            vitesse += 0.5
        else:
            serpent.pop()

        if tete[0] < 0 or tete[0] >= largeur or tete[1] < 0 or tete[1] >= hauteur or tete in serpent[1:]:
            game_over(score)

        fond = fond1 if score < 5 else fond2
        fenetre.blit(pygame.transform.scale(fond, (largeur, hauteur)), (0,0))
        fenetre.blit(pomme_img, pomme)

        for bloc in serpent:
            pygame.draw.rect(fenetre, vert, (bloc[0], bloc[1], taille_bloc, taille_bloc))

        tete_x, tete_y = serpent[0]
        oeil_offset = max(3, taille_bloc // 6)
        if direction[0] > 0:
            yeux = [(tete_x + taille_bloc - oeil_offset, tete_y + oeil_offset),
                    (tete_x + taille_bloc - oeil_offset, tete_y + taille_bloc - oeil_offset)]
        elif direction[0] < 0:
            yeux = [(tete_x + oeil_offset, tete_y + oeil_offset),
                    (tete_x + oeil_offset, tete_y + taille_bloc - oeil_offset)]
        elif direction[1] < 0:
            yeux = [(tete_x + oeil_offset, tete_y + oeil_offset),
                    (tete_x + taille_bloc - oeil_offset, tete_y + oeil_offset)]
        else:
            yeux = [(tete_x + oeil_offset, tete_y + taille_bloc - oeil_offset),
                    (tete_x + taille_bloc - oeil_offset, tete_y + taille_bloc - oeil_offset)]
        for oeil in yeux:
            pygame.draw.circle(fenetre, blanc, oeil, oeil_offset)

        texte_centre_multiligne([f"Score : {score}"], y_start_ratio=0.02, espace_ratio=0.05)
        pygame.display.update()
        clock.tick(vitesse)

# -------- GAME OVER --------
def game_over(score):
    pygame.mixer.music.stop()
    gameover_sound.play()
    while True:
        fenetre.fill(noir)
        lignes = [
            "GAME OVER",
            f"Score : {score}",
            "R : Rejouer",
            "M : Menu"
        ]
        texte_centre_multiligne(lignes, y_start_ratio=None, espace_ratio=0.1)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                redimensionner(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    jeu()
                elif event.key == pygame.K_m:
                    menu()

# -------- LANCEMENT --------
intro()
menu()