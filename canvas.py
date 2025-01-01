"""
\file canvas.py
\brief Implémentation du canvas de l'interface graphique (affichage du tableau et des images)
\author Maksym Valigunda
\version 1.0
"""

from tkinter import Canvas, Scrollbar


class CanvasTierList(Canvas):
    def __init__(self, parent, n_pixels_par_case=63, nombre_lignes=1, nombre_colonnes=3):

        # Parent :
        self.parent = parent

        # Nombre de lignes et de colonnes :
        self.nombre_lignes = nombre_lignes
        self.nombre_colonnes = nombre_colonnes

        # Nombre de paliers :
        self.nombre_paliers = nombre_lignes-1

        # Position fixe des bouttons :
        self.ligne_boutton = self.nombre_lignes-1

        # Nombre de pixels par case :
        self.n_pixels_par_case = n_pixels_par_case

        # Police :
        self.taille = self.n_pixels_par_case // 10 + 1

        # Dictionnaire qui contient une liste des positions des lignes en fonction du palier :
        self.dictionnaire_lignes_par_palier = {}
        for i in range(self.nombre_paliers):
            self.dictionnaire_lignes_par_palier[i] = 1

        # Appel du constructeur de la classe de base (Canvas)
        largeur = (self.nombre_colonnes * self.n_pixels_par_case) + self.n_pixels_par_case/2
        hauteur = (self.nombre_lignes * self.n_pixels_par_case)/2
        super().__init__(parent, width=largeur, height=hauteur)

    def etablir_dimension(self, modele):
        self.nombre_colonnes = 20
        if modele == "K-POP":
            self.nombre_lignes = 10
        elif modele == "K-POP 2.0":
            self.nombre_lignes = 15
        elif modele == "Classique":
            self.nombre_lignes = 6
        elif modele == "Autre":
            self.nombre_lignes = 11
        self.nombre_paliers = self.nombre_lignes - 1
        self.ligne_boutton = self.nombre_lignes - 1
        for i in range(self.nombre_paliers):
            self.dictionnaire_lignes_par_palier[i] = 1

    def dessiner_tableau(self, modele):
        indice = 0
        for i in self.dictionnaire_lignes_par_palier:
            texte_x = 0
            texte_y = indice * self.n_pixels_par_case

            points = ''
            nom = ''
            couleur = ''

            if modele == "K-POP":
                if i == 0:
                    couleur = '#DC6384'
                    points = '10'
                    nom = 'LÉGENDAIRE'
                elif i == 1:
                    couleur = '#e06666'
                    points = '9,5'
                    nom = 'PARFAIT'
                elif i == 2:
                    couleur = '#e69138'
                    points = '9'
                    nom = 'ÉMOTIONNEL'
                elif i == 3:
                    couleur = '#ffd966'
                    points = '8,5'
                    nom = 'EXCELLENT'
                elif i == 4:
                    couleur = '#93c47d'
                    points = '8'
                    nom = 'STANDARD'
                elif i == 5:
                    couleur = '#6aa84f'
                    points = '7,5'
                    nom = 'DE QUALITÉ'
                elif i == 6:
                    couleur = '#76a5af'
                    points = '7'
                    nom = 'AGRÉABLE'
                elif i == 7:
                    couleur = '#3d85c6'
                    points = '6,5'
                    nom = 'BIEN'
                elif i == 8:
                    couleur = '#8e7cc3'
                    points = '6'
                    nom = 'LIMITE'

            elif modele == "K-POP 2.0":
                if i == 0:
                    couleur = '#f04357'
                    points = '10'
                    nom = 'LÉGENDAIRE'
                elif i == 1:
                    couleur = '#f04377'
                    points = '9,75'
                    nom = 'PARFAIT'
                elif i == 2:
                    couleur = '#f043bc'
                    points = '9,5'
                    nom = "ÉMOTIONNEL"
                elif i == 3:
                    couleur = '#aa46e3'
                    points = '9,25'
                    nom = "CHEF D'OEUVRE"
                elif i == 4:
                    couleur = '#704fdb'
                    points = '9'
                    nom = 'EXCELLENT'
                elif i == 5:
                    couleur = '#3068e3'
                    points = '8,75'
                    nom = 'TRÈS BON'
                elif i == 6:
                    couleur = '#449fdb'
                    points = '8,5'
                    nom = 'STANDARD'
                elif i == 7:
                    couleur = '#34d6d9'
                    points = '8,25'
                    nom = 'UNIQUE'
                elif i == 8:
                    couleur = '#34d994'
                    points = '8'
                    nom = 'BANGER'
                elif i == 9:
                    couleur = '#34d94d'
                    points = '7,75'
                    nom = 'BON'
                elif i == 10:
                    couleur = '#73d934'
                    points = '7,5'
                    nom = 'ADDICTIF'
                elif i == 11:
                    couleur = '#b3d934'
                    points = '7'
                    nom = 'AGRÉABLE'
                elif i == 12:
                    couleur = '#d9c334'
                    points = '6,5'
                    nom = 'BIEN'
                elif i == 13:
                    couleur = '#d97c34'
                    points = '6'
                    nom = 'LIMITE'

            elif modele == "Classique":
                if i == 0:
                    couleur = '#DC6384'
                    nom = 'S'
                elif i == 1:
                    couleur = '#e06666'
                    nom = 'A'
                elif i == 2:
                    couleur = '#e69138'
                    nom = 'B'
                elif i == 3:
                    couleur = '#ffd966'
                    nom = 'C'
                elif i == 4:
                    couleur = '#93c47d'
                    nom = 'D'

            elif modele == "Autre":
                if i == 0:
                    couleur = '#DC6384'
                    nom = '10'
                elif i == 1:
                    couleur = '#e06666'
                    nom = '9'
                elif i == 2:
                    couleur = '#e69138'
                    nom = '8'
                elif i == 3:
                    couleur = '#ffd966'
                    nom = '7'
                elif i == 4:
                    couleur = '#93c47d'
                    nom = '6'
                elif i == 5:
                    couleur = '#6aa84f'
                    nom = '5'
                elif i == 6:
                    couleur = '#76a5af'
                    nom = '4'
                elif i == 7:
                    couleur = '#3d85c6'
                    nom = '3'
                elif i == 8:
                    couleur = '#8e7cc3'
                    nom = '2'
                elif i == 9:
                    couleur = '#0d8c77'
                    nom = '1'
            for j in range(self.dictionnaire_lignes_par_palier[i]):
                debut_ligne = (indice+j) * self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case

                debut_colonne_paliers = 0
                fin_colonne_palier = 2 * self.n_pixels_par_case

                debut_colonne_lignes = 2 * self.n_pixels_par_case
                fin_colonne_lignes = debut_colonne_lignes + self.n_pixels_par_case * (self.nombre_colonnes - 2)

                # Palier
                self.create_rectangle(debut_colonne_paliers, debut_ligne, fin_colonne_palier, fin_ligne, fill=couleur,
                                      width=1, tags='tableau')
                # Ligne
                self.create_rectangle(debut_colonne_lignes, debut_ligne, fin_colonne_lignes, fin_ligne, fill='#434343',
                                      width=1, tags='tableau')
                if j > 0:
                    # Ligne qui sépare les lignes du palier est masquée
                    self.create_line(debut_colonne_paliers, debut_ligne, fin_colonne_palier, debut_ligne, fill=couleur)
            if modele == "K-POP" or modele == "K-POP 2.0":
                # Cote
                self.create_text((texte_x + 7), (texte_y + 5), text=points, fill='white',
                                 font=f'Arial {self.taille+1} bold', tags='tableau', anchor='nw')
            # Nom palier
            self.create_text((texte_x + self.n_pixels_par_case),
                             (texte_y + self.n_pixels_par_case / 2),
                             text=nom, fill='black', font=f'Arial {self.taille+3}', tags='tableau')
            indice = indice + self.dictionnaire_lignes_par_palier[i]
        # Générateur d'images :
        x1 = 2 * self.n_pixels_par_case
        y1 = (self.ligne_boutton * self.n_pixels_par_case)
        x2 = x1 + self.n_pixels_par_case
        y2 = y1 + self.n_pixels_par_case
        self.create_rectangle(x1, y1, x2, y2, fill='yellow', tags='tableau')
        for i in range(12):
            index = i*5
            self.create_line(x1 + 2 + index, y1 + 2, x2 - 2, y2 - 2 - index, fill='black', width=1, tags='tableau')
            self.create_line(x1 + 2, y1 + 2 + index, x2 - 2 - index, y2 - 2, fill='black', width=1, tags='tableau')

        # Corbeille :
        x1 = (self.nombre_colonnes - 1) * self.n_pixels_par_case
        y1 = (self.ligne_boutton * self.n_pixels_par_case)
        x2 = x1 + self.n_pixels_par_case
        y2 = y1 + self.n_pixels_par_case
        self.create_rectangle(x1, y1, x2, y2, fill='red', tags='tableau')
        self.create_line(x1+5, y1+5, x2-5, y2-5, fill='black', width=3, tags='tableau')
        self.create_line(x2-5, y1+5, x1+5, y2-5, fill='black', width=3, tags='tableau')

    def actualiser(self, modele):
        # Mise à jour du tableau (paliers, lignes, cotes, noms des paliers, générateur d'images, cobeille) :
        self.delete('tableau')
        self.dessiner_tableau(modele)
        # Mise à jour de la taille de la fenêtre :
        nouvelle_largeur = self.nombre_colonnes * self.n_pixels_par_case
        nouvelle_hauteur = self.nombre_lignes * self.n_pixels_par_case
        self.config(width=nouvelle_largeur, height=nouvelle_hauteur)

    def selectionner_chanson(self, position):
        debut_colonne = position.colonne * self.n_pixels_par_case
        debut_ligne = position.ligne * self.n_pixels_par_case
        fin_colonne = debut_colonne + self.n_pixels_par_case
        fin_ligne = debut_ligne + self.n_pixels_par_case
        self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, outline='red', width=3,
                              tags='contour')
