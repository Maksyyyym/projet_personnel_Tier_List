"""
\file main.py
\brief Fichier main du programme qui permet l'affichage de l'interface et qui assûre la programmation événementielle
\author IFT-1004
\version 1.0
"""

from interface import FenetreTierList

if __name__ == '__main__':
    fenetre = FenetreTierList()
    fenetre.mainloop()
