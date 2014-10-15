#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 2.7
# 02/2011
 
import sys, os
from cx_Freeze import setup, Executable
 
#############################################################################
# préparation des options 
 
# chemins de recherche des modules
path = sys.path + ["biblio", "consultations", "etatbase", "etiquettes", 
                   "jugement", "publications", "retourcolis", "saisiebord", 
                   "verifications", "vuetable"]
 
# options d'inclusion/exclusion des modules
includes = ["sip"]
excludes = []
packages = []
 
# copier les fichiers et/ou répertoires et leur contenu
includefiles = [("aide", "aide")]
if sys.platform == "linux2":
    includefiles += [(r"/usr/lib/qt4/plugins/sqldrivers","sqldrivers")]
elif sys.platform == "win32":
    includefiles += [(r"C:\Python27\Lib\site-packages\PyQt4\plugins\sqldrivers","sqldrivers")]
else:
    pass
 
# inclusion éventuelle de bibliothèques supplémentaires
binpathincludes = []
if sys.platform == "linux2":
    # pour que les bibliothèques de /usr/lib soient copiées aussi
    binpathincludes += ["/usr/lib"]
 
# construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes
           }
 
#############################################################################
# préparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"
 
cible_1 = Executable(
    script = "concoursphotos.pyw",
    base = base,
    compress = True,
    icon = None,
    )
 
#############################################################################
# création du setup
setup(
    name = "concoursphotos",
    version = "1",
    description = "Traitement de concours photo sous Windows et Linux",
    author = "Tyrtamos",
    options = {"build_exe": options},
    executables = [cible_1]
    )
