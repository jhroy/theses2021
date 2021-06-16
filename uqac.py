# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
# import csv, requests, io, time
import csv, requests
# from PyPDF2 import PdfFileReader

fichier = "uqac2021.csv"
entetes = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

page = BeautifulSoup(open("uqac.html"), "html.parser")

resultats = page.find_all("p")

for resultat in resultats:
	try:
		urlThese = resultat.a["href"]
		print(urlThese)

	# 	urlThese = "{}?show=full".format(urlThese)
	# 	print(urlThese)
		site2 = requests.get(urlThese, headers=entetes, timeout=30)
		page2 = BeautifulSoup(site2.text, "html.parser")

		titre = page2.find("meta", attrs={"name":"eprints.title"})["content"]
		auteur = page2.find("meta", attrs={"name":"eprints.creators_name"})["content"]
		annee = page2.find("meta", attrs={"name":"eprints.date"})["content"]

		departement = page2.find("meta", attrs={"name":"eprints.department"})["content"]
		langue = page2.find("meta", attrs={"name":"DC.language"})["content"]
		diplome = page2.find("meta", attrs={"name":"eprints.thesis_type"})["content"]

		num_pages = page2.find("meta", attrs={"name":"eprints.pages"})["content"]

		infos = ["UQAC", titre, annee, auteur, departement, langue, diplome, num_pages, urlThese]

		print(infos)

		asterix = open(fichier,"a")
		obelix = csv.writer(asterix)
		obelix.writerow(infos)

		time.sleep(1)

	except:
		pass

	print("#"*10)
