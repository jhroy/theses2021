# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv, requests, io, time, roman
from PyPDF2 import PdfFileReader

fichier = "laval2021.csv"

# Déclaration dans l'entête de mes requêtes HTTP pour bien indiquer qui bombarde le serveur avec toutes ces requêtes et pourquoi
entetes = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

# Première boucle dans Érudit
for an in range(2000,2021):
	for p in range(1,19): # Deuxième boucle dans toutes les pages pour une année donnée
		url = "https://www.erudit.org/fr/theses/laval/{}/?page={}".format(an,p)
		print(url)
		
		# On se connecte à Érudit
		site = requests.get(url, headers=entetes)
		page = BeautifulSoup(site.text, "html.parser")
		
		# On recueille la liste de toutes les dissertations se trouvant sur cette page
		resultats = page.find("ul", class_="theses").find_all("li", class_="thesis")
		
		# Troisième boucle pour traiter chacune des dissertations se trouvant sur la page
		for resultat in resultats:
			try:
				urlThese = resultat.a["href"]
				print(urlThese)
				numero = urlThese.split("/")[-1]
				
				# On construit l'URL spécifique à l'Université Laval, ici
				urlThese = "https://corpus.ulaval.ca/jspui/handle/20.500.11794/{}?mode=full".format(numero)
				print(urlThese)
				
				# On se connecte au répertoire institutionnel de l'U. Laval, toujours avec nos entêtes de présentation
				site2 = requests.get(urlThese, headers=entetes, timeout=20)
				page2 = BeautifulSoup(site2.text, "html.parser")
				
				# On va chercher toutes les métadonnées possibles
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
				
				# Laval nous donne la langue dans laquelle a été rédigée la thèse ou le mémoire
				try:
					langue = page2.find("meta", attrs={"name":"DC.language"})["content"]
				except:
					langue = "inconnue"
				
				# Laval nous donne aussi le nombre de pages du documents (le code ci-dessous fait même une conversion des pages liminaires de chiffres romains en chiffres arabes)
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
				
				# Si le nombre de pages n'est pas dans les métadonnées, le script va chercher le PDF et en compte le nombre de pagess
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
				
				# On confine toutes les données dans un fichier CSV
				asterix = open(fichier,"a")
				obelix = csv.writer(asterix)
				obelix.writerow(infos)

				time.sleep(2)
				
			except:
				pass

			print("-"*10)
