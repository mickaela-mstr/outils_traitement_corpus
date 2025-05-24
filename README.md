# Projet outils_traitement_de_corpus

---

## TP1 - étude de cas CoNLL-2003

### Quelle type de tâche propose CoNLL 2003 ?

CoNLL 2003 propose une tâche de reconnaissance d'entités nommées. C’est une tâche de séquence d’étiquetage où l’on doit repérer et classifier les entités nommées dans un texte, comme :

* des personnes (PER),
* des organisations (ORG),
* des lieux (LOC)

### Quel type de données y a-t-il dans CoNLL 2003 ?

Les données de CoNLL 2003 sont des phrases de textes journalistiques pré-annotées.

Chaque mot est accompagné de :

* son POS tag (part-of-speech),
* son chunk tag (groupe syntaxique),
* son tag NER (type d'entité ou "O" si ce n'est pas une entité).

Format typique :

```
Germany  NNP  B-NP  B-LOC  
's       POS  B-NP  O  
representative  NN  I-NP  O  
...
```

### À quel besoin répond CoNLL 2003 ?

CoNLL 2003 répond au besoin de développer, tester et comparer des modèles de NER, de standardiser l'évaluation grâce à un benchmark public et de stimuler la recherche en traitement automatique du langage naturel sur des tâches de type information extraction. C’est un benchmark de référence dans la communauté du NLP.

### Quels types de modèles ont été entraînés sur CoNLL 2003 ?

Initialement il y avait CRF (Conditional Random Fields), SVM et des modèles à base de règles + lexiques. Aujourd’hui on retrouve LSTM-BiLSTM + CRF, mais aussi des transformers pré-entraînés (ex : BERT, RoBERTa, Flair) et des fine-tuning de modèles comme `bert-base-cased` sur le corpus.

### Est-ce un corpus monolingue ou multilingue ?

CoNLL 2003 est bilingue. Il contient des données en anglais (Reuters RCV1) et en allemand (Eci Multilingual Newswire Corpus). Mais dans la plupart des benchmarks modernes, seule la version anglaise est utilisée.

### Définition des besoins du projet

Ce projet s'inscrit dans le cadre d’un besoin d’analyse automatique de contenu textuel descriptif dans l’univers du jeu vidéo, et plus précisément dans le domaine de la classification d'entités fictives à partir de descriptions naturelles. L’objectif est de démontrer qu’un modèle de traitement automatique du langage peut apprendre à associer un texte riche en informations encyclopédiques à une catégorie précise.

Le sujet traité concerne la classification automatique des Pokémon en fonction de leur type (Eau, Feu, Plante, etc.) à partir de leurs descriptions textuelles.

La tâche réalisée est une tâche de classification supervisée multi-classes à une seule étiquette : à chaque description correspond exactement un type. Il s'agit donc de construire un modèle qui apprend à associer chaque entrée textuelle à une sortie catégorielle parmi 15 classes possibles.

Le projet exploite des données textuelles descriptives issues de Poképédia, un site collaboratif francophone dédié à l’univers Pokémon. Chaque entrée est constituée d’un texte descriptif et du type associé à un Pokémon.

Les données ont été récupérées manuellement via un script de scraping. Les descriptions concernent les 151 premiers Pokémon (génération 1). Ces données sont librement accessibles en ligne sur Poképédia, qui fonctionne sous licence Creative Commons BY-NC-SA, ce qui permet une utilisation à des fins non commerciales dans un cadre académique ou pédagogique.

---

## TP2 - Récupération du corpus

Le corpus a été constitué à partir d’un script de scraping. Ce script récupère automatiquement les descriptions textuelles et les types associés aux 151 Pokémon de la première génération, directement depuis le site Poképédia.

La page de départ est la liste officielle des Pokémon de la première génération. Le script utilise `requests` pour charger la page, puis `BeautifulSoup` pour parser le HTML et extraire les liens vers les pages individuelles de chaque Pokémon. Pour chaque entrée, le script visite la page dédiée au Pokémon et en extrait tous les paragraphes de la section de contenu principal (`<div id="mw-content-text">`), à partir du deuxième paragraphe afin d’éviter les résumés non pertinents.

Le nom, le type (par défaut le premier type affiché dans le tableau de la page principale) et la description complète sont extraits et stockés dans un dictionnaire, puis rassemblés dans un DataFrame Pandas. Enfin, l’ensemble des données est exporté dans un fichier CSV (`pokedex.csv`) qui sert de base au corpus utilisé dans les étapes ultérieures du projet (visualisation, augmentation, entraînement, etc.).

---

## TP3 - Visualisation du corpus et statistiques

Une série d'analyses textuelles a été menée sur les descriptions des 151 premiers Pokémon. Le corpus a d'abord été nettoyé en retirant la ponctuation, les mots non alphabétiques ainsi qu'une liste personnalisée de stopwords spécifiques aux descriptions afin de se concentrer sur le vocabulaire réellement distinctif.

Un nuage de mots global a été généré pour observer les termes les plus fréquents dans l'ensemble du corpus. On y retrouve des mots liés aux capacités physiques, à l’environnement naturel ou au comportement des pokémons. Par la suite, un nuage de mots a été produit pour chaque type afin de mettre en évidence les spécificités lexicales propres à chacun. Ces visualisations montrent clairement que chaque type possède un champ lexical caractéristique : le type Feu met en avant des mots comme "brûle" ou "flamme", tandis que le type Eau fait ressortir des termes comme "nage" ou "vague".

