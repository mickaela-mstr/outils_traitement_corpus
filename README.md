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

répondre aux questions concernant le projet.

---

## TP2 - Récupération du corpus

---

## TP3 - Visualisation du corpus et statistiques

Une série d'analyses textuelles a été menée sur les descriptions des 151 premiers Pokémon. Le corpus a d'abord été nettoyé en retirant la ponctuation, les mots non alphabétiques ainsi qu'une liste personnalisée de stopwords spécifiques aux descriptions afin de se concentrer sur le vocabulaire réellement distinctif.

Un nuage de mots global a été généré pour observer les termes les plus fréquents dans l'ensemble du corpus. On y retrouve des mots liés aux capacités physiques, à l’environnement naturel ou au comportement des pokémons. Par la suite, un nuage de mots a été produit pour chaque type afin de mettre en évidence les spécificités lexicales propres à chacun. Ces visualisations montrent clairement que chaque type possède un champ lexical caractéristique : le type Feu met en avant des mots comme "brûle" ou "flamme", tandis que le type Eau fait ressortir des termes comme "nage" ou "vague".

En complément, un barplot des vingt mots les plus fréquents a été réalisé pour l’ensemble du corpus, ainsi que des barplots spécifiques à chaque type, afin de quantifier visuellement les dominantes lexicales. Enfin, des statistiques générales ont été calculées : on compte en moyenne 271 mots par description, pour une longueur textuelle moyenne d’environ 2337 caractères, et le corpus couvre 15 types différents.

Les différentes visualisations sont disponibles au format png dans le dossier `résultats/`.






