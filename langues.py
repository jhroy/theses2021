# License GNU, GPL v3 -- Jean-Hugues Roy -- 2021
# coding: utf-8

import csv, langid
# from textblob import TextBlob
from langdetect import detect
from polyglot.detect import Detector
from collections import Counter

fichierIn = "toutes2021.csv"
fichierOut = "toutes2021-avec-langues.csv"

f = open(fichierIn)
theses = csv.reader(f)
next(theses)

for these in theses:
	langues = []
	print(these[1])

	texte = these[1].replace("\n"," ")
	while "  " in texte:
		texte = texte.replace("  "," ")
	texte = texte.lower().strip()
	
	# print("«")
	# print(texte)
	# print("»")

	try:
		if texte is not None and texte != "":
			# print(detect(texte))
			langues.append(detect(texte)) # Utilisation de langdetect
			# lang = TextBlob(texte)
			# print(lang.detect_language())
			# langues.append(lang.detect_language())
			# print(langid.classify(texte),type(langid.classify(texte)))
			# for l in langid.classify(texte):
				# print(langid.classify(texte).index(l),l)
			# print(langid.classify(texte)[0])
			langues.append(langid.classify(texte)[0]) # Utilisation de langid
			detecteur = Detector(texte)
			langues.append(detecteur.language.code) # Utilisation de polyglot
			# print(detecteur.language.code)
			print(langues)
			freq = Counter(langues)
			# print(freq.most_common(1)[0][0],freq.most_common(1)[0][1])
			if freq.most_common(1)[0][1] > 1:
				langue = freq.most_common(1)[0][0]
			else:
				langue = "inconnue"
		else:
				langue = "inconnue"
	except:
		langue = "inconnue"
		# print("##############################")
		# print("### Pas pu faire l'analyse ###")
		# print("##############################")
	print(langue)
	print("+"*10)

	these.append(langue)

	print(these)

	mark = open(fichierOut, "a")
	zuck = csv.writer(mark)
	zuck.writerow(these)