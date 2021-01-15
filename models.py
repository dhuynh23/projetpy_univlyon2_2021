#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/01/2021

@author: laila et david
"""

################################## Déclaration des classes ##################################
#Librairies à charger
import pickle
import re
import string
import collections

# Liste de mots anglais qui ne sont pas utiles à l'analyse des mots
english_stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", 
 "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", 
 "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", 
 "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", 
 "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", 
 "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", 
 "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", 
 "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", 
 "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

class Corpus():
        
    def __init__(self,name, excludeStopWords):
        self.name = name # Nom du corpus
        self.collection = {} # Liste des documents  (dictionnaire)
        self.id2doc = {} # Liste des titres (id) de documents (dictionnaire)
        self.ndoc = 0  # Indice du dernier document inséré
        # Dictionnaire (clé = reddit/arxiv, valeur = liste des mots dans un tableau)
        self.wordsByDoc = {}  #.Par ex: { "reddit": ["mot1", "mot2", "mot3"], "arxiv": ["mot1", "mot6", "mot3"] }
        # Dictionnaire (clé = reddit/arxiv, valeur = liste des mots en chaine (str = string)
        self.wordsStrByDoc = {} # Par ex: { "reddit": "mot1 mot2 mot3", "arxiv": "mot1 mot6 mot3" }
        self.excludeStopWords = excludeStopWords # Booleén True/False pour l'option d'exclusion des stopwords
        
    # Fonction qui permet d'ajouter un document au corpus
    def add_doc(self, doc):
        self.collection[self.ndoc] = doc
        self.id2doc[self.ndoc] = doc.get_title()
        self.ndoc += 1
    
    # Fonction qui permet de récupérer un document depuis son indice
    def get_doc(self, i):
        return self.collection[i]
    
    # Fonction qui permet de récupérer tous les documents
    def get_coll(self):
        return self.collection

    # Fonction qui permet de personnaliser ce qu'affiche un print() d'un objet Corpus
    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)
    
    # Fonction qui permet de personnaliser ce qu'affiche un repr() d'un objet Corpus
    def __repr__(self):
        return self.name

    # Fonction (non utilisée) qui permet de sauvegarder le fichier corpus 
    def save(self,file):
            pickle.dump(self, open(file, "wb" ))
    
    # Retourne tout le corpus en un seul grand texte concaténé et nettoyé
    def get_word_list_from_docType(self, docType):        
        if not docType in self.wordsByDoc: #Si le dictionnaire wordsByDoc ne contient pas de clé reddit/arxiv             
            textConcatene = ''
            for key, value in self.collection.items(): # On parcours chaque document du corpus
                if value.getType() == docType: # On vérifie que pour chaque document, son type (renvoyé par getType()) soit le même que celui passé en parametre (docType)
                    textConcatene = textConcatene + value.text # Si oui, on concatene son contenu dans la variable textConcatene
            textConcateneEtNettoye = self.nettoyer_texte(textConcatene) # textConcatene est maintenant rempli de tous les documents d'un type. On appelle nettoyer_texte pour le nettoyer

            # option des stop words activé ou non
            if (self.excludeStopWords): # Si exclusion, on enleve les mots qui font parti de english_stopwords
                # textConcateneEtNettoye.split() permet de spliter une phrase en x mots
                self.wordsByDoc[docType] = [word for word in textConcateneEtNettoye.split() if word not in english_stopwords]
            else:
                self.wordsByDoc[docType] = [word for word in textConcateneEtNettoye.split()]   

            # On remplit maintenant le dictionnaire wordsStrByDoc à partir du dictionnaire wordsByDoc fraichement rempli 
            # ["mot1", "mot2"] devient "mot1 mot2"
            self.wordsStrByDoc[docType] = ' '.join(word for word in self.wordsByDoc.get(docType))

        return self.wordsByDoc.get(docType)
    
    # Trouve le top x des mots de tout le corpus
    def get_most_common_words(self, topX, docType):
        mots = self.get_word_list_from_docType(docType)
        # On recupere le dictionnaire de mot (du docType reddit ou arxiv) qu'on transforme en objet Collection.Counter
        cc = collections.Counter(mots)
        # Utilisation de la fonction most_common (https://docs.python.org/3/library/collections.html)
        result = cc.most_common(topX)
        # exemple de result : [('mot1', 1143), ('mot2', 966), ('mot3', 762)]
        return result
      
    # Fonction qui prend un texte en entrée et renvoie le texte nettoyé     
    def nettoyer_texte(self,txt):
        # on enleve les retours a la ligne
        clean_txt = txt.lower().replace('\n', ' ')
        
        # Regex (bibliotheque re) pour supprimer les chiffres
        clean_txt = re.sub(r'\d+', '', clean_txt)
        
        # on enleve les url des textes
        clean_txt = re.sub(r"http\S+", "", clean_txt)

        # on enleve la ponctuation (https://stackoverflow.com/questions/18429143/strip-punctuation-with-regex-python)
        clean_txt = ' '.join(word.strip(string.punctuation) for word in clean_txt.split())
        
        return clean_txt
    
    # Donne la fréquence d'un mot dans un type de document cible
    def get_freq_for_a_word(self, mot, docTypeCible):
        return self.wordsByDoc.get(docTypeCible).count(mot)
    
    # Donne la chronologie d'un mot => Date de l'article | Nb d'occurence à cette date 
    def get_word_infos_by_doc(self, mot, docType):
        # J'initialise un dictionnaire Clé (= date) / Valeur (occurence)
        dicoDate={}
        for key, value in self.collection.items(): # On parcours chaque document du corpus
            if value.getType() == docType: # On vérifie que pour chaque document, son type (renvoyé par getType()) soit le même que celui passé en parametre (docType)
                txt = self.nettoyer_texte(value.get_text())
                # J'utilise la bibliothèqe re pour avoir le nb de fois qu'on trouve dans le doc en cours, le mot passé en param
                count = len(re.findall(r'\b%s\b' % re.escape(mot), txt))
                if (count > 0):                    
                    # Si au moins une occurence, on met à jour le dico
                    datestr = value.get_date().strftime("%d/%m/%Y") # On ne veut garder que le jour/mois/année en format string
                    if (datestr in dicoDate):
                        dicoDate[datestr] = dicoDate.get(datestr) + count # Si le cle (date) existe deja, on additione
                    else:
                        dicoDate[datestr] = count
        return dicoDate
                        
class Document():
    
    # constructor
    def __init__(self, date, title, text):
        self.date = date
        self.title = title
        self.text = text
    
    # getters
    
    def get_title(self):
        return self.title
    
    def get_date(self):
        return self.date
        
    def get_text(self):
        return self.text

    def __str__(self):
        return "Document " + self.getType() + " : " + self.title
    
    def __repr__(self):
        return self.title
    
    def getType(self):
        pass
    
# classe fille permettant de modéliser un Document Reddit
#

class RedditDocument(Document):
    
    def __init__(self, date, title, text):        
        Document.__init__(self, date, title, text)

    def getType(self):
        return "reddit"
       
#
# classe fille permettant de modéliser un Document Arxiv
#

class ArxivDocument(Document):
    
    def __init__(self, date, title, text):
        Document.__init__(self, date, title, text)
 
    def getType(self):
        return "arxiv"

