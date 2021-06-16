# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv, requests, io, time
from PyPDF2 import PdfFileReader
from correspondances import escholarship

fichier = "mcgill2021.csv"

for an in range(2003,2022):
	for p in range(1,26):
		url = "https://www.erudit.org/fr/theses/mcgill/{}/?page={}".format(an,p)
		# print(url)
		site = requests.get(url)
		page = BeautifulSoup(site.text, "html.parser")

		resultats = page.find("ul", class_="theses").find_all("li", class_="thesis")

		for resultat in resultats:
			try:
				urlThese = resultat.a["href"]
				# session = requests.Session()
				print(urlThese)
				numero = urlThese.split("object_id=")[-1]
				print(escholarship[numero])
				# redirect1 = requests.head(urlThese, allow_redirects=True)
				# print(redirect1.url)
				# session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:87.0) Gecko/20100101 Firefox/87.0"
				# redirect2 = session.get(redirect1.url, allow_redirects=True, timeout=10)
				# print(redirect2.url)

				site2 = requests.get(escholarship[numero])
				page2 = BeautifulSoup(site2.text, "html.parser")
				# print(page2)

				titre = page2.find("meta", attrs={"name":"citation_title"})["content"]
				auteur = page2.find("meta", attrs={"name":"citation_author"})["content"]
				annee = page2.find("meta", attrs={"name":"citation_publication_date"})["content"]
				urlPDF = page2.find("meta", attrs={"name":"citation_pdf_url"})["content"]
				# print(titre)
				# # print(titre, auteur, annee)

				try:
					departement = page2.find("li", class_="attribute-department").text.strip()
				except:
					departement = "inconnu"
				try:
					langue = page2.find("li", class_="attribute-language").text.strip()
				except:
					langue = "inconnue"
				diplome = page2.find("li", class_="attribute-degree").text.strip()
				# # print(departement, langue, diplome)

				response = requests.get(urlPDF)
				with io.BytesIO(response.content) as open_pdf_file:
					read_pdf = PdfFileReader(open_pdf_file)
					num_pages = read_pdf.getNumPages()
					# print(num_pages)

				urlThese = escholarship[numero]

				infos = ["McGill", titre, annee, auteur, departement, langue, diplome, num_pages, urlThese]

				print(infos)

				asterix = open(fichier,"a")
				obelix = csv.writer(asterix)
				obelix.writerow(infos)
			
			except:
				pass

			print("*"*8)

			# time.sleep(1)