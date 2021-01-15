# -*- coding: utf-8 -*-
"""
Created on 02/01/2021

@author: david
"""

"""

# Created by: PyQt5 UI code generator 5.15.2
#
"""

#Librairies à charger
from PyQt5 import QtCore, QtGui, QtWidgets # Bibliothèque pour la construction de l'interface graphique
from actionscreen import Ui_ActionScreen # Import de la classe Ui_ActionScreen (2e fenetre)
from models import Corpus, RedditDocument, ArxivDocument # Import des classes modèles

import praw
import urllib.request
import xmltodict   
import datetime as dt

# Classe de la fenetre principal du programme (UI initialisé par PyQt5)

class Ui_MainWindow(object):
    
    # Fonction de setup de la fenetre
    def setupUi(self, MainWindow):
        # Initilisation d'1 instance de corpus à vide
        self.corpus = Corpus("", True)
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(619, 379)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # On place une frame sur notre fenetre. C'est sur cette frame qu'on va poser les autres composants (bouton...)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 611, 371))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        # setStyleSheet = Personnalisation du look
        self.frame.setStyleSheet("background-color: white;")
                
        self.btnOK = QtWidgets.QPushButton(self.frame)
        self.btnOK.setGeometry(QtCore.QRect(250, 230, 111, 51))
        self.btnOK.setObjectName("btnOK")
        # Au click du bouton OK, on lancher la fonction launchResearch pour demarrer la recherche de docs
        self.btnOK.clicked.connect(self.launchResearch)
        # On personnalise la police du bouton
        btnFont = QtGui.QFont()
        btnFont.setFamily("Fantasy")
        btnFont.setPointSize(14)
        btnFont.setBold(True)
        btnFont.setWeight(75)
        self.btnOK.setFont(btnFont)
        self.btnOK.setStyleSheet("QPushButton{\n"
"    background-color:#1976d2;\n"
"    border-radius: 15px;\n"
"    color:white;\n"
"    opacity: 0.9;\n"
"}")
        self.lblArticlesMax = QtWidgets.QLabel(self.frame)
        self.lblArticlesMax.setGeometry(QtCore.QRect(20, 150, 71, 20))
        self.lblArticlesMax.setObjectName("lblArticlesMax")
        
        # spArticlesMax = Permet de régler le nombre d'articles maximum à récupérer
        self.spArticlesMax = QtWidgets.QSpinBox(self.frame)
        self.spArticlesMax.setGeometry(QtCore.QRect(100, 150, 81, 22))
        self.spArticlesMax.setObjectName("spArticlesMax")
        self.spArticlesMax.setMinimum(10)
        self.spArticlesMax.setMaximum(100000)
        
        # inputTheme = C'est le champ où l'utilisateur va taper son thème
        self.inputTheme = QtWidgets.QLineEdit(self.frame)
        self.inputTheme.setGeometry(QtCore.QRect(100, 100, 421, 21))
        self.inputTheme.setObjectName("inputTheme")
       
        self.lblTitre = QtWidgets.QLabel(self.frame)
        self.lblTitre.setGeometry(QtCore.QRect(50, 20, 491, 51))
        self.lblTitre.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTitre.setObjectName("lblTitre")
         # On personnalise la police du titre
        titleFont = QtGui.QFont()
        titleFont.setFamily("Fantasy")
        titleFont.setPointSize(10)
        titleFont.setBold(True)
        titleFont.setWeight(75)
        self.lblTitre.setFont(titleFont)
        
        # lblTheme : Label "Thème" accompagnant le champ d'édition
        self.lblTheme = QtWidgets.QLabel(self.frame)
        self.lblTheme.setGeometry(QtCore.QRect(20, 100, 71, 20))
        self.lblTheme.setObjectName("lblTheme")
        
        # progressBar : Barre de progression qui évolue apres le click sur le bouton OK
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setGeometry(QtCore.QRect(35, 310, 541, 23))
        self.progressBar.setProperty("value", 0)
        # par défaut on la rend visible et à 0%
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)
        self.progressBar.setObjectName("progressBar")

        self.progressBar.setStyleSheet("QProgressBar{\n"
    "background-color: #1976d2;\n"
    "color: white;\n"
    "border-style: none;\n"
    "text-align: center;\n"
    "\n"
    "}\n"
    "    \n"
    "QProgressBar::chunk{\n"
    "background-color: #63a4ff;\n"
    "\n"
    "\n"
    "}\n"
    "")
        
        # On prévoit un label d'erreur qui s'affiche au dessus de la barre de progression en cas de retour d'erreur sur les appels API
        self.lblError = QtWidgets.QLabel(self.frame)
        self.lblError.setGeometry(QtCore.QRect(60, 290, 500, 20))
        self.lblError.setText("")
        self.lblError.setObjectName("lblError")
        
        # chkBoxExcludeStopWords : Case à cocher pour permettre à l'utilisateur d'enlever les "mots vides" des documents (stopwords)
        self.chkBoxExcludeStopWords = QtWidgets.QCheckBox(self.frame)
        self.chkBoxExcludeStopWords.setChecked(True)
        self.chkBoxExcludeStopWords.setGeometry(QtCore.QRect(100, 190, 281, 20))
        self.chkBoxExcludeStopWords.setObjectName("chkBoxExcludeStopWords")
        
        MainWindow.setCentralWidget(self.centralwidget)

        # Appel à la fonction pour donner du texte à nos composants ("OK" pour le bouton OK...)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Fonction générée par PyQt5 UI code generator
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Projet Python 2021 - Laila DJEBLI / David HUYNH"))
        self.btnOK.setText(_translate("MainWindow", "OK"))
        self.lblArticlesMax.setText(_translate("MainWindow", "Articles max"))
        self.lblTitre.setText(_translate("MainWindow", "PROJET PYTHON LAILA DJEBLI / DAVID HUYNH"))
        self.lblTheme.setText(_translate("MainWindow", "Thème"))
        self.chkBoxExcludeStopWords.setText(_translate("MainWindow", "Exclure les stopwords (\"mots vides\")"))
        
    # Fonction qui permet d'ouvrir la fenetre d'action
    def openActions(self):
        self.window = QtWidgets.QMainWindow()
        self.uiActionScreen = Ui_ActionScreen(self.corpus) # Instanciation de la classe Ui_ActionScreen située dans le fichier actionscreen.py
        self.uiActionScreen.setupUi(self.window)
        self.window.show() # On affiche cette fenetre
        
    # Fonction qui permet d'appeler les API et fait évoluer la barre de progression
    def launchResearch(self):
        if (self.inputTheme.text !=  ''):
            # Remise à zero du message d'erreur
            self.lblError.setText("")
            self.progressBar.setValue(10)
            # Instanciation du Corpus avec le thème tapé par l'utilisateur et la valeur booleenne de la case à cocher
            self.corpus = Corpus(self.inputTheme.text(), self.chkBoxExcludeStopWords.isChecked())
            self.progressBar.setValue(20)
            # On englobe les appels dans un try/except. Comme ca en cas d'erreur, on affiche les erreurs.
            try:
                # Récupération des documents sur reddit
                self.getDocsFromReddit(self.inputTheme.text(), self.spArticlesMax.value())
                self.progressBar.setValue(60)
                # Récupération des documents sur Arxiv
                self.getDocsFromArxiv(self.inputTheme.text(), self.spArticlesMax.value())
                
                # Concaténation de tous les documents et nettoyage + Chargement des propriétés wordsByDoc et wordsStrByDoc
                self.corpus.get_word_list_from_docType("reddit")
                self.progressBar.setValue(80)
                
                # Concaténation de tous les documents et nettoyage + Chargement des propriétés wordsByDoc et wordsStrByDoc
                self.corpus.get_word_list_from_docType("arxiv")
                self.progressBar.setValue(100)
                    
                self.progressBar.setValue(0)
                # Si aucune erreur, on affiche l'écran des actions
                self.openActions()            
            except Exception as e:
                # En cas d'erreur :
                print(e) # J'affiche dans la console l'erreur
                self.progressBar.setValue(0) # Je remet la barre de progression à zero
                # Enfin j'affiche un message d'erreur à l'utilisateur
                self.lblError.setText("Erreur dans la récupération des données. Veuillez essayer avec un autre thème")

    # Appel API Reddit et alimentation du corpus
    def getDocsFromReddit(self, theme, nbResultatsMax):
        # Récupération des documents depuis Reddit
        reddit = praw.Reddit(client_id='0AlqCfHuOc5Hkg', client_secret='80PspjYMdTvF91ti9qZeWzAS2BU', user_agent='Reddit Irambique')
        hot_posts = reddit.subreddit(theme).hot(limit=nbResultatsMax)
        # On parcours les post reddit pour créer des docs
        for post in hot_posts:
            datet = dt.datetime.fromtimestamp(post.created)
            txt = post.title + ". "+ post.selftext
            txt = txt.replace('\n', ' ')
            txt = txt.replace('\r', ' ')
            # Appel du constructeur RedditDocument (classe enfant de la classe Document)
            doc = RedditDocument(datet, post.title, txt)
            # Appel de la fonction add_doc pour ajouter le document tout juste instancié dans l'objet collection (du corpus)
            self.corpus.add_doc(doc)
    
    # Appel API Arxiv et alimentation du corpus
    def getDocsFromArxiv(self, theme, nbResultatsMax):
        # Récupération des documents depuis Arxiv
        url = 'http://export.arxiv.org/api/query?search_query=all:'+theme+'&start=0&max_results='+str(nbResultatsMax)
        data =  urllib.request.urlopen(url).read().decode()
        docsFromArxiv = xmltodict.parse(data)['feed']['entry']
        
        # On parcours les post Arxiv pour créer des docs
        for doc in docsFromArxiv:
            datet = dt.datetime.strptime(doc['published'], '%Y-%m-%dT%H:%M:%SZ')
            txt = doc['title']+ ". " + doc['summary']
            txt = txt.replace('\n', ' ')
            txt = txt.replace('\r', ' ')
            # Appel du constructeur ArxivDocument (classe enfant de la classe Document)
            doc = ArxivDocument(datet, doc['title'], txt)
            # Appel de la fonction add_doc pour ajouter le document tout juste instancié dans l'objet collection (du corpus)
            self.corpus.add_doc(doc)
            
# Instanciation de Ui_MainWindow et affichage de la fenetre
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())