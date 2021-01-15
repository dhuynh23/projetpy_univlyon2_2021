# -*- coding: utf-8 -*-

"""
@author: laila et david
"""
#Librairies à charger
from PyQt5 import QtCore, QtGui, QtWidgets # Bibliothèque pour la constructeur de l'interface graphique
from rank_bm25 import BM25Okapi # Bibliothèque pour calculer les score BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer # Bibliothèque pour calculer les score TF-IDF
from tkinter import *
from pandastable import Table # Bibliothèque pour afficher des dataframe panda 
import pandas as pd

# Classe de la 3e fenetre : celle qui permet d'afficher les tableaux de résultats (via pandastable)
class Ui_ResultsFrame(Frame):
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('600x400+200+100')         
        self.frame = Frame(self.main)
        self.frame.pack(fill=BOTH,expand=1)
        return
    # A chaque changement de tableau, on appelle cette fonction avec le dataframe à afficher et le titre de la fenetre
    def changeView(self, dataFrameToDisplay, title):
        self.main.title(title)
        self.table = pt = Table(self.frame, dataframe=dataFrameToDisplay,
                                showtoolbar=False, showstatusbar=True)
        pt.show()
        
# Classe de la fenetre des actions du programme (UI initialisé par PyQt5)
class Ui_ActionScreen(object):
    
    def __init__(self, Corpus):
        self.corpus = Corpus
        self.ui_results = Ui_ResultsFrame()    

    # Fonction de setup de la fenetre (déclaration et mise en place des composants)
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(793, 399)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 791, 401))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        # SpinBox qui permet à l'utilisateur de taper le nombre de top mots utilisés qui veut afficher sur les docs Reddit
        self.spNbTopWordsReddit = QtWidgets.QSpinBox(self.frame)
        self.spNbTopWordsReddit.setGeometry(QtCore.QRect(40, 30, 42, 31))
        self.spNbTopWordsReddit.setObjectName("spNbTopWordsReddit")
        # On laisse la possibilité de choisir entre 1 et 1000
        self.spNbTopWordsReddit.setMinimum(1)
        self.spNbTopWordsReddit.setMaximum(1000)
        
        # SpinBox qui permet à l'utilisateur de taper le nombre de top mots utilisés qui veut afficher sur les docs Arxiv
        self.spNbTopWordsArxiv = QtWidgets.QSpinBox(self.frame)
        self.spNbTopWordsArxiv.setGeometry(QtCore.QRect(450, 30, 42, 31))
        self.spNbTopWordsArxiv.setObjectName("spNbTopWordsArxiv")
        # On laisse la possibilité de choisir entre 1 et 1000
        self.spNbTopWordsArxiv.setMinimum(1)
        self.spNbTopWordsArxiv.setMaximum(1000)
        
        # On crée la police des boutons qu'on appliquera à tous les boutons de l'écran
        btnFont = QtGui.QFont()
        btnFont.setFamily("Fantasy")
        btnFont.setPointSize(10)
        btnFont.setBold(True)
        btnFont.setWeight(20)
        
        # Bouton qui permet de retrouver les X tops mots (celles qui ont le + d'occurence) du corpus Reddit
        self.btnTopMotsReddit = QtWidgets.QPushButton(self.frame)
        self.btnTopMotsReddit.setGeometry(QtCore.QRect(100, 30, 221, 41))
        self.btnTopMotsReddit.setObjectName("btnTopMotsReddit")
        # Au click on lance la recherche des tops mots dans le corpus
        self.btnTopMotsReddit.clicked.connect(self.getTopXWordsFromRedditResults)
        # Application du style de police au bouton
        self.btnTopMotsReddit.setFont(btnFont)
        # Application d'un look au bouton
        self.btnTopMotsReddit.setStyleSheet("QPushButton{\n"
        "    background-color:#1976d2;\n"
        "    border-radius: 15px;\n"
        "    color:white;\n"
        "    opacity: 0.9;\n"
        "}")
        
        # Bouton qui permet de retrouver les X tops mots (celles qui ont le + d'occurence) du corpus Arxiv
        self.btnTopMotsArxiv = QtWidgets.QPushButton(self.frame)
        self.btnTopMotsArxiv.setGeometry(QtCore.QRect(510, 30, 181, 41))
        self.btnTopMotsArxiv.setObjectName("btnTopMotsArxiv")
        self.btnTopMotsArxiv.clicked.connect(self.getTopXWordsFromArxivResults)        
        self.btnTopMotsArxiv.setFont(btnFont)
        self.btnTopMotsArxiv.setStyleSheet("QPushButton{\n"
        "    background-color:#67daff;\n"
        "    border-radius: 15px;\n"
        "    color:black;\n"
        "    opacity: 0.9;\n"
        "}")
        
        # Bouton qui permet d'afficher la liste des mots trouvés par Reddit et inexistant dans les documents Arxiv du corpus
        self.btnMotsPasDansArxiv = QtWidgets.QPushButton(self.frame)
        self.btnMotsPasDansArxiv.setGeometry(QtCore.QRect(30, 90, 341, 71))
        self.btnMotsPasDansArxiv.setObjectName("btnMotsPasDansArxiv")
        # Au click du bouton, on affiche la liste des mots
        self.btnMotsPasDansArxiv.clicked.connect(self.getWordsNotInArxivResults)
        self.btnMotsPasDansArxiv.setFont(btnFont)
        self.btnMotsPasDansArxiv.setStyleSheet("QPushButton{\n"
        "    background-color:#1976d2;\n"
        "    border-radius: 15px;\n"
        "    color:white;\n"
        "    opacity: 0.9;\n"
        "}")
        
        # Bouton qui permet d'afficher la liste des mots trouvés par Arxiv et inexistant dans les documents Reddit du corpus
        self.btnMotsPasDansReddit = QtWidgets.QPushButton(self.frame)
        self.btnMotsPasDansReddit.setGeometry(QtCore.QRect(440, 90, 341, 71))
        self.btnMotsPasDansReddit.setObjectName("btnMotsPasDansReddit")
        # Au click du bouton, on affiche la liste des mots
        self.btnMotsPasDansReddit.clicked.connect(self.getWordsNotInRedditResults)
        self.btnMotsPasDansReddit.setFont(btnFont)
        self.btnMotsPasDansReddit.setStyleSheet("QPushButton{\n"
        "    background-color:#67daff;\n"
        "    border-radius: 15px;\n"
        "    color:black;\n"
        "    opacity: 0.9;\n"
        "}")
        
        
        # Bouton qui permet d'afficher le score BM250Okapi d'un mot tapé par l'utilisateur, cherchant dans les docs reddit du corpus
        self.btnScoreOkapiReddit = QtWidgets.QPushButton(self.frame)
        self.btnScoreOkapiReddit.setGeometry(QtCore.QRect(160, 180, 211, 51))
        self.btnScoreOkapiReddit.setObjectName("btnScoreOkapiReddit")
        self.btnScoreOkapiReddit.clicked.connect(self.getOkapiScoringForReddit)
        self.btnScoreOkapiReddit.setFont(btnFont)
        self.btnScoreOkapiReddit.setStyleSheet("QPushButton{\n"
        "    background-color:#1976d2;\n"
        "    border-radius: 15px;\n"
        "    color:white;\n"
        "    opacity: 0.9;\n"
        "}")
        
        
        # Bouton qui permet d'afficher le score TF-IDF de tous les mots du corpus Reddit
        self.btnScoreTFIDFReddit = QtWidgets.QPushButton(self.frame)
        self.btnScoreTFIDFReddit.setGeometry(QtCore.QRect(80, 310, 290, 51))
        self.btnScoreTFIDFReddit.setObjectName("btnScoreTFIDFReddit")
        self.btnScoreTFIDFReddit.clicked.connect(self.getScoreTfIdfForReddit)
        self.btnScoreTFIDFReddit.setFont(btnFont)
        self.btnScoreTFIDFReddit.setStyleSheet("QPushButton{\n"
        "    background-color:#1976d2;\n"
        "    border-radius: 15px;\n"
        "    color:white;\n"
        "    opacity: 0.9;\n"
        "}")
        
        # Bouton qui permet d'afficher le score BM250Okapi d'un mot tapé par l'utilisateur, cherchant dans les docs arxiv du corpus
        self.btnScoreOkapiArxiv = QtWidgets.QPushButton(self.frame)
        self.btnScoreOkapiArxiv.setGeometry(QtCore.QRect(560, 180, 211, 51))
        self.btnScoreOkapiArxiv.clicked.connect(self.getOkapiScoringForArxiv)
        self.btnScoreOkapiArxiv.setObjectName("btnScoreOkapiArxiv")
        self.btnScoreOkapiArxiv.setFont(btnFont)
        self.btnScoreOkapiArxiv.setStyleSheet("QPushButton{\n"
        "    background-color:#67daff;\n"
        "    border-radius: 15px;\n"
        "    color:black;\n"
        "    opacity: 0.9;\n"
        "}")
        
        # Champ qui permet à l'utilisateur de taper le mot dont il veut avoir le score BM250Okapi sur reddit
        self.inputMotOkapiReddit = QtWidgets.QLineEdit(self.frame)
        self.inputMotOkapiReddit.setGeometry(QtCore.QRect(30, 200, 113, 22))
        self.inputMotOkapiReddit.setObjectName("inputMotOkapiReddit")
        # Champ qui permet à l'utilisateur de taper le mot dont il veut avoir le score BM250Okapi sur arxiv
        self.inputMotOkapiArxiv = QtWidgets.QLineEdit(self.frame)
        self.inputMotOkapiArxiv.setGeometry(QtCore.QRect(440, 190, 113, 22))
        self.inputMotOkapiArxiv.setObjectName("inputMotOkapiArxiv")
        
        # Bouton qui permet d'afficher le score TF-IDF de tous les mots du corpus Arxiv
        self.btnScoreTFIDFArxiv = QtWidgets.QPushButton(self.frame)
        self.btnScoreTFIDFArxiv.setGeometry(QtCore.QRect(490, 310, 231, 51))
        self.btnScoreTFIDFArxiv.setObjectName("btnScoreTFIDFArxiv")
        self.btnScoreTFIDFArxiv.clicked.connect(self.getScoreTfIdfForArxiv)
        self.btnScoreTFIDFArxiv.setFont(btnFont)
        self.btnScoreTFIDFArxiv.setStyleSheet("QPushButton{\n"
        "    background-color:#67daff;\n"
        "    border-radius: 15px;\n"
        "    color:black;\n"
        "    opacity: 0.9;\n"
        "}")
        
        # Bouton qui permet d'afficher la chronologie dans reddit des occurences (par date de document) pour un mot choisi par l'utilisateur.
        self.btnFriseChronoMotReddit = QtWidgets.QPushButton(self.frame)
        self.btnFriseChronoMotReddit.setGeometry(QtCore.QRect(160, 240, 211, 51))
        self.btnFriseChronoMotReddit.setObjectName("btnFriseChronoMotReddit")
        self.btnFriseChronoMotReddit.clicked.connect(self.getChronoWordForReddit)
        self.btnFriseChronoMotReddit.setFont(btnFont)
        self.btnFriseChronoMotReddit.setStyleSheet("QPushButton{\n"
        "    background-color:#1976d2;\n"
        "    border-radius: 15px;\n"
        "    color:white;\n"
        "    opacity: 0.9;\n"
        "}")
        
        # Champ qui permet à l'utilisateur de taper le mot dont il veut avoir la chronologie dans reddit
        self.inputChronoMotReddit = QtWidgets.QLineEdit(self.frame)
        self.inputChronoMotReddit.setGeometry(QtCore.QRect(30, 250, 113, 22))
        self.inputChronoMotReddit.setText("")
        self.inputChronoMotReddit.setObjectName("inputChronoMotReddit")
        
         # Champ qui permet à l'utilisateur de taper le mot dont il veut avoir la chronologie dans arxiv
        self.inputChronoMotArxiv = QtWidgets.QLineEdit(self.frame)
        self.inputChronoMotArxiv.setGeometry(QtCore.QRect(440, 250, 113, 22))
        self.inputChronoMotArxiv.setText("")
        self.inputChronoMotArxiv.setObjectName("inputChronoMotArxiv")
        
        # Bouton qui permet d'afficher la chronologie dans arxiv des occurences (par date de document) pour un mot choisi par l'utilisateur.
        self.btnFriseChronoMotArxiv = QtWidgets.QPushButton(self.frame)
        self.btnFriseChronoMotArxiv.setGeometry(QtCore.QRect(560, 240, 211, 51))
        self.btnFriseChronoMotArxiv.setObjectName("btnFriseChronoMotArxiv")
        self.btnFriseChronoMotArxiv.clicked.connect(self.getChronoWordForArxiv)
        self.btnFriseChronoMotArxiv.setFont(btnFont)
        self.btnFriseChronoMotArxiv.setStyleSheet("QPushButton{\n"
        "    background-color:#67daff;\n"
        "    border-radius: 15px;\n"
        "    color:black;\n"
        "    opacity: 0.9;\n"
        "}")
        
        # Ligne verticale séparatrice
        self.lineSeparateur = QtWidgets.QFrame(self.frame)
        self.lineSeparateur.setGeometry(QtCore.QRect(380, 20, 21, 341))
        self.lineSeparateur.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineSeparateur.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineSeparateur.setObjectName("lineSeparateur")
        
        # Appel à la fonction pour donner du texte à nos composants
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # Fonction générée par PyQt5 UI code generator
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Actions"))
        self.btnMotsPasDansArxiv.setText(_translate("Dialog", "Les mots de reddit qui n\'apparaissent pas dans arxiv"))
        self.btnTopMotsReddit.setText(_translate("Dialog", "mots les + utilisés par Reddit"))
        self.btnScoreOkapiReddit.setText(_translate("Dialog", "Score BM25Okapi d\'un mot "))
        self.btnScoreTFIDFReddit.setText(_translate("Dialog", "Score TF-IDF de tous les mots de reddit"))
        self.btnTopMotsArxiv.setText(_translate("Dialog", "mots les + utilisés par Arxiv"))
        self.btnMotsPasDansReddit.setText(_translate("Dialog", "Les mots de arxiv qui n\'apparaissent pas dans reddit"))
        self.btnScoreOkapiArxiv.setText(_translate("Dialog", "Score BM25Okapi d\'un mot "))
        self.btnScoreTFIDFArxiv.setText(_translate("Dialog", "Score TF-IDF de tous les mots de arxiv"))
        self.btnFriseChronoMotReddit.setText(_translate("Dialog", "Fréquence/Chronologie d\'un mot"))
        self.btnFriseChronoMotArxiv.setText(_translate("Dialog", "Fréquence/Chronologie d\'un mot"))
    
    # Fonction qui permet d'appeler les fonctions qui affiche les résultats sous forme de tableau
    def displayDataframe(self, dataframe, title):
        try:
            self.ui_results.frame.destroy() # On ferme la precedente fenetre (si une est ouverte)
        except:
            pass
        self.ui_results = Ui_ResultsFrame() # Instanciation de la fenetre de resultat
        self.ui_results.changeView(dataframe, title) # On passe le dataframe à afficher et le titre à mettre dans la fenetre
        self.ui_results.mainloop()  
        
    # Fonction qui permet d'afficher les top mots (avec le + d'occurences) dans les documents reddit
    def getTopXWordsFromRedditResults(self):
        # On appelle la fonction get_most_common_words() du corpus
        topWordsFromReddit = self.corpus.get_most_common_words(self.spNbTopWordsReddit.value(), "reddit")
        # On transforme l'objet  topWordsFromReddit (de type Counter) en liste puis en dataframe
        dataframeToDisplay = pd.DataFrame.from_records(list(dict(topWordsFromReddit).items()), columns=['mot','occurrence'])
        # On affiche le résultat
        self.displayDataframe(dataframeToDisplay, "Top " + str(self.spNbTopWordsReddit.value()) + " des mots sur reddit")

    # Fonction qui permet d'afficher les top mots (avec le + d'occurences) dans les documents arxiv    
    def getTopXWordsFromArxivResults(self):
        # On appelle la fonction get_most_common_words() du corpus
        topWordsFromArxiv = self.corpus.get_most_common_words(self.spNbTopWordsArxiv.value(), "arxiv")
        # On transforme l'objet  topWordsFromReddit (de type Counter) en liste puis en dataframe
        dataframeToDisplay = pd.DataFrame.from_records(list(dict(topWordsFromArxiv).items()), columns=['mot','occurrence'])
        # On affiche le résultat
        self.displayDataframe(dataframeToDisplay, "Top " + str(self.spNbTopWordsArxiv.value()) + " des mots sur arxiv")

    
    # Afficher les mots de reddit qui ne sont dans aucun document venant de arxiv
    def getWordsNotInArxivResults(self):
        data = list(set(self.corpus.wordsByDoc.get("reddit")) - set(self.corpus.wordsByDoc.get("arxiv")))
        dataframeToDisplay = pd.DataFrame(data)
        self.displayDataframe(dataframeToDisplay, "Les mots de reddit qui n\'apparaissent pas dans les résultats d'arxiv")
        
    # Afficher les mots de arxiv qui ne sont dans aucun document venant de reddit   
    def getWordsNotInRedditResults(self):
        data = list(set(self.corpus.wordsByDoc.get("arxiv")) - set(self.corpus.wordsByDoc.get("reddit")))
        dataframeToDisplay = pd.DataFrame(data)
        self.displayDataframe(dataframeToDisplay, "Les mots de arxiv qui n\'apparaissent pas dans les résultats de reddit")
        
        
    # Afficher le scoring pour un mot par rapport au corpus filtré sur les docs reddit
    # Utilisation de la bibliothèque Rank-BM25 (https://pypi.org/project/rank-bm25/)
    def getOkapiScoringForReddit(self):
        # On indexe le corpus (tout le corpus reddit = 1 document pour faire simple)
        tokenized_corpus = [self.corpus.wordsByDoc.get('reddit')]
        bm25 = BM25Okapi(tokenized_corpus)
        # On passe le mot à scorer
        tokenized_query = self.inputMotOkapiReddit.text().lower().split(" ")
        doc_scores = bm25.get_scores(tokenized_query)        
        # On transforme l'objet doc_scores renvoyé par la bibliothèque Rank-BM25 à partir de nos données en entrée
        dataframeToDisplay = pd.DataFrame(doc_scores)
        self.displayDataframe(dataframeToDisplay, "Le score BM 250 OKAPI du mot " + self.inputMotOkapiReddit.text().lower() + " dans les résultats reddit")

    # Afficher le scoring pour un mot par rapport au corpus filtré sur les docs arxiv
    # Utilisation de la bibliothèque Rank-BM25 (https://pypi.org/project/rank-bm25/)
    def getOkapiScoringForArxiv(self):           
        tokenized_corpus = [self.corpus.wordsByDoc.get('arxiv')]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = self.inputMotOkapiArxiv.text().lower().split(" ")
        doc_scores = bm25.get_scores(tokenized_query)        
        dataframeToDisplay = pd.DataFrame(doc_scores)
        self.displayDataframe(dataframeToDisplay, "Le score BM 250 OKAPI du mot " + self.inputMotOkapiArxiv.text().lower() + " dans les résultats arxiv")
        
    # Afficher le scoring TF-IDF pour un mot par rapport au corpus filtré sur les docs arxiv
    # Inspiré du code présenté dans l'article https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
    def getScoreTfIdfForReddit(self):     
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([self.corpus.wordsStrByDoc.get('reddit')])
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        denselist = dense.tolist()
        dataframeToDisplay = pd.DataFrame(denselist, columns=feature_names)
        self.displayDataframe(dataframeToDisplay, "Le score TF-IDF des mots dans les résultats reddit")

    # Afficher le scoring TF-IDF pour un mot par rapport au corpus filtré sur les docs arxiv
    # Inspiré du code présenté dans l'article https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
    def getScoreTfIdfForArxiv(self):  
        vectorizer = TfidfVectorizer()         
        vectors = vectorizer.fit_transform([self.corpus.wordsStrByDoc.get('arxiv')])
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        denselist = dense.tolist()
        dataframeToDisplay = pd.DataFrame(denselist, columns=feature_names)
        self.displayDataframe(dataframeToDisplay, "Le score TF-IDF des mots dans les résultats arxiv")

    # Permet d'appeler get_word_infos_by_doc() afin de rechercher la chronologie d'un mot précis dans tout le corpus reddit
    def getChronoWordForReddit(self):  
        data = self.corpus.get_word_infos_by_doc(self.inputChronoMotReddit.text().lower(), 'reddit')
        dataframeToDisplay =pd.DataFrame([data])
        self.displayDataframe(dataframeToDisplay, "Chronologie du mot " + self.inputChronoMotReddit.text().lower() + " dans les docs de reddit")

    # Permet d'appeler get_word_infos_by_doc() afin de rechercher la chronologie d'un mot précis dans tout le corpus arxiv
    def getChronoWordForArxiv(self):  
        data = self.corpus.get_word_infos_by_doc(self.inputChronoMotArxiv.text().lower(), 'arxiv')
        dataframeToDisplay =pd.DataFrame([data])
        self.displayDataframe(dataframeToDisplay, "Chronologie du mot " + self.inputChronoMotArxiv.text().lower() + " dans les docs d'arxiv")