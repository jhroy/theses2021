# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv, requests, io, time, roman
from PyPDF2 import PdfFileReader

fichier = "laval2021.csv"
entetes = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

for an in range(2008,2021):
	for p in range(1,19):
		url = "https://www.erudit.org/fr/theses/laval/{}/?page={}".format(an,p)
		print(url)
		site = requests.get(url, headers=entetes)
		page = BeautifulSoup(site.text, "html.parser")
		
		resultats = page.find("ul", class_="theses").find_all("li", class_="thesis")

		for resultat in resultats:
			try:
				urlThese = resultat.a["href"]
				print(urlThese)
				numero = urlThese.split("/")[-1]
				urlThese = "https://corpus.ulaval.ca/jspui/handle/20.500.11794/{}?mode=full".format(numero)
				print(urlThese)

				site2 = requests.get(urlThese, headers=entetes, timeout=20)
				page2 = BeautifulSoup(site2.text, "html.parser")

				titre = page2.find("meta", attrs={"name":"DC.title"})["content"]
				auteur = page2.find("meta", attrs={"name":"DC.creator"})["content"]
				annee = page2.find("meta", attrs={"name":"citation_publication_date"})["content"]
		# 	# 	urlThese = page2.find("meta", attrs={"name":"citation_abstract_html_url"})["content"]
				urlPDF = page2.find("meta", attrs={"name":"citation_pdf_url"})["content"]
				# print(titre, auteur, annee)
				print(titre)

				try:
					tds = page2.find_all("td", class_="metadataFieldLabel")
					for td in tds:
						if td.text == "etdms.degree.name":
							depdip = td.find_next("td").text.strip()
					depdip = depdip.split(".")
					# print(depdip)
					departement = depdip[1].strip()
					diplome = depdip[0].strip()
				except:
					departement = "inconnu"
					diplome = "inconnu"
				try:
					langue = page2.find("meta", attrs={"name":"DC.language"})["content"]
				except:
					langue = "inconnue"

				try:
					pages = page2.find("meta", attrs={"name":"DCTERMS.extent"})["content"]
					print(pages)
					pages = pages.split(",")
					# print(pages)
					num_pages = 0
					for x in pages:
						# print(x)
						x = x.split()[0].replace("[","").replace("]","").strip()
						try:
							nb = roman.fromRoman(x.upper())
						except:
							nb = x
						# print(nb)
						num_pages += int(nb)	
					# print(num_pages)

				except:
					try:
						response = requests.get(urlPDF, headers=entetes, timeout=30)
						with io.BytesIO(response.content) as open_pdf_file:
							read_pdf = PdfFileReader(open_pdf_file)
							num_pages = read_pdf.getNumPages()
							# print(num_pages)
					except:
						num_pages = None

				infos = ["U. Laval", titre, annee, auteur, departement, langue, diplome, num_pages, urlThese]

				print(infos)

				asterix = open(fichier,"a")
				obelix = csv.writer(asterix)
				obelix.writerow(infos)

				time.sleep(2)
				
			except:
				pass

			print("-"*10)
