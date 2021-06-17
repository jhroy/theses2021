# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv, requests, io, time
from PyPDF2 import PdfFileReader
from concordiaData import donnees

fichier = "concordia2021.csv"
entetes = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

for these in donnees["@graph"]:
	try:
		if int(these["datePublished"]) > 1999:
			annee = these["datePublished"]
			urlThese = these["url"]
			titre = these["name"]
			auteur = these["creator"][0]["name"]
			prenom = these["creator"][0]["givenName"]
			nom = these["creator"][0]["familyName"]
			urlPDF = these["distribution"][0]["contentUrl"]
			# print(these.keys())
			# print(these["@context"])

			site2 = requests.get(urlThese, headers=entetes, timeout=30)
			page2 = BeautifulSoup(site2.text, "html.parser")

			try:
				departement = page2.find("meta", attrs={"name":"eprints.department"})["content"]
			except:
				departement = "inconnu"

			try:
				diplome = page2.find("meta", attrs={"name":"eprints.thesis_type"})["content"]
			except:
				diplome = "inconnu"
			try:
				langue = page2.find("meta", attrs={"name":"DC.language"})["content"]
			except:
				langue = "inconnue"

			try:
				response = requests.get(urlPDF, headers=entetes, timeout=30)
				with io.BytesIO(response.content) as open_pdf_file:
					read_pdf = PdfFileReader(open_pdf_file)
					num_pages = read_pdf.getNumPages()
					# print(num_pages)
			except:
				num_pages = None

			infos = ["Concordia", titre, annee, auteur, nom, prenom, departement, langue, diplome, num_pages, urlThese]

			print(infos)

			asterix = open(fichier,"a")
			obelix = csv.writer(asterix)
			obelix.writerow(infos)

			time.sleep(1)

			print("%"*10)
	except:
		pass
