"""
\file interface.py
\brief Implémentation de l'interface graphique d'une Tier List
\author Maksym Valigunda
\version 1.0
"""

from tkinter import Tk, Label, NSEW, Button, messagebox, Menu, Scrollbar, Frame, Canvas
import tkinter.font as tkfont
from canvas import CanvasTierList
from position import Position
from PIL import ImageTk, Image, ImageGrab
import os
import ast


class FenetreTierList(Tk):
    """L'objet FenetreTierList qui représente le concept d'interface graphique d'une liste de palliers (Tier List)
    affichée sous forme de fenêtre comprenant un canvas qui affiche la grille et les images, le menu d'options, les
    divers boutons représentant les manipulations possibles et la scrollbar.


    Le principe de ce programme est le suivant. À son exécution, l'utilisateur a le choix de sélectionner une catégorie
    de classement ainsi que le format de classement souhaité. Par la suite, la grille vide apparaît et l'utilisateur a la
    possibilité de faire charger une première image représentant l'objet à classer. À l'aide de la souris, l'utilisateur
    choisit la ligne représentant le palier du dit objet. Une fois que celui-ci est classé, l'utilisateur n'a qu'à faire
    charger le prochain objet à classer. Lorsque tous les objets de la catégorie sont classés, l'utilisateur a le choix
    de prendre une capture d'écran de sa liste completée ou de sauvegarder son travail afin de pouvoir le modifier
    ultérieurement. Les images d'une catégorie doivent se trouver dans un dossier de fichiers nommé
    "Catégorie_(NOM DE LA CATÉGORIE)" se trouvant dans le dossier du projet et chacune des images doit être nommée
    "(ARTISTE ou AUTEUR)_(NOM)".

    """
    def __init__(self):
        super().__init__()

        # Scrollbar :
        self.main_frame = Frame(self)
        self.main_frame.pack(fill='both', expand=1)
        self.my_canvas = Canvas(self.main_frame)
        self.my_canvas.pack(side='left', fill='both', expand=1)
        self.my_scrollbar = Scrollbar(self.main_frame, orient='vertical', command=self.my_canvas.yview)
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.second_frame = Frame(self.my_canvas)
        self.my_canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        # Canvas :
        self.canvas_tier_list = CanvasTierList(self.second_frame)
        self.canvas_tier_list.grid(sticky=NSEW)
        # self.canvas_tier_list.pack(side='left', fill='both', expand=1)
        self.canvas_tier_list.bind('<Button-1>', self.selectionner_clic_gauche)
        self.canvas_tier_list.bind('<Button-3>', self.selectionner_clic_droit)

        # Fenêtre centrée sur l'écran :
        self.eval('tk::PlaceWindow . center')
        largeur = self.canvas_tier_list.winfo_width()
        hauteur = self.canvas_tier_list.winfo_height()
        self.my_canvas.configure(width=largeur, height=hauteur)
        self.my_canvas.configure(scrollregion=(0, 0, largeur, hauteur))

        # Titre :
        self.title("Tier List")

        # Positions/paliers source/cible :
        self.position_source = None
        self.position_cible = None
        self.palier_source = None
        self.palier_cible = None

        # Catégorie de la Tier List (nom du dossier) :
        self.categorie = None

        # Modèle de la Tier List :
        self.modele = None

        # Menu :
        self.menubar = Menu(self)

        # Menu pour sauvegarder le progrès :
        self.sauvegarde_menu = Menu(self.menubar, tearoff=0)
        self.sauvegarde_menu.add_command(label="Sauvegarder", command=self.sauvegarder)
        self.sauvegarde_menu.add_command(label="Dernière sauvegarde", command=self.charger_sauvegarde)
        self.menubar.add_cascade(label='Fichier', menu=self.sauvegarde_menu)

        # Menu pour changer de catégorie :
        self.categorie_menu = Menu(self.menubar, tearoff=0)
        self.files = [f for f in os.listdir() if os.path.isdir(f)]
        self.liste_categories = []
        for nom in self.files:
            if "Catégorie_" in nom:
                categorie_raccourcie = nom.lstrip("Catégorie_")
                self.liste_categories.append(categorie_raccourcie)
                self.categorie_menu.add_radiobutton(label=categorie_raccourcie,
                                                    command=lambda t=nom: self.choisir_categorie(t))
        self.menubar.add_cascade(label='Catégorie', menu=self.categorie_menu)

        # Menu pour choisir le modèle de la Tier List :
        self.modele_menu = Menu(self.menubar, tearoff=0)
        liste_modeles = ["K-POP", "K-POP 2.0", "Classique", "Autre"]
        for modele in liste_modeles:
            self.modele_menu.add_radiobutton(label=modele, command=lambda t=modele: self.choisir_modele(t))
        self.menubar.add_cascade(label='Modèle', menu=self.modele_menu)

        self.config(menu=self.menubar)

        # Dictionnaire des artistes et de leurs chansons :
        self.dictionnaire_artistes_chansons = self.lecture_fichier_texte()[0]

        # Liste des artistes :
        self.liste_artistes = self.lecture_fichier_texte()[1]
        self.artistes_utilises = []

        # Dictionnaire des images en fonction de leurs positions :
        self.dictionnaire_images = {}

        # Dictionnaire des titres des chansons en fonction de leurs positions :
        self.dictionnaire_chansons = {}

        # Dictionnaire du nombre de chansons par palier :
        self.nombre_chansons_par_palier = {}

        # Dictionnaire des numéros de lignees occupées par chaque palier :
        self.dictionnaire_positions_par_palier = {}

        # Boutton pour placer une nouvelle chanson :
        self.boutton = Button(self.second_frame, text='Prochaine chanson', command=self.nouvelle_chanson, bg='#57a83e',
                              fg='white', bd=3, font=f'Arial {self.canvas_tier_list.taille+1} bold', anchor='center')
        
        # Boutton pour enregistrer la Tier List :
        self.capture = Button(self.second_frame, text='Enregistrer', command=self.screenshot, bg='#1d3fdb', fg='white',
                              bd=3, font=f'Arial {self.canvas_tier_list.taille+1} bold', anchor='center')

        # Compteur de chansons restantes :
        self.compteur = 0
        self.label_compteur = Label(self.second_frame, font=f'Arial {self.canvas_tier_list.taille+1} bold',
                                    anchor='center', bg='white')

        # Message d'accueil :
        self.message_bienvenue = Label(self.second_frame, text="MENU",
                                       font=f'Techno {self.canvas_tier_list.taille+4} bold',
                                       fg='white', bg='#434343')
        # self.message_bienvenue.pack()
        self.message_bienvenue.place(x=self.canvas_tier_list.winfo_width()/2, y=self.canvas_tier_list.winfo_height()/2,
                                     anchor='center')
        self.config(width=self.canvas_tier_list.winfo_width()/2, height=self.canvas_tier_list.winfo_height()/2)
        self.canvas_tier_list['bg'] = '#434343'

        self.changement = False

    def selectionner_clic_gauche(self, event):
        if self.modele is not None:
            ligne = event.y // self.canvas_tier_list.n_pixels_par_case
            colonne = event.x // self.canvas_tier_list.n_pixels_par_case
            position = Position(ligne, colonne)
            # print(f"Position : {position}")
            # print(f"Dictionnaire images : {self.dictionnaire_images}")
            if self.position_source is None:
                # Aucune image choisie; choix de position source
                palier = None
                for i in self.dictionnaire_positions_par_palier:
                    if position.ligne in self.dictionnaire_positions_par_palier[i]:
                        palier = i
                # print(f"Palier : {palier}")
                palier_non_vide = self.dictionnaire_images[palier] != []
                position_non_vide = False
                for sequence in self.dictionnaire_images[palier]:
                    if type(sequence[1]) is tuple:
                        if position.ligne in sequence[1] and position.colonne in sequence[1]:
                            position_non_vide = True
                            break
                    else:
                        if position == sequence[1]:
                            position_non_vide = True
                            break
                position_dans_tableau = position.colonne >= 2

                if palier_non_vide and position_non_vide and position_dans_tableau:
                    # Choix d'une des images qui sont sur l'écran
                    self.position_source = position
                    # Choix palier source :
                    for i in self.dictionnaire_positions_par_palier:
                        if self.position_source.ligne in self.dictionnaire_positions_par_palier[i]:
                            self.palier_source = i
                    # print(f"Position source : {self.position_source}")
                    # print(f"Palier source : {self.palier_source}")
                    # Marque l'image sélectionnée en rouge
                    self.canvas_tier_list.selectionner_chanson(self.position_source)
                    chanson = ''
                    for sequence in self.dictionnaire_chansons[self.palier_source]:
                        if type(sequence[1]) is tuple:
                            if (self.position_source.ligne in sequence[1] and
                                    self.position_source.colonne in sequence[1]):
                                chanson = sequence[0]
                                break
                        else:
                            if sequence[1] == self.position_source:
                                chanson = sequence[0]
                                break
                    self.affichage_titre_chanson_au_complet(chanson, self.position_source)

            elif position.ligne != self.canvas_tier_list.ligne_boutton:
                # Une image déjà choisie; choix de position cible
                if position.ligne not in self.dictionnaire_positions_par_palier[self.palier_source]:
                    # Position cible valide :
                    self.position_cible = position
                    # Choix palier cible :
                    for i in self.dictionnaire_positions_par_palier:
                        if self.position_cible.ligne in self.dictionnaire_positions_par_palier[i]:
                            self.palier_cible = i
                    # print(f"Position cible : {self.position_cible}")
                    # print(f"Palier cible : {self.palier_cible}")
                    self.canvas_tier_list.delete('contour')
                    self.canvas_tier_list.delete('nom_complet')
                    if self.palier_source == self.canvas_tier_list.nombre_paliers:
                        # Stockage en mémoire de l'image en position source :
                        image = self.dictionnaire_images[self.palier_source][0][0]
                        chanson = self.dictionnaire_chansons[self.palier_source][0][0]
                        # Ajout de cette image et de la colonne de la position cible dans la liste correspondante à la
                        # ligne de la position cible dans le dictionnaire d'images :
                        self.dictionnaire_images[self.palier_cible].append([image, self.position_cible])
                        self.dictionnaire_chansons[self.palier_cible].append([chanson, self.position_cible])
                        # Initialisation de la liste correpondante à la ligne de la position source à une liste vide:
                        self.dictionnaire_images[self.palier_source] = []
                        self.dictionnaire_chansons[self.palier_source] = []
                        # print(f"Dictionnaire d'images : {self.dictionnaire_images}")
                        # Ajout d'une chanson sur le palier correspondant à la ligne de la position cible :
                        self.nombre_chansons_par_palier[self.palier_cible] += 1
                        # print(f"Nombre de chansons par palier : {self.nombre_chansons_par_palier}")
                    else:
                        for sequence in self.dictionnaire_images[self.palier_source]:
                            if sequence[1] == self.position_source:
                                # print(f"Séquence : {sequence}")
                                # Stockage en mémoire de l'image en position source :
                                image = sequence[0]
                                chanson = ""
                                couple_a_enlever = []
                                for couple in self.dictionnaire_chansons[self.palier_source]:
                                    if couple[1] == self.position_source:
                                        chanson = couple[0]
                                        couple_a_enlever = couple
                                # Ajout de cette image et de la colonne de la position cible dans la liste
                                # correspondante à la ligne de la position cible dans le dictionnaire d'images :
                                self.dictionnaire_images[self.palier_cible].append(
                                    [image, self.position_cible])
                                self.dictionnaire_chansons[self.palier_cible].append(
                                    [chanson, self.position_cible])

                                # Réinitialisation de la liste correpondante à la ligne de la position source :
                                self.dictionnaire_images[self.palier_source].remove(sequence)
                                self.dictionnaire_chansons[self.palier_source].remove(couple_a_enlever)
                                # Suppression d'une chanson sur le palier correspondant à la ligne de la position
                                # source :
                                self.nombre_chansons_par_palier[self.palier_source] -= 1
                                # Ajout d'une chanson sur le palier correspondant à la ligne de la position cible :
                                self.nombre_chansons_par_palier[self.palier_cible] += 1
                                # print(f"Nombre de chansons par palier : {self.nombre_chansons_par_palier}")
                    # Correction du nombre de lignes par palier :
                    self.correction_paliers()
                    # Mise à jour de l'affichage du canvas :
                    self.actualiser_images()
                    # print(f"Dictionnaire d'images : {self.dictionnaire_images}")
                    # print(f"Dictionnaire de chansons : {self.dictionnaire_chansons}")
                    # Réinitialisation des positions source et cible :
                    self.position_source = None
                    self.position_cible = None
                    self.palier_source = None
                    self.palier_cible = None

            elif position.colonne == self.canvas_tier_list.nombre_colonnes-1:
                self.position_cible = position
                # Choix palier cible :
                for i in self.dictionnaire_positions_par_palier:
                    if self.position_cible.ligne in self.dictionnaire_positions_par_palier[i]:
                        self.palier_cible = i
                # print(f"Position cible : {self.position_cible}")
                # print(f"Palier cible : {self.palier_cible}")
                self.canvas_tier_list.delete('contour')
                self.canvas_tier_list.delete('nom_complet')
                for sequence in self.dictionnaire_images[self.palier_source]:
                    if sequence[1] == self.position_source:
                        # print(f"Séquence : {sequence}")
                        # Stockage en mémoire de l'image en position source :
                        couple_a_enlever = []
                        for couple in self.dictionnaire_chansons[self.palier_source]:
                            if couple[1] == self.position_source:
                                couple_a_enlever = couple

                        # Réinitialisation de la liste correpondante à la ligne de la position source :
                        self.dictionnaire_images[self.palier_source].remove(sequence)
                        self.dictionnaire_chansons[self.palier_source].remove(couple_a_enlever)
                        # Suppression d'une chanson sur le palier correspondant à la ligne de la position source :
                        self.nombre_chansons_par_palier[self.palier_source] -= 1
                        # print(f"Nombre de chansons par palier : {self.nombre_chansons_par_palier}")
                # Correction du nombre de lignes par palier :
                self.correction_paliers()
                # Mise à jour de l'affichage du canvas :
                self.actualiser_images()
                # Réinitialisation des positions source et cible :
                self.position_source = None
                self.position_cible = None
                self.palier_source = None
                self.palier_cible = None

    def selectionner_clic_droit(self, event):
        if self.modele is not None:
            ligne = event.y // self.canvas_tier_list.n_pixels_par_case
            colonne = event.x // self.canvas_tier_list.n_pixels_par_case
            position = Position(ligne, colonne)

            if self.position_source is not None:
                if position == self.position_source:
                    self.position_source = None
                    self.palier_source = None
                    self.canvas_tier_list.delete('contour')
                    self.canvas_tier_list.delete('nom_complet')

    def dessiner_images(self):
        self.canvas_tier_list.actualiser(self.modele)

        if self.changement:
            # Détermination de la taille et de la position de la fenêtre sur l'écran :
            largeur = int(self.canvas_tier_list['width']) + 1
            hauteur = int(self.canvas_tier_list['height'])
            self.my_canvas.configure(width=largeur - 15, height=hauteur)
            self.my_canvas.configure(scrollregion=(0, 0, largeur, hauteur))
            if hauteur >= 981:
                hauteur = 981
            self.geometry(f"{largeur + 23}x{hauteur + 6}+0+0")
        self.changement = False

        # Parcourt les lignes sur lesquelles sont déjà placées les images :
        for palier in self.dictionnaire_images:
            if not self.dictionnaire_images[palier] == []:
                if palier == self.canvas_tier_list.nombre_paliers:
                    # Image vient d'apparaître
                    # Stockage en mémoire de l'image de et de la chanson :
                    album = self.dictionnaire_images[palier][0][0]
                    chanson = self.dictionnaire_chansons[palier][0][0]
                    # Dessin de l'image :
                    self.canvas_tier_list.create_image(2 * self.canvas_tier_list.n_pixels_par_case,
                                                       self.canvas_tier_list.ligne_boutton *
                                                       self.canvas_tier_list.n_pixels_par_case,
                                                       image=album, tags='image', anchor='nw')

                    # Affichage du titre de la chanson :
                    chanson_raccourcie = self.raccourcissement_chanson(chanson)
                    longueur_chanson = self.calibrage_longueur_rectangle(chanson_raccourcie)

                    centre_x = 2.5 * self.canvas_tier_list.n_pixels_par_case
                    centre_y = (self.canvas_tier_list.ligne_boutton+0.85) * self.canvas_tier_list.n_pixels_par_case

                    hgx_rectangle = centre_x - (longueur_chanson / 2)
                    hgy_rectangle = (self.canvas_tier_list.ligne_boutton+0.77) * self.canvas_tier_list.n_pixels_par_case
                    bdx_rectangle = centre_x + (longueur_chanson / 2)
                    bdy_rectangle = (self.canvas_tier_list.ligne_boutton+0.95) * self.canvas_tier_list.n_pixels_par_case

                    self.canvas_tier_list.create_rectangle(hgx_rectangle, hgy_rectangle, bdx_rectangle, bdy_rectangle,
                                                           fill='yellow', width=0, tags='image')

                    self.canvas_tier_list.create_text(centre_x, centre_y,
                                                      text=f'{chanson_raccourcie}', fill='black', tags='image',
                                                      font=f'Arial {self.canvas_tier_list.taille} bold')

                else:

                    # Images sur le tableau
                    limite = (self.canvas_tier_list.nombre_colonnes - 2)

                    # Parcourt les listes contenant l'image et le numéro de colonne correspondant au numéro de la ligne:
                    for i in range(self.nombre_chansons_par_palier[palier]):
                        indice = i//limite

                        # Stockage en mémoire de l'image de et de la chanson :
                        album = self.dictionnaire_images[palier][i][0]
                        chanson = self.dictionnaire_chansons[palier][i][0]

                        # Dessin de l'image :
                        self.canvas_tier_list.create_image(((2+i)-(limite * indice)) *
                                                           self.canvas_tier_list.n_pixels_par_case,
                                                           self.dictionnaire_positions_par_palier[palier][indice] *
                                                           self.canvas_tier_list.n_pixels_par_case,
                                                           image=album, tags='image', anchor='nw')

                        # Affichage du titre de la chanson :
                        chanson_raccourcie = self.raccourcissement_chanson(chanson)
                        longueur_chanson = self.calibrage_longueur_rectangle(chanson_raccourcie)

                        centre_x = ((2.5 + i)-(limite * indice)) * self.canvas_tier_list.n_pixels_par_case
                        centre_y = ((self.dictionnaire_positions_par_palier[palier][indice] + 0.85) *
                                    self.canvas_tier_list.n_pixels_par_case)

                        hgx_rectangle = centre_x - (longueur_chanson / 2)
                        hgy_rectangle = ((self.dictionnaire_positions_par_palier[palier][indice] + 0.77) *
                                         self.canvas_tier_list.n_pixels_par_case)
                        bdx_rectangle = centre_x + (longueur_chanson / 2)
                        bdy_rectangle = ((self.dictionnaire_positions_par_palier[palier][indice] + 0.95) *
                                         self.canvas_tier_list.n_pixels_par_case)

                        self.canvas_tier_list.create_rectangle(hgx_rectangle, hgy_rectangle, bdx_rectangle,
                                                               bdy_rectangle, fill='yellow', width=0, tags='image')

                        self.canvas_tier_list.create_text(centre_x, centre_y,
                                                          text=f'{chanson_raccourcie}', fill='black', tags='image',
                                                          font=f'Arial {self.canvas_tier_list.taille} bold')

                        nouvelle_ligne = self.dictionnaire_positions_par_palier[palier][indice]
                        nouvelle_colonne = ((2+i)-(limite * indice))
                        nouvelle_position = Position(nouvelle_ligne, nouvelle_colonne)
                        # print(f"Nouvelle position : {nouvelle_position}")
                        # Mise à jour du nouveau numéro de colonne de l'image :
                        self.dictionnaire_images[palier][i][1] = nouvelle_position
                        # print(self.dictionnaire_images[palier])

                        # Mise à jour du numéro de colonne de la chanson correspondante :
                        self.dictionnaire_chansons[palier][i][1] = nouvelle_position
                        # print(self.dictionnaire_chansons[palier])

    def raccourcissement_chanson(self, chanson):
        font = tkfont.Font(family="Arial", size=self.canvas_tier_list.taille, weight="bold")
        longueur_chanson = font.measure(chanson) + 5
        while longueur_chanson > self.canvas_tier_list.n_pixels_par_case:
            chanson = chanson[:-1]
            longueur_chanson = font.measure(chanson) + 5
        return chanson

    def calibrage_longueur_rectangle(self, chanson):
        font = tkfont.Font(family="Arial", size=self.canvas_tier_list.taille, weight="bold")
        longueur_chanson = font.measure(chanson) + 5
        return longueur_chanson

    def affichage_titre_chanson_au_complet(self, chanson, position):
        longueur_chanson = self.calibrage_longueur_rectangle(chanson)

        centre_x = (position.colonne + 0.5) * self.canvas_tier_list.n_pixels_par_case
        centre_y = (position.ligne + 0.85) * self.canvas_tier_list.n_pixels_par_case

        hgx_rectangle = centre_x - (longueur_chanson / 2)
        hgy_rectangle = (position.ligne + 0.77) * self.canvas_tier_list.n_pixels_par_case
        bdx_rectangle = centre_x + (longueur_chanson / 2)
        bdy_rectangle = (position.ligne + 0.95) * self.canvas_tier_list.n_pixels_par_case

        self.canvas_tier_list.create_rectangle(hgx_rectangle, hgy_rectangle, bdx_rectangle,
                                               bdy_rectangle, fill='yellow', width=0, tags='nom_complet')

        self.canvas_tier_list.create_text(centre_x, centre_y, text=f'{chanson}', fill='black',
                                          tags='nom_complet', font=f'Arial {self.canvas_tier_list.taille} bold')

    def nouvelle_chanson(self):
        if self.menubar.index(3) is not None and self.menubar.index(2) is not None and self.categorie is not None:
            # Catégorie choisie; impossible de changer une fois la première chanson est appelée :
            self.modele_menu.destroy()
            self.menubar.delete(3)
            self.categorie_menu.destroy()
            self.menubar.delete(2)
        while (len(self.liste_artistes) != 0 and self.dictionnaire_images[self.canvas_tier_list.nombre_paliers] == []
               and self.position_source is None):
            # Liste des artistes est non vide
            # Choix du premier artiste :
            artiste = self.liste_artistes[0]
            if artiste not in self.artistes_utilises:
                self.artistes_utilises.append(artiste)
            if len(self.dictionnaire_artistes_chansons[artiste]) == 0:
                # Aucune chanson de l'artiste restante à classer
                # Supression de l'artiste :
                self.liste_artistes = self.liste_artistes[1:]
                try:
                    # Choix prochain artiste :
                    artiste = self.liste_artistes[0]
                except IndexError:
                    self.compteur = 0
                    break
            # Choix première chanson de l'artiste :
            chanson = self.dictionnaire_artistes_chansons[artiste][0]
            self.compteur -= 1
            # Ouverture image correspondante à la chanson :
            try:
                image = Image.open(f"{self.categorie}/{artiste}_{chanson}.jpg")
            except FileNotFoundError:
                try:
                    image = Image.open(f"{self.categorie}/{artiste}_{chanson}.png")
                except FileNotFoundError:
                    messagebox.showerror(title="Image introuvable!", message="Ajoutez des images manquantes!")
                    break
            # Supression de la chanson choisie de la liste :
            self.dictionnaire_artistes_chansons[artiste].pop(0)
            image = image.resize((self.canvas_tier_list.n_pixels_par_case, self.canvas_tier_list.n_pixels_par_case))
            image_tk = ImageTk.PhotoImage(image)
            position_arrivee = Position((self.canvas_tier_list.nombre_lignes - 1), 2)
            # Ajout image dans le dictionnaire d'images à la dernière ligne :
            self.dictionnaire_images[self.canvas_tier_list.nombre_paliers].append([image_tk, position_arrivee])
            # Ajout chanson dans le dictionnaire d'images à la dernière ligne :
            self.dictionnaire_chansons[self.canvas_tier_list.nombre_paliers].append([chanson, position_arrivee])
            # Mise à jour de l'affichage du canvas :
            self.actualiser_images()
            print(f"Dictionnaires des artistes et de leurs chansons : {self.dictionnaire_artistes_chansons}")
            break
        if len(self.liste_artistes) == 0:
            # Listes des artistes est vide
            if len(self.dictionnaire_artistes_chansons) == 0:
                # Dictionnaire des artistes et des chansons est vide (aucune catégorie choisie)
                messagebox.showerror(title="ERREUR", message="Veillez sélectionner une catégorie!")
            else:
                # Dictionnaire des artistes et des chansons n'est pas vide (toutes les chansons de la catégorie ont été
                # classées)
                messagebox.showinfo(title="Félicitations!", message="Toutes les chansons ont été classées avec succès!")

    def actualiser_images(self):
        # Mise à jour de la position des widgets :
        self.positionnement_widgets()
        # Mise à jour des images :
        self.canvas_tier_list.delete('image')
        self.dessiner_images()

    def remplissage_fichier_texte(self):
        arret = False
        print(f"Veuillez choisir une catégorie parmi : {self.liste_categories}")
        categorie = input("Catégorie : ")
        while categorie not in self.liste_categories:
            if categorie == "x":
                exit()
            else:
                print(f"Veuillez choisir une catégorie parmi : {self.liste_categories}")
                categorie = input("Catégorie : ")
        fichier_texte = open(f'Catégorie_{categorie}/Liste_artistes-chansons.txt', 'w')
        while not arret:
            artiste = input("Artiste : ")
            if artiste == 'x':
                break
            fichier_texte.write(f"{artiste} : ")
            chanson = input("Chanson : ")
            if chanson != 'x':
                fichier_texte.write(f"{chanson}")
            while chanson != 'x':
                chanson = input("Chanson : ")
                if chanson != 'x':
                    fichier_texte.write(" | ")
                    fichier_texte.write(f"{chanson}")
                else:
                    fichier_texte.write(f"\n")
        fichier_texte.close()

    def lecture_fichier_texte(self):
        dictionnaire = {}
        liste = []
        try:
            fichier_texte = open(f"{self.categorie}/Liste_artistes-chansons.txt", "r")
            ligne_artiste = fichier_texte.readline()
            while ligne_artiste != "":
                ligne_artiste = ligne_artiste.rstrip("\n")
                artiste = ""
                for caractere in ligne_artiste:
                    if caractere == " ":
                        ligne_artiste = ligne_artiste.lstrip(f"{artiste} : ")
                        if "_" in ligne_artiste:
                            ligne_artiste = ligne_artiste.lstrip("_")
                        break
                    artiste += caractere
                dictionnaire[artiste] = []
                liste.append(artiste)

                ligne_artiste = ligne_artiste.split(" | ")
                for chanson in ligne_artiste:
                    dictionnaire[artiste].append(chanson)

                ligne_artiste = fichier_texte.readline()
            fichier_texte.close()
            return dictionnaire, liste
        except FileNotFoundError:
            return dictionnaire, liste

    def screenshot(self):
        box = (self.canvas_tier_list.winfo_rootx()+1, self.canvas_tier_list.winfo_rooty()+1,
               self.canvas_tier_list.winfo_rootx() + self.canvas_tier_list.winfo_width()-2,
               self.canvas_tier_list.winfo_rooty() + self.canvas_tier_list.winfo_height() -
               self.canvas_tier_list.n_pixels_par_case-2)
        grab = ImageGrab.grab(bbox=box)
        grab.save(f'{self.categorie}/TierListCompletée.png')

    def correction_paliers(self):
        for palier in range(self.canvas_tier_list.nombre_paliers):
            if palier != self.canvas_tier_list.nombre_paliers and self.dictionnaire_images[palier] != []:
                limite_colonnes = self.canvas_tier_list.nombre_colonnes - 2
                nombre_colonnes = self.nombre_chansons_par_palier[palier]
                lignes_par_palier = self.canvas_tier_list.dictionnaire_lignes_par_palier[palier]

                indice_longueur = 0
                for numero in self.dictionnaire_positions_par_palier:
                    if numero == (palier + 1):
                        break
                    if len(self.dictionnaire_positions_par_palier[numero]) > 1:
                        indice_longueur += (len(self.dictionnaire_positions_par_palier[numero])-1)

                if nombre_colonnes > (limite_colonnes * lignes_par_palier):
                    self.canvas_tier_list.nombre_lignes += 1
                    self.canvas_tier_list.dictionnaire_lignes_par_palier[palier] += 1
                    self.dictionnaire_positions_par_palier[palier].append(palier+indice_longueur+1)
                    for i in range(palier+1, self.canvas_tier_list.nombre_paliers+1):
                        for j in range(len(self.dictionnaire_positions_par_palier[i])):
                            self.dictionnaire_positions_par_palier[i][j] += 1
                    self.changement = True

                elif (limite_colonnes * lignes_par_palier) - nombre_colonnes >= limite_colonnes:
                    self.canvas_tier_list.nombre_lignes -= 1
                    self.canvas_tier_list.dictionnaire_lignes_par_palier[palier] -= 1
                    dernier_indice = (len(self.dictionnaire_positions_par_palier[palier]) - 1)
                    self.dictionnaire_positions_par_palier[palier].pop(dernier_indice)
                    for i in range(palier+1, self.canvas_tier_list.nombre_paliers+1):
                        for j in range(len(self.dictionnaire_positions_par_palier[i])):
                            self.dictionnaire_positions_par_palier[i][j] -= 1
                    self.changement = True

        # Mise à jour de la ligne du boutton :
        self.canvas_tier_list.ligne_boutton = self.canvas_tier_list.nombre_lignes - 1
        # print(f"Nombre lignes : {self.canvas_tier_list.nombre_lignes}")
        # print(f"Dictionnaire lignes par palier : {self.canvas_tier_list.dictionnaire_lignes_par_palier}")
        # print(f"Dictionnaire positions par palier : {self.dictionnaire_positions_par_palier}")
        # print(f"Ligne boutton : {self.canvas_tier_list.ligne_boutton}")

    def choisir_categorie(self, categorie):
        self.categorie = categorie
        self.dictionnaire_artistes_chansons = self.lecture_fichier_texte()[0]
        print(self.dictionnaire_artistes_chansons)
        self.liste_artistes = self.lecture_fichier_texte()[1]
        categorie_raccourcie = categorie.lstrip("Catégorie_")
        self.title(f"Tier List {categorie_raccourcie}")
        for artiste in self.dictionnaire_artistes_chansons:
            liste_chansons = self.dictionnaire_artistes_chansons[artiste]
            self.compteur += len(liste_chansons)

    def choisir_modele(self, modele):
        self.canvas_tier_list['bg'] = 'white'
        self.message_bienvenue.destroy()
        # Mise à jour du modèle :
        self.modele = modele
        # Mise à jour de la dimenstion et du tableau :
        self.canvas_tier_list.etablir_dimension(modele)
        self.canvas_tier_list.actualiser(self.modele)
        # Positionnement des widgets :
        self.positionnement_widgets()
        # Initialisation des dictionnaires :
        for i in range(self.canvas_tier_list.nombre_paliers + 1):
            self.dictionnaire_images[i] = []
        for i in range(self.canvas_tier_list.nombre_paliers + 1):
            self.dictionnaire_chansons[i] = []
        for i in range(self.canvas_tier_list.nombre_paliers + 1):
            self.nombre_chansons_par_palier[i] = 0
        for i in range(self.canvas_tier_list.nombre_paliers + 1):
            self.dictionnaire_positions_par_palier[i] = [i]
        # Détermination de la taille et de la position de la fenêtre sur l'écran :
        largeur = int(self.canvas_tier_list['width']) + 1
        hauteur = int(self.canvas_tier_list['height'])
        self.my_canvas.configure(width=largeur - 15, height=hauteur)
        self.my_scrollbar.pack(side='right', fill='y')
        self.my_canvas.configure(scrollregion=(0, 0, largeur, hauteur))
        if hauteur >= 981:
            hauteur = 981
        self.geometry(f"{largeur + 23}x{hauteur + 6}+0+0")

    def sauvegarder(self):
        if self.categorie is not None and self.modele is not None:
            if messagebox.askokcancel(title="Sauvegarde demandée",
                                      message="L'ancienne sauvergarde sera perdue. Sauvegarder le progrès actuel?"):
                self.enregistrement_informations()
        else:
            messagebox.showerror(title="ERREUR", message="Veillez sélectionner une catégorie et un modèle!")

    def enregistrement_informations(self):
        fichier_texte = open(f'{self.categorie}/Dernière_sauvegarde.txt', 'w')
        fichier_texte.write(f"Dictionnaire_artistes_chansons : {self.dictionnaire_artistes_chansons}\n")
        fichier_texte.write(f"Liste des artistes : {self.liste_artistes}\n")
        fichier_texte.write(f"Liste des artistes utilisés : {self.artistes_utilises}\n")
        fichier_texte.write(f"Dictionnaire de chansons : {self.dictionnaire_chansons}\n")
        fichier_texte.write(f"Dictionnaire du nombre de chansons par palier : {self.nombre_chansons_par_palier}\n")
        fichier_texte.write(
            f"Dictionnaire des numéros de lignes occupées par chaque palier : "
            f"{self.dictionnaire_positions_par_palier}\n")
        fichier_texte.write(
            f"Dictionnaire des lignes par palier : {self.canvas_tier_list.dictionnaire_lignes_par_palier}\n")
        fichier_texte.write(f"Nombre de lignes : {self.canvas_tier_list.nombre_lignes}\n")
        fichier_texte.write(f"Nombre de colonnes : {self.canvas_tier_list.nombre_colonnes}\n")
        fichier_texte.write(f"Nombre de paliers : {self.canvas_tier_list.nombre_paliers}\n")
        fichier_texte.write(f"Lignes des bouttons : {self.canvas_tier_list.ligne_boutton}\n")
        fichier_texte.write(f"Modèle : {self.modele}\n")
        fichier_texte.close()

    def charger_sauvegarde(self):
        if self.categorie is not None:
            try:
                self.geometry(f"{50}x{50}+0+0")
                self.canvas_tier_list['bg'] = 'white'
                self.message_bienvenue.destroy()

                fichier_texte = open(f'{self.categorie}/Dernière_sauvegarde.txt', 'r')
                ligne = fichier_texte.readline().rstrip("\n")
                self.dictionnaire_artistes_chansons = (
                    ast.literal_eval(ligne.lstrip("Dictionnaire_artistes_chansons : ")))
                # print(self.dictionnaire_artistes_chansons)
                ligne = fichier_texte.readline().rstrip("\n")
                self.liste_artistes = ast.literal_eval(ligne.lstrip("Liste des artistes : "))
                # print(self.liste_artistes)
                ligne = fichier_texte.readline().rstrip("\n")
                self.artistes_utilises = ast.literal_eval(ligne.lstrip("Liste des artistes utilisés : "))
                # print(self.artistes_utilises)
                ligne = fichier_texte.readline().rstrip("\n")
                self.dictionnaire_chansons = ast.literal_eval(ligne.lstrip("Dictionnaire de chansons : "))
                # print(self.dictionnaire_chansons)
                ligne = fichier_texte.readline().rstrip("\n")
                self.nombre_chansons_par_palier = ast.literal_eval(ligne.lstrip
                                                                   ("Dictionnaire du nombre de chansons par palier : "))

                ligne = fichier_texte.readline().rstrip("\n")
                self.dictionnaire_positions_par_palier = (
                    ast.literal_eval(ligne.lstrip("Dictionnaire des numéros de lignees occupées par chaque palier : ")))

                ligne = fichier_texte.readline().rstrip("\n")
                self.canvas_tier_list.dictionnaire_lignes_par_palier = (
                    ast.literal_eval(ligne.lstrip("Dictionnaire des lignes par palier : ")))

                ligne = fichier_texte.readline().rstrip("\n")
                self.canvas_tier_list.nombre_lignes = int(ligne.lstrip("Nombre de lignes : "))

                ligne = fichier_texte.readline().rstrip("\n")
                self.canvas_tier_list.nombre_colonnes = int(ligne.lstrip("Nombre de colonnes : "))

                ligne = fichier_texte.readline().rstrip("\n")
                self.canvas_tier_list.nombre_paliers = int(ligne.lstrip("Nombre de paliers : "))

                ligne = fichier_texte.readline().rstrip("\n")
                self.canvas_tier_list.ligne_boutton = int(ligne.lstrip("Lignes des bouttons : "))

                ligne = fichier_texte.readline().rstrip("\n")
                self.modele = ligne.lstrip("Modèle : ")

                fichier_texte.close()

                for i in range(self.canvas_tier_list.nombre_paliers + 1):
                    self.dictionnaire_images[i] = []
                image = None
                for numero in self.dictionnaire_chansons:
                    if not self.dictionnaire_chansons[numero] == []:
                        for sequence in self.dictionnaire_chansons[numero]:
                            chanson = sequence[0]
                            for artiste in self.artistes_utilises:
                                try:
                                    image = Image.open(f"{self.categorie}/{artiste}_{chanson}.jpg")
                                    break
                                except FileNotFoundError:
                                    try:
                                        image = Image.open(f"{self.categorie}/{artiste}_{chanson}.png")
                                        break
                                    except FileNotFoundError:
                                        continue
                            image = image.resize((self.canvas_tier_list.n_pixels_par_case,
                                                  self.canvas_tier_list.n_pixels_par_case))
                            image_tk = ImageTk.PhotoImage(image)
                            self.dictionnaire_images[numero].append([image_tk, sequence[1]])
                # print(self.dictionnaire_images)
                # print(self.canvas_tier_list.dictionnaire_lignes_par_palier)
                # print(self.dictionnaire_images)
                self.compteur = 0
                for artiste in self.liste_artistes:
                    liste_chansons = self.dictionnaire_artistes_chansons[artiste]
                    self.compteur += len(liste_chansons)

                # Mise à jour du tableau :
                self.canvas_tier_list.dessiner_tableau(self.modele)
                # Positionnement des widgets :
                self.positionnement_widgets()
                # Ajout d'images :
                self.dessiner_images()
                # Supression des options de catégorie et de modèle :
                self.modele_menu.destroy()
                self.menubar.delete(3)
                self.categorie_menu.destroy()
                self.menubar.delete(2)
                # Détermination de la taille et de la position de la fenêtre sur l'écran :
                largeur = int(self.canvas_tier_list['width'])
                hauteur = int(self.canvas_tier_list['height']) + 1
                self.my_canvas.configure(width=largeur - 15, height=hauteur)
                self.my_scrollbar.pack(side='right', fill='y')
                self.my_canvas.configure(scrollregion=(0, 0, largeur, hauteur))
                if hauteur >= 981:
                    hauteur = 981
                self.geometry(f"{largeur + 23}x{hauteur + 6}")
            except FileNotFoundError:
                categorie = self.categorie.lstrip("Catégorie_")
                messagebox.showerror(title="ERREUR", message=f"Aucune sauvegarde pour la catégorie "
                                                             f"{categorie}!")
        else:
            messagebox.showerror(title="ERREUR", message="Veillez sélectionner une catégorie!")

    def positionnement_widgets(self):
        self.boutton.place(x=self.canvas_tier_list.n_pixels_par_case,
                           y=self.canvas_tier_list.ligne_boutton * self.canvas_tier_list.n_pixels_par_case + 15,
                           anchor='center')
        self.capture.place(x=self.canvas_tier_list.n_pixels_par_case,
                           y=(self.canvas_tier_list.ligne_boutton + 1) * self.canvas_tier_list.n_pixels_par_case - 15,
                           anchor='center')
        self.label_compteur['text'] = f"{self.compteur} chansons restantes"
        self.label_compteur.place(x=self.canvas_tier_list.n_pixels_par_case * 3 + 20,
                                  y=(self.canvas_tier_list.ligne_boutton + 1) *
                                  self.canvas_tier_list.n_pixels_par_case -
                                  self.canvas_tier_list.n_pixels_par_case // 2 - 5)


if __name__ == "__main__":
    TierList = FenetreTierList()
    TierList.remplissage_fichier_texte()
    # print(TierList.canvas_tier_list.dictionnaire_lignes_par_palier)
    # print(TierList.dictionnaire_artistes_chansons)
    # print(TierList.liste_artistes)
    # print(TierList.files)
