import pandas as pd

# Spécifiez le chemin vers votre fichier CSV
fichier_csv = pd.read_csv('Etudiant.csv', header=None)

tableau = fichier_csv.values

# Afficher le tableau
print(tableau)
listeNumeroEtudiant = []
listeNom = []
listeMotDePasse = []
compteur = len(tableau)
for i in range(compteur):
    listeNumeroEtudiant.append(tableau[i][1])
    listeNom.append(tableau[i][0])
    listeMotDePasse.append(tableau[i][2])
    
print(listeNumeroEtudiant)

def rechercherEtu(listeNumeroEtudiants,listeNom,listeMotDePasse,numeroRecherche):
    compteur = len(listeNumeroEtudiants)
    for i in range(compteur):
        if(listeNumeroEtudiants[i]==numeroRecherche):
            return(listeNom[i], listeMotDePasse[i])
    return (-1,-1)

numeroRecherche  = 723156

nom, motdePasse = rechercherEtu(listeNumeroEtudiant, listeNom, listeMotDePasse, numeroRecherche)   

if(nom!= -1 and motdePasse!= -1):
    print(nom,motdePasse)
else:
    print("erreur !")
