# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv, requests, io, time
from PyPDF2 import PdfFileReader

fichier = "udesherbrooke2021.csv"
# grades = ["Thèse","Mémoire"]
entetes = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

for an in range(2016,2022):
	for p in range(1,11):
		url = "https://www.erudit.org/fr/theses/sherbrooke/{}/?page={}".format(an,p)
		print(url)
		
		site = requests.get(url, headers=entetes)
		page = BeautifulSoup(site.text, "html.parser")
		
		resultats = page.find("ul", class_="theses").find_all("li", class_="thesis")

		for resultat in resultats:
			# try:

			urlThese = "{}?show=full".format(resultat.a["href"])
			print(urlThese)
			site2 = requests.get(urlThese, headers=entetes, timeout=30)
			page2 = BeautifulSoup(site2.text, "html.parser")

			titre = page2.find("meta", attrs={"name":"DC.title"})["content"]
			auteur = page2.find("meta", attrs={"name":"DC.creator"})["content"]
			annee = page2.find("meta", attrs={"name":"citation_date"})["content"]
			urlThese = page2.find("meta", attrs={"name":"citation_abstract_html_url"})["content"]
			try:
				urlPDF = page2.find("meta", attrs={"name":"citation_pdf_url"})["content"]
			except:
				urlPDF = "aucun"
			# print(titre, auteur, annee)

			# print(page2)

			departement = "inconnu"
			langue = "inconnue"
			diplome = "inconnu"
			num_pages = None

			ariane = page2.find("ul", class_="breadcrumb").find_all("li")
			departement = ariane[1].text.strip()

			# try:
			# tds = page2.find_all("td", class_="label-cell")
			# print(len(tds))
			# for td in tds:
			# 	# print(td.text)
			# 	if td.text == "tme.degree.discipline":
			# 		departement = td.find_next("td").text.strip()
			# departement = page2.find("div", class_="simple-item-view-degreediscipline").text.replace("Programme","").replace("Discipline","").strip()
			# except:
			# 	departement = "inconnu"
			# try:
			langue = page2.find("meta", attrs={"name":"citation_language"})["content"]
			# except:
			# 	langue = "inconnue"
			# diplome = page2.find("div", class_="citation_keywords").text.strip()
			diplome = page2.find("meta", attrs={"name":"DC.type"})["content"]
		# 	# # print(departement, langue, diplome)

			try:
				response = requests.get(urlPDF)
				with io.BytesIO(response.content) as open_pdf_file:
					read_pdf = PdfFileReader(open_pdf_file)
					num_pages = read_pdf.getNumPages()
					# print(num_pages)
			except:
				num_pages = None

			infos = ["UdeSherbrooke", titre, annee, auteur, departement, langue, diplome, num_pages, urlThese]

			print(infos)

			asterix = open(fichier,"a")
			obelix = csv.writer(asterix)
			obelix.writerow(infos)

			time.sleep(1)

			# except:
			# 	pass

			print("#"*10)
