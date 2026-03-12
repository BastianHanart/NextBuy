# NEXT_BUY
## Préambule

Le projet Next_Buy est un projet IA / DATA, avec pour objectif de pouvoir prédire différents éléments liés aux achats dans un supermarché.

Notre but est de comprendre, analyser et interpréter les données d’un supermarché, afin de construire des modèles d’IA permettant de prédire, améliorer et optimiser les ventes du supermarché.

## Installer notre projet

Pour pouvoir utiliser notre projet, il faut d’abord savoir comment l’initialiser correctement.

Après avoir installé tous les fichiers de ce répertoire, ouvrez un terminal et placez-vous à la racine du projet.

Exécutez ensuite les commandes suivantes :

- python3 -m venv Myvenv
- source Myvenv/bin/activate
- pip install -r requirements.txt

Le fichier requirements.txt contient toutes les dépendances nécessaires au projet.

Si cette étape se déroule correctement, alors le projet est initialisé et prêt à être utilisé.

## Utiliser notre projet

Pour accéder à notre dashboard interactif et retrouver toutes les informations importantes, exécutez la commande suivante :

streamlit run dashboard.py

Cela devrait ouvrir automatiquement une page web du type :

localhost:8501

Si la page ne s’ouvre pas automatiquement, ouvrez votre navigateur et tapez dans la barre d’adresse :

localhost:8501
Explorer le code du projet

#### Si vous souhaitez regarder plus en détail notre code, voici les fichiers les plus intéressants à parcourir à l’aide d’un IDE comme VS Code ou Jupyter Notebook.

##### Analyse.ipynb

Ce premier fichier nous a permis de parcourir les différents tableaux afin de détecter les premières erreurs potentielles.

Nous analysons de nombreux éléments qui nous permettent de faire un premier tri important entre les données à conserver et celles à supprimer.

##### Nettoyage.ipynb

Ce fichier permet de comprendre notre cheminement de pensée ainsi que les différentes actions que nous avons réalisées pour nettoyer les données et pouvoir ensuite utiliser au mieux notre fichier CSV (tableau de valeurs).

##### notebook.ipynb

Ce fichier permet de visualiser différents graphiques répondant à 8 questions principales que nous nous sommes posées au début du projet.

##### Reflexion.ipynb

Dans la continuité de notre réflexion, ce fichier nous a servi à noter et expliquer chaque étape du projet.

Il nous permet :

- d’expliquer le projet aux membres du groupe,

- de garder une trace claire du développement,

- et de retrouver facilement chaque élément important du projet.

##### Model_IA_Type_B.ipynb

Ce fichier est dédié au développement et à l’entraînement de nos différents modèles d’IA.

On peut y voir :

- les différentes étapes de recherche,

- les tests d’algorithmes,

- et les méthodes utilisées pour obtenir les meilleures précisions possibles.