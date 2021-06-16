# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv, requests, io, time
from PyPDF2 import PdfFileReader

fichier = "udem2021.csv"
entetes = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

for an in range(2000,2022):
	for p in range(1,23):
		url = "https://www.erudit.org/fr/theses/udem/{}/?page={}".format(an,p)
		print(url)
		site = requests.get(url,headers=entetes)
		page = BeautifulSoup(site.text, "html.parser")

		resultats = page.find("ul", class_="theses").find_all("li", class_="thesis")

		for resultat in resultats:
			try:
				urlThese = resultat.a["href"]
				print(urlThese)

				site2 = requests.get(urlThese,headers=entetes)
				page2 = BeautifulSoup(site2.text, "html.parser")

				titre = page2.find("meta", attrs={"name":"DC.title"})["content"]
				auteur = page2.find("meta", attrs={"name":"DC.creator"})["content"]
				try:
					annee = page2.find("meta", attrs={"name":"DC.date"})["content"]
				except:
					annee = an
				urlThese = page2.find("meta", attrs={"name":"DC.identifier"})["content"]
				urlPDF = page2.find("meta", attrs={"name":"citation_pdf_url"})["content"]
				# # print(titre, auteur, annee)

				try:
					departement = page2.find("div", class_="simple-item-view-degreediscipline").text.replace("Programme","").replace("Discipline","").strip()
				except:
					departement = "inconnu"
				try:
					langue = page2.find("meta", attrs={"name":"DCTERMS.language"})["content"]
				except:
					langue = "inconnue"
				diplome = page2.find("div", class_="simple-item-view-degreelevel").text.replace("Cycle d'études","").replace("Level","").strip()
				# # print(departement, langue, diplome)

				try:
					response = requests.get(urlPDF)
					with io.BytesIO(response.content) as open_pdf_file:
						read_pdf = PdfFileReader(open_pdf_file)
						num_pages = read_pdf.getNumPages()
						# print(num_pages)
				except:
					num_pages = None

				infos = ["UdeM", titre, annee, auteur, departement, langue, diplome, num_pages, urlThese]

				print(infos)

				asterix = open(fichier,"a")
				obelix = csv.writer(asterix)
				obelix.writerow(infos)
			
				time.sleep(1)

			except:
				pass

			print("~"*8)




# for p in range(55,1900):
# 	url = "https://papyrus.bib.umontreal.ca/xmlui/discover?rpp=10&etal=0&group_by=none&page={}&sort_by=dc.date.issued_dt&order=desc&filtertype_0=type&filter_relational_operator_0=equals&filter_0=Th%C3%A8se+ou+m%C3%A9moire+%2F+Thesis+or+Dissertation".format(p)
# 	# print(url)
# 	site = requests.get(url)
# 	page = BeautifulSoup(site.text, "html.parser")

# 	resultats = page.find_all("div", class_="artifact-description")

# 	for resultat in resultats:
# 		urlThese = "https://papyrus.bib.umontreal.ca{}".format(resultat.a["href"])
# 		print(urlThese)
# 		try:
# 			site2 = requests.get(urlThese)
# 			page2 = BeautifulSoup(site2.text, "html.parser")

# 			titre = page2.find("meta", attrs={"name":"DC.title"})["content"]
# 			auteur = page2.find("meta", attrs={"name":"DC.creator"})["content"]
# 			annee = page2.find("meta", attrs={"name":"DC.date"})["content"]
# 			urlThese = page2.find("meta", attrs={"name":"DC.identifier"})["content"]
# 			urlPDF = page2.find("meta", attrs={"name":"citation_pdf_url"})["content"]
# 			# # print(titre, auteur, annee)

# 			try:
# 				departement = page2.find("div", class_="simple-item-view-degreediscipline").text.replace("Programme","").replace("Discipline","").strip()
# 			except:
# 				departement = "inconnu"
# 			try:
# 				langue = page2.find("meta", attrs={"name":"DCTERMS.language"})["content"]
# 			except:
# 				langue = "inconnue"
# 			diplome = page2.find("div", class_="simple-item-view-degreelevel").text.replace("Cycle d'études","").replace("Level","").strip()
# 			# # print(departement, langue, diplome)

# 			try:
# 				response = requests.get(urlPDF)
# 				with io.BytesIO(response.content) as open_pdf_file:
# 					read_pdf = PdfFileReader(open_pdf_file)
# 					num_pages = read_pdf.getNumPages()
# 					# print(num_pages)
# 			except:
# 				num_pages = None

# 			infos = ["UdeM", titre, annee, auteur, departement, langue, diplome, num_pages, urlThese]

# 			print(infos)

# 			asterix = open(fichier,"a")
# 			obelix = csv.writer(asterix)
# 			obelix.writerow(infos)
		
# 			time.sleep(1)

		# except:
		# 	pass