En complément, un barplot des vingt mots les plus fréquents a été réalisé pour l’ensemble du corpus, ainsi que des barplots spécifiques à chaque type, afin de quantifier visuellement les dominantes lexicales. Enfin, des statistiques générales ont été calculées : on compte en moyenne 271 mots par description, pour une longueur textuelle moyenne d’environ 2337 caractères, et le corpus couvre 15 types différents.

Les différentes visualisations sont disponibles au format png dans le dossier `figures/`.

---

## TP4 - Augmentation des données et choix du modèle

### Augmentation du corpus par back-translation

Pour enrichir le dataset initial, une technique d’augmentation de données par back-translation a été appliquée. Chaque description de Pokémon a d'abord été traduite du français vers l’anglais, puis de l’anglais vers le français en utilisant la librairie `deep-translator` et le service Google Translate. Afin de respecter la limite de 5000 caractères imposée par l’API de traduction, les descriptions trop longues ont été tronquées à la fin d'une phrase complète.

Ce procédé a permis de générer une version reformulée de chaque description tout en conservant l'information de type associée. L’ensemble des descriptions originales et traduites a ensuite été fusionné pour créer un fichier final enrichi (`pokedex_aug_backtranslate.csv`).

### Choix du modèle et de l’architecture

La tâche consiste à prédire le type d’un Pokémon à partir de sa description textuelle, ce qui relève d’une tâche de classification de texte à une seule étiquette. Pour cela, une architecture de type encodeur transformer a été choisie, car elle est particulièrement adaptée à la représentation sémantique de textes en entrée. Plus précisément, le modèle préentraîné `camembert-base` a été retenu. Il s’agit d’un modèle de type RoBERTa, entraîné sur de larges corpus francophones. Il est utilisé ici avec une couche de classification pour apprendre à associer chaque description à l’un des 15 types de Pokémon du corpus.

---

## TP5 - Fine-tuning du modèle

Pour la tâche de classification du type d’un Pokémon à partir de sa description, le modèle `camembert-base` a été entraîné à l’aide du framework Hugging Face Transformers. La classification s’effectue parmi 15 types différents. Les données utilisées combinent les descriptions originales du Pokédex et des exemples augmentés par back-translation.

Chaque description a d’abord été tokenisée avec le tokenizer CamemBERT, puis les étiquettes textuelles (types) ont été encodées en entiers. Le corpus a été divisé en un jeu d'entraînement et un jeu de test (80/20). Le modèle `CamembertForSequenceClassification` a ensuite été entraîné sur 5 époques avec une fonction de perte adaptée à la classification multi-classes.

Le modèle finetuné est sauvegardé dans le dossier `results/model/`, avec le tokenizer et le label encoder, afin de pouvoir faire des prédictions ultérieures sur de nouvelles descriptions. Les performances sont suivies à chaque époque avec des métriques de précision (`accuracy`) et de score F1 pondéré, ce dernier étant utilisé comme critère de sauvegarde du meilleur modèle.

---

### TP6 - Évaluation du modèle

### Analyse des résultats (premier essai)

Le modèle obtient 100% de rappel uniquement pour la classe "Eau"et toutes les autres classes ont une précision, un rappel et un f1-score nuls. L’accuracy globale est exactement le ratio de la classe "Eau" dans le test set (16/61 ≈ 26.2%). Cela signifie que le modèle prédit "Eau" pour toutes les entrées, car c’est la classe la plus représentée dans les données.

Pourquoi cela se produit? Car le dataset est fortement déséquilibré. Par exemple si "Eau" est 30% du corpus et "Glace" 1%, le modèle préfère prédire "Eau" car ça minimise la perte (surtout sans pondération des classes). Le Trainer de Hugging Face n’applique pas de poids de classes automatiquement dans `CrossEntropyLoss`. Enfin, un petit corpus amplifie l'effet de déséquilibre, certaines classes peuvent même ne jamais apparaître dans l’entraînement ou test.

### Analyse des résultats (deuxième essai)

Le modèle `camembert-base` finetuné pour la classification des types Pokémon a été évalué sur un jeu de test représentant 20 % du corpus, après un équilibrage des classes par sur-échantillonnage. Ce rééquilibrage a permis de corriger un fort biais initial du modèle qui tendait à prédire systématiquement la classe majoritaire , ce qui se traduisait par des scores F1 quasi nuls pour toutes les autres classes.

Après oversampling, les résultats montrent une nette amélioration des performances. L’accuracy atteint 91,8 %, et le F1-score macro-pondéré dépasse les 0.91, ce qui indique une bonne généralisation, y compris sur les types moins fréquents. La majorité des classes ont été correctement reconnues, et même les types rares comme "Spectre", "Dragon" ou "Roche" ont obtenu des scores de F1 très satisfaisants. Les quelques types absents du jeu de test (par exemple "Fée", "Glace", "Combat") n’ont pas été évalués, ce qui est normal compte tenu de la petite taille du jeu de test.

Une matrice de confusion a été générée pour visualiser les prédictions du modèle par rapport aux étiquettes réelles. Elle confirme que les erreurs de classification sont rares et que les prédictions sont bien réparties entre les différentes classes. Ces résultats validés indiquent que le modèle est maintenant suffisamment entrainé pour être utilisé sur de nouvelles descriptions.




