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

---

## TP2 - étude de cas CoNLL-2003



