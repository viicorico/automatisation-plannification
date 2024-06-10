# Application de planification automatisée des examens

## À propos 👀
Bienvenue sur le projet **# Application de planification automatisée des examens**
Ce projet vise à développer une application de gestion des emplois du temps pour automatiser la planification des examens universitaires.
L'objectif principal est d'attribuer des horaires et des salles d'examen de manière optimale, en évitant les conflits d'horaires pour les étudiants, en maximisant l'utilisation des ressources disponibles et en respectant diverses contraintes académiques et administratives.

## Algorithmes utilisés 💡

### Coloration des graphes
* Description : La coloration de graphes attribue des couleurs à chaque sommet d'un graphe tel que deux sommets adjacents n'ont pas la même couleur.
* Avantages : Offre une méthodologie structurée pour organiser les tâches, ressources et contraintes temporelles.
* Inconvénients : Le problème est NP-complet, rendant difficile la recherche d'une solution optimale en temps polynomial.
### Algorithme de Welsh-Powell
* Description : Utilisé pour la coloration des graphes, il trie les sommets par ordre décroissant de degrés et attribue des couleurs en conséquence.
* Avantages : Simple et efficace pour minimiser le nombre de couleurs utilisées.
* Inconvénients : Peut ne pas toujours produire la solution optimale.
### Algorithme Génétique
* Description : Utilise une population de solutions pour représenter les plannings, évoluant cette population au fil des générations via sélection, croisement et mutation.
* Avantages : Exploration efficace de l'espace des solutions et adaptabilité aux contraintes spécifiques.
* Inconvénients : Mise en œuvre complexe et dépendance aux paramètres choisis.

## Contraintes
* Contrainte d'Adjacence : Deux matières d'une même filière ne peuvent pas avoir la même horaire.
* Contrainte d'Équilibre : Équilibrer le nombre de matières par session pour minimiser la variance.
* Contrainte de Session : Chaque session a une capacité maximale en termes de places.
* Contrainte de Durée des Examens : La durée de la session doit être au moins égale à la somme des durées de tous les examens qui s'y déroulent.

## Fonctionnement en clair 🤔
- Initialisation de la population de solutions.
- Évolution de la population au fil des générations par sélection des parents, croisement et mutation.
- Évaluation de la variance des solutions pour trouver la meilleure solution valide.
- Itération jusqu'à atteindre une solution satisfaisante ou un nombre maximal d'itérations sans amélioration.

## Installation et exécution 📥⚡
Pour lancer l'application, suivez les étapes ci-dessous :

1. Prérequis : Assurez-vous d'avoir Python et PyQt5 installés sur votre machine.

2. Exécution de l'application :
   Le fichier main.py contient le point d'entrée de l'application. Il initialise l'interface utilisateur développée avec PyQt5, exécute les algorithmes, et lance le processus de planification des examens. Une fois exécutée, l'application génère et affiche le planning optimal pour tous (ou/et l'étudiant) en fonction des contraintes et des données fournies.

## Pour plus de détails 🔍
Le rapport du projet est disponible sous le fichier Rapport_final.pdf

4. * La connexion se fait avec le numéro étudiant de l'élève ainsi que son mot de passe qui se trouve dans le tableau csv/Etudiants.csv.
   * La connexion avec le compte administrateur suit le même principe que la connexion au compte étudiant, les informations se situant dans le tableau csv/Administrateur.csv.
   Celui-ci aura accès à tous les emplois du temps et pourra recherche un emploi du temps spécifique à un élève
