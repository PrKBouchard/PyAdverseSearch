#  PyAdverseSearch

## Table des matières

[Présentation de PyAdverseSearch](#1---présentation-de-pyadversesearch)

[Structure du projet et utilisation](#2---structure-du-projet-et-utilisation)

[Fonctionnement détaillé des classes](#3---fonctionnement-détaillé-des-classes)

[Outils et modules utilitaires](#recommandation-du-chat--outils-et-utilitaires)

[Fonctions Privées et protégées](#4--fonctions-privées-et-protégées)

[Pour les developpeurs](#5--pour-les-developpeurs)

[Jeux intégrés disponibles](#6---jeux-intégrés-disponibles)

[Interaction homme VS IA](#7---interaction-homme-vs-ia-jouer-contre-minimax)

[Monte Carlo](#8---algorithmes-supplémentaires--monte-carlo)

[Tests unitaires complets](#9---tests-unitaires-complets)

[Documentation Sphinx](#10---documentation-sphinx)

[Conclusion](#conclusion)


## 1 - Présentation de PyAdverseSearch
### Motivation et objectifs

PyAdverseSearch a été développée pour répondre à un besoin croissant dans le domaine de l'intelligence artificielle : disposer d'une bibliothèque Python flexible et modulaire dédiée à l'implémentation d'algorithmes d'exploration adverse. Face à l'absence d'outils spécialisés combinant simplicité d'utilisation et performance, PyAdverseSearch offre une solution complète pour les chercheurs, étudiants et développeurs souhaitant travailler avec des algorithmes de prise de décision dans des environnements compétitifs.

Les objectifs principaux de cette bibliothèque sont :

- Fournir une plateforme unifiée pour l'implémentation et l'analyse d'algorithmes d'exploration adverse
- Proposer une architecture modulaire facilitant l'extension et la personnalisation
- Simplifier le processus de développement d'agents intelligents pour divers environnements de jeu

### Introduction à PyAdverseSearch

PyAdverseSearch est une bibliothèque Python spécialisée dans la programmation d'algorithmes d'exploration adverse. Elle fournit une infrastructure complète pour modéliser des jeux à information complète et implémenter des stratégies de prise de décision intelligentes. Particulièrement adaptée aux jeux à somme nulle entre deux joueurs, cette bibliothèque permet de simuler, analyser et optimiser des stratégies de jeu grâce à différents algorithmes d'exploration.

La bibliothèque s'articule autour de plusieurs classes fondamentales, chacune ayant un rôle spécifique dans l'architecture globale :


## 2 - Structure du projet et utilisation

### Organisation du code source

PyAdverseSearch adopte une structure de projet claire et organisée pour faciliter la navigation, la compréhension et l'extension du code :

    PyAdverseSearch/
    ├── class/
    │   ├── game.py
    │   ├── minimax.py
    │   ├── node.py
    │   ├── state.py
    │   └── tree.py
    └── README.md

- Le répertoire **class/** contient les différentes classes fondamentales de la bibliothèque.
- Le document **README.md** est le documentation du projet PyAdverseSearch.

### Installation et prérequis

#### Prérequis

Avant d'installer PyAdverseSearch, assurez-vous que votre environnement répond aux exigences suivantes :

- **Python** : Version 3.9 ou supérieure
- **Bibliothèques de base** :
  - NumPy (>= 1.19.0) : pour les manipulations de tableaux et les calculs
  - Matplotlib (>= 3.3.0) : pour les fonctionnalités de visualisation
  - pytest (>= 6.0.0) : pour exécuter les tests unitaires (uniquement nécessaire pour le développement)

#### Installation standard

La méthode la plus simple pour installer PyAdverseSearch est d'utiliser pip, le gestionnaire de paquets Python :

    pip install pyadversesearch

Cette commande installera automatiquement la dernière version stable de la bibliothèque ainsi que toutes ses dépendances.

#### Installation depuis la source

Pour les utilisateurs souhaitant accéder à la version de développement ou contribuer au projet, l'installation depuis le dépôt source est recommandée :

    # Cloner le dépôt
    git clone https://github.com/PrKBouchard/PyAdverseSearch.git

    # Se déplacer dans le répertoire du projet
    cd PyAdverseSearch

    # Installer en mode développement
    pip install -e .

L'installation en mode développement (`-e`) permet de modifier le code source et de voir les changements appliqués sans avoir à réinstaller la bibliothèque.

#### Vérification de l'installation

Pour vérifier que l'installation s'est correctement déroulée, exécutez :

    import pyadversesearch
    print(pyadversesearch.__version__)

Si aucune erreur n'apparaît et que la version s'affiche, l'installation est réussie.


### Guide d'utilisation rapide

L'utilisation de PyAdverseSearch se déroule généralement en quatre étapes principales :

1. **Définir un jeu spécifique** en étendant la classe Game et en implémentant ses méthodes abstraites.
2. **Créer une représentation d'état** en étendant la classe State pour modéliser la configuration du jeu.
3. **Instancier un algorithme d'exploration** comme Minimax en lui fournissant le jeu configuré.
4. **Utiliser l'algorithme** pour déterminer les meilleures actions à chaque étape du jeu.

#### Exemple d'utilisation générique

Voici comment implémenter et utiliser PyAdverseSearch pour un jeu personnalisé :

1. **Définir le jeu et l'état** : Créez des sous-classes de Game et State qui implémentent les règles spécifiques de votre jeu.

2. **Configurer l'algorithme d'exploration** : Instanciez un algorithme comme Minimax avec votre jeu.

3. **Utiliser l'algorithme pour prendre des décisions** : À chaque tour, utilisez l'algorithme pour déterminer le meilleur coup.

Cette approche modulaire permet d'adapter facilement la bibliothèque à différents jeux tout en réutilisant les algorithmes d'exploration implémentés.

### Personnalisation et extension

PyAdverseSearch est conçu pour être hautement extensible. Vous pouvez :

- **Créer de nouveaux jeux** en étendant la classe Game
- **Implémenter de nouveaux algorithmes d'exploration** en suivant le modèle des classes existantes
- **Personnaliser les fonctions d'évaluation** pour améliorer la prise de décision
- **Développer des visualisations personnalisées** pour analyser le comportement des algorithmes
- **Optimiser les algorithmes existants** pour des jeux spécifiques

La bibliothèque fournit des interfaces claires et une documentation détaillée pour faciliter ces extensions.

## 3 - Fonctionnement détaillé des classes

### Classe Game

La classe Game sert de fondation pour définir la structure et les règles d'un jeu à deux joueurs. C'est une classe abstraite qui doit être étendue pour implémenter un jeu spécifique.

#### Responsabilités principales

- Définir les règles du jeu
- Gérer l'initialisation de l'état du jeu
- Déterminer les actions légales à chaque état
- Calculer les états résultant de l'application d'actions
- Identifier les états terminaux et leurs valeurs d'utilité

#### Méthodes clés

- `game_possible_actions()` : 
- `game_is_terminal()` : 
- `game_utility()` : 
- `game_heuristic()` : 
- `get_winner()` : 


### Classe Minimax

La classe Minimax implémente l'algorithme Minimax classique, une technique fondamentale pour l'exploration adverse dans les jeux à deux joueurs à somme nulle.

#### Principe de fonctionnement

L'algorithme Minimax repose sur un principe simple mais puissant :

1. À chaque état du jeu, l'algorithme considère toutes les actions légales et les états qui en résultent.
2. Pour les nœuds MAX (joueur actif), il choisit l'action qui maximise la valeur minimale que l'adversaire peut forcer.
3. Pour les nœuds MIN (adversaire), il suppose que l'adversaire choisira l'action qui minimise la valeur maximale que le joueur actif peut obtenir.
4. Ce processus est appliqué récursivement jusqu'à atteindre des états terminaux ou une profondeur maximale.
5. Les valeurs des états terminaux ou profonds sont ensuite propagées vers la racine pour déterminer la meilleure action.

#### Responsabilités principales

- Implémenter l'algorithme Minimax récursif
- Déterminer la meilleure action à partir d'un état donné
- Évaluer les états non-terminaux à une profondeur maximale
- Construire implicitement un arbre d'exploration
- Propager les valeurs des feuilles vers la racine

#### Méthodes clés

- `minimax_decision()` : 
- `max_value()` : 
- `min_value()` : 


### Classe Node

La classe Node représente un nœud dans l'arbre d'exploration. Elle associe un état de jeu à des informations relatives à l'exploration et aux relations de parenté dans l'arbre.

#### Responsabilités principales

- Encapsuler un état de jeu
- Maintenir les relations parent-enfant dans l'arbre
- Stocker des informations d'évaluation
- Faciliter la navigation dans l'arbre d'exploration
- Conserver des statistiques d'exploration pour certains algorithmes

#### Méthodes clés
- `expand()` : 
- `is_terminal()` : 
- `display()` :



### Classe State

La classe State représente une configuration complète du jeu à un moment donné. Elle encapsule toutes les informations nécessaires pour décrire entièrement l'état du jeu.

#### Responsabilités principales

- Maintenir la représentation du plateau de jeu
- Identifier le joueur actif
- Conserver l'historique des mouvements
- Fournir des méthodes de duplication et de comparaison d'états
- Représenter de manière efficace l'information du jeu

#### Méthodes clés

- `possible_actions()` : 
- `is_terminal()` : 
- `utility()` : 
- `evaluate()` : 
- `apply_action()` : 
- `generate_successors()` : 
- `display()` :



### Classe Tree

La classe Tree gère la structure globale de l'arbre d'exploration et fournit des méthodes pour sa manipulation.

#### Responsabilités principales

- Maintenir la structure arborescente avec son nœud racine
- Fournir des méthodes de construction et d'expansion de l'arbre
- Faciliter la recherche et la navigation dans l'arbre
- Gérer la sérialisation et la persistance de l'arbre
- Optimiser l'utilisation de la mémoire

#### Méthodes clés

- `build_tree()` : 
- `display()` : 



### Outils et utilitaires

En plus des classes principales, PyAdverseSearch fournit notamment un module utilitaire pour faciliter le développement et la visualisation.

#### Module visualization.py

Le module visualization.py fournit des outils pour :

- Visualiser les arbres d'exploration
- Représenter graphiquement les états du jeu
- Animer le processus d'exploration
- Générer des diagrammes d'analyse
- Exporter des visualisations pour documentation

L'utilisation judicieuse de ces modules permet d'améliorer significativement l'efficacité du développement et la qualité des analyses réalisées avec PyAdverseSearch.

## 4- Fonctions Privées et protégées

Dans PyAdverseSearch, certaines fonctions sont nommées avec un ou deux tirets bas en préfixe pour indiquer leur usage restreint, selon les conventions de Python.

Les fonctions protégées (préfixées par un seul _) sont utilisées à l'intérieur des classes ou par des sous-classes. Elles ne sont pas destinées à être appelées directement par les utilisateurs de la bibliothèque. C’est notamment le cas de plusieurs méthodes dans la classe State comme _possible_actions, _apply_action, _is_terminal, ou _evaluate, qui sont conçues pour être utilisées uniquement par les algorithmes internes (comme Minimax) ou l’arbre d’exploration. De même, des méthodes comme _expand dans Node sont réservées à la construction automatique de l’arbre.

Une fonction privée (préfixée par __) est utilisée dans la classe GameTree. Il s'agit de __build_tree, qui gère la construction complète de l’arbre de recherche. Elle est volontairement masquée pour éviter toute modification ou appel extérieur, car elle contient des opérations critiques.

L’adoption de ces conventions permet de séparer clairement ce qui relève de la logique interne et ce qui peut être utilisé ou redéfini par les développeurs. Cela contribue à la stabilité, la lisibilité et la sécurité du code dans l’ensemble du projet.

## 5- Pour les developpeurs 

## Guide de développement pour PyAdverseSearch

Ce fichier README s'adresse aux développeurs souhaitant reprendre, étendre ou améliorer la bibliothèque PyAdverseSearch. Contrairement au guide principal destiné aux utilisateurs, ce document fournit une vue détaillée de l'architecture interne, des conventions de conception, ainsi que des indications précises pour développer de nouveaux jeux, algorithmes ou fonctionnalités compatibles avec le framework.

## Présentation générale

PyAdverseSearch est structurée pour permettre une exploration adverse efficace dans des jeux à deux joueurs à somme nulle. Elle s’appuie sur des classes abstraites à spécialiser pour chaque jeu, ainsi qu’un arbre d’exploration et des algorithmes comme Minimax. La bibliothèque est conçue pour être facilement extensible, tout en respectant une architecture bien définie.

#### Classes principales et leurs rôles

- **Classe Game** : Représente un jeu et ses règles. Elle définit la logique fondamentale du jeu, notamment les actions légales, les transitions d'état, et les conditions de fin de partie. Cette classe est abstraite et doit être étendue pour implémenter un jeu spécifique.

- **Classe State** : Modélise un état du jeu à un moment précis. Elle encapsule toutes les informations nécessaires pour décrire complètement la configuration du jeu : positions des pièces, joueur actif, historique des coups, etc.

- **Classe Node** : Représente un nœud dans l'arbre d'exploration. Chaque nœud est associé à un état du jeu et maintient des références vers son parent et ses enfants, ainsi que des informations d'évaluation.

- **Classe Tree** : Gère la structure arborescente utilisée pour l'exploration des possibilités de jeu. Elle facilite la construction, la navigation et la manipulation de l'arbre de recherche.

- **Classe Minimax** : Implémente l'algorithme Minimax, une technique fondamentale d'exploration adverse qui alterne entre la maximisation du gain pour un joueur et la minimisation pour l'autre, permettant de déterminer la meilleure action à entreprendre.

Ces composants travaillent ensemble pour permettre une analyse approfondie des jeux et la sélection de mouvements optimaux dans divers contextes.


## Structure interne du projet

Le dossier principal contient un répertoire class/ qui regroupe les classes essentielles : State, Game, Node, Tree, Minimax, ainsi qu'une interface SearchAlgorithm. Le dossier test/ contient des implémentations concrètes de jeux comme le Tic Tac Toe ou le Puissance 4. Ces exemples servent à la fois de démonstration et de base pour les tests automatisés ou manuels.

## Conception orientée objet et hiérarchie

La classe State est abstraite et doit être étendue pour chaque jeu. Elle définit les éléments nécessaires à la modélisation d’un état de jeu : le plateau (board), l’état parent, et une référence à l’instance de la classe Game pour appeler dynamiquement les fonctions du jeu. Chaque état doit donc implémenter les méthodes publiques possible_actions, apply_action, is_terminal, et evaluate, qui définissent respectivement les actions valides, la transition d’un état à un autre, la condition de fin de partie, et l’évaluation heuristique.

La classe Game est le point d’entrée utilisateur. Elle permet d’associer des fonctions spécifiques à un jeu donné à une instance globale, en centralisant les règles, la fonction de fin, l’utilité et l’heuristique. Elle construit automatiquement un arbre d’exploration à partir de l’état initial, via la classe GameTree.

La classe Node représente chaque nœud de l’arbre de jeu. Elle encapsule un état, ses enfants, le joueur,  son parent, un identifiant unique et sa profondeur. La construction de l’arbre est déléguée à GameTree, dont la méthode privée __build_tree() s’occupe de générer récursivement tous les nœuds à partir de la racine.

L’algorithme Minimax est implémenté dans sa propre classe. Il propose trois modes d'exécution : classique (sans limite), avec profondeur maximale, et avec limite de temps. La méthode principale choose_best_move permet de déterminer le meilleur coup à jouer à partir d’un état donné.

## Conventions de nommage et encapsulation

Dans l’architecture de PyAdverseSearch, des conventions sont utilisées pour marquer les fonctions internes ou critiques :

Les méthodes préfixées par un seul tiret bas (_) sont dites protégées. Elles sont destinées à être utilisées uniquement en interne, soit par la classe elle-même, soit par ses sous-classes. Par exemple, dans la classe State, les méthodes _possible_actions, _apply_action, _is_terminal, _evaluate ou _generate_successors sont appelées par l’arbre d’exploration et les algorithmes, mais ne doivent pas être invoquées directement par l’utilisateur final. Elles assurent une interface cohérente entre les classes internes tout en permettant la spécialisation via des méthodes publiques comme apply_action.

Une seule méthode privée est définie dans le projet : __build_tree, au sein de la classe GameTree. Le double underscore (__) déclenche un mécanisme de masquage de nom en Python (name mangling) afin de limiter strictement son accès à la classe elle-même. Cette méthode étant responsable de la construction complète et récursive de l’arbre, elle est rendue privée pour garantir l'intégrité de la structure et éviter toute manipulation externe non contrôlée.

Ces conventions d'encapsulation permettent de maintenir la séparation entre l'interface utilisateur et l'infrastructure interne, ce qui facilite la maintenance et la robustesse de la bibliothèque.

## Étendre la bibliothèque : ajout d’un nouveau jeu

Pour ajouter un jeu personnalisé, il faut :

Créer une nouvelle sous-classe de State et y implémenter toutes les méthodes obligatoires (possible_actions, apply_action, is_terminal, evaluate).

Définir les fonctions spécifiques au jeu : celles-ci seront passées à la classe Game lors de son instanciation (par exemple, winner_function, utility, heuristic).

Instancier un objet Game avec l’état initial et les fonctions définies.

Vérifier que state.game est bien initialisé (ce lien est crucial pour que les méthodes dynamiques comme _is_terminal ou _evaluate fonctionnent).

Tester le comportement à l’aide de l’algorithme Minimax, en modifiant éventuellement sa profondeur ou sa limite de temps.

## Ajouter un nouvel algorithme d’exploration

L’extension à d’autres algorithmes est également prévue. Il suffit de créer une nouvelle classe héritant de SearchAlgorithm et d’implémenter la méthode choose_best_move(state). L’algorithme peut exploiter l’arbre fourni ou utiliser une autre stratégie (ex. Monte Carlo, Alpha-Beta Pruning, etc.).

Il est conseillé de respecter la structure et les conventions existantes, notamment pour le nommage des paramètres, la gestion du temps et la compatibilité avec les objets State et Game.

## Tests, exemples et recommandations

Les fichiers de test sont situés dans le dossier test/. Ils contiennent des jeux complets comme TicTacToe (state_tictactoe.py) ou Connect 4, ainsi que des fonctions comme generate_tictactoe_game() qui facilitent l’automatisation des tests. Il est recommandé de créer une fonction équivalente pour tout nouveau jeu ajouté.

L’affichage des états est géré par la méthode display() dans chaque sous-classe de State, et peut être personnalisé pour chaque jeu. Des visualisations plus avancées peuvent être ajoutées sous forme de modules externes ou notebooks Jupyter.

## Collaboration et bonnes pratiques

Les contributions au projet se font via GitHub. Chaque fonctionnalité doit être développée sur une branche dédiée. Toute nouvelle classe ou méthode importante doit être documentée. Il est également recommandé de conserver une certaine homogénéité dans les messages de commit, les noms de fichiers et les logs (print("[DEBUG] ...")).

Ce guide vise à fournir aux développeurs toutes les informations nécessaires pour comprendre, utiliser et faire évoluer PyAdverseSearch de manière structurée et efficace.

## 6 - Jeux intégrés disponibles

En plus de la structure modulaire permettant d'ajouter ses propres jeux, PyAdverseSearch intègre déjà plusieurs jeux de démonstration pleinement fonctionnels :

Tic Tac Toe (morpion) : disponible dans test/state_tictactoe.py

Puissance 4 : dans test/state_puissance4.py

Connect 4 : dans test/state_connect4.py

Chaque jeu implémente les méthodes requises (apply_action(), evaluate(), possible_actions()...) en héritant de la classe State, avec des variantes spécifiques du plateau de jeu. Ces fichiers servent à la fois de démonstration et de base pour jouer contre une IA ou exécuter des tests automatiques.

## 7 - Interaction homme vs IA (jouer contre Minimax)

Depuis la branche dev, il est désormais possible de jouer contre l’algorithme Minimax dans plusieurs jeux. Cette fonctionnalité permet à un utilisateur humain d’interagir en temps réel avec l’IA, en alternant les tours et en observant les choix stratégiques effectués par l’algorithme.
Dans le fichier state_tictactoe.py, une première version de cette interaction a été intégrée, offrant la possibilité de simuler un affrontement en console entre un joueur humain et l'algorithme Minimax appliqué au jeu du morpion (Tic Tac Toe).
Cette logique a ensuite été étendue au jeu du Puissance 4. Le test propose une interface utilisateur en ligne de commande où :

Le joueur choisit s’il souhaite commencer la partie ou laisser l’IA jouer en premier.

L’algorithme Minimax est appliqué avec une profondeur configurable (jusqu’à 6).

Les coups possibles sont affichés, et le joueur sélectionne manuellement son option.

La partie progresse jusqu’à ce qu’un état terminal soit atteint (victoire ou match nul).


## 8 - Algorithmes supplémentaires : Monte Carlo

En plus de Minimax, une version expérimentale de l'algorithme Monte Carlo est présente dans le fichier montecarlo.py. Il s'agit d'un algorithme basé sur des simulations répétées aléatoires de parties, permettant d'évaluer les actions non pas par calcul exhaustif, mais par échantillonnage probabiliste.
La méthode principale de cette classe est choose_best_move(state), comme dans Minimax, et elle peut être utilisée de manière interchangeable pour certains jeux.


## 9 - Tests unitaires complets

Le dossier test/ contient des scripts de tests variés :

test_minimax.py : vérifie le bon fonctionnement de l’algorithme Minimax.

test_montecarlo.py : teste les décisions issues de l’algorithme Monte Carlo.

test_state_tictactoe.py, test_state_connect4.py, test_state_puissance4.py : assurent que les jeux implémentés respectent bien les méthodes requises et fonctionnent correctement.

test_full_game_next_move.py : joue une partie complète en alternant IA et coups simulés.

Tous ces tests permettent de s'assurer que les modules du projet restent fonctionnels même après modifications.



## 10 - Documentation Sphinx

PyAdverseSearch dispose d'une documentation technique complète générée avec **Sphinx** et le thème `sphinx-rtd-theme`. Elle couvre l'intégralité des classes, algorithmes et interfaces graphiques du projet.

### Accès rapide à la documentation

La documentation est déjà pré-générée dans le dépôt. Il suffit d'ouvrir directement ce fichier dans un navigateur :

    docs/_build/html/index.html

Sous Windows via PowerShell :

    Start-Process "docs\_build\html\index.html"

Aucune installation supplémentaire n'est nécessaire pour consulter la documentation existante.

---

### Regénérer la documentation (optionnel)

Les étapes ci-dessous sont uniquement nécessaires si vous souhaitez regénérer la documentation après avoir modifié le code source.

### Prérequis

Les dépendances nécessaires sont déjà incluses dans l'environnement virtuel du projet. Pour les installer manuellement :

    pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints

### Structure de la documentation

    docs/
    ├── conf.py              # Configuration Sphinx
    ├── index.rst            # Page d'accueil
    ├── about.rst            # Informations sur le projet
    ├── Makefile             # Build Unix/macOS
    ├── make.bat             # Build Windows
    ├── _static/
    │   └── custom.css       # Personnalisation CSS
    ├── classes/
    │   ├── index.rst
    │   ├── algorithm.rst    # SearchAlgorithm (classe de base)
    │   ├── game.rst         # Game
    │   ├── state.rst        # State (classe abstraite)
    │   ├── node.rst         # Node
    │   ├── tree.rst         # GameTree
    │   ├── minimax.rst      # Minimax
    │   ├── alphabeta.rst    # AlphaBeta
    │   ├── negamax.rst      # NegamaxSolver
    │   ├── montecarlo.rst   # MonteCarlo (MCTS)
    │   ├── mtdf.rst         # MTDf
    │   ├── pnsearch.rst     # PNSearch
    │   └── autosolver.rst   # AutoSolver
    └── interface/
        ├── index.rst
        ├── connect4_gui.rst          # Interface Puissance 4 basique
        ├── connect4_gui_enhanced.rst # Interface Puissance 4 complète
        ├── tictactoe_gui.rst         # Interface Morpion
        ├── reversi.rst               # Interface Reversi (Arcade)
        └── pdf_report.rst            # Générateur de rapport PDF

### Générer la documentation HTML

**Sur Windows :**

    cd docs
    .\make.bat html

Ou directement via Python (recommandé dans un environnement virtuel) :

    cd docs
    python -m sphinx -b html . _build/html

**Sur Linux / macOS :**

    cd docs
    make html


### Autres formats disponibles

Sphinx supporte plusieurs formats de sortie :

| Commande              | Format produit          |
|-----------------------|-------------------------|
| `make html`           | Site web HTML           |
| `make latexpdf`       | PDF via LaTeX           |
| `make epub`           | Livre numérique EPUB    |
| `make text`           | Texte brut              |
| `make linkcheck`      | Vérification des liens  |

### Ajouter de la documentation

Pour documenter une nouvelle classe ou un nouveau module :

1. Ajouter des docstrings au format Sphinx (`:param:`, `:type:`, `:return:`, `:rtype:`) dans le fichier Python.
2. Créer un fichier `.rst` dans `docs/classes/` ou `docs/interface/` :

        .. Ma nouvelle classe
        Mon titre
        =========

        .. automodule:: PyAdverseSearch.classes.ma_classe
           :members:
           :undoc-members:
           :show-inheritance:

3. Référencer ce fichier dans le `toctree` du fichier `index.rst` parent.
4. Relancer `make html`.

### Conventions de docstrings

Le projet utilise le style Sphinx natif (`:param:` / `:type:` / `:return:`) :

    def ma_methode(self, state, depth):
        """
        Description courte.

        Description longue optionnelle.

        :param state: État courant du jeu.
        :type state: State
        :param depth: Profondeur restante.
        :type depth: int
        :return: Valeur évaluée.
        :rtype: float
        """


## Conclusion

PyAdverseSearch offre une infrastructure complète, flexible et performante pour l'implémentation et l'analyse d'algorithmes d'exploration adverse. Sa conception modulaire permet une adaptation facile à divers jeux et contextes, tandis que ses algorithmes optimisés garantissent des performances satisfaisantes même pour des problèmes complexes.

Que vous soyez chercheur explorant de nouvelles techniques d'intelligence artificielle, étudiant apprenant les fondements de la théorie des jeux, ou développeur intégrant des capacités décisionnelles dans vos applications, PyAdverseSearch fournit les outils nécessaires pour concrétiser vos projets avec efficacité et élégance.

Nous vous encourageons à explorer les exemples fournis, à expérimenter avec vos propres implémentations, et à contribuer au développement continu de cette bibliothèque au sein de la communauté PyAdverseSearch.

## Étudiant-es ayant travaillé sur la librairie

**2025** : Anaïs Dariane Nikiema, Martin Queval, Thibault Stouls, Hugo Vicente, Benjamin Bouquet, Ewan Burasovitch, Mathys Lohézic, Axel Ozange, Mélissa Djenadi

**2026** : James Genitrini, Lucas Hätet, Clément Hubert, Lucas Lablanche, Quentin Laparre, Benjamin Lecomte, Halim Luquet, Ilyes Zaidi
