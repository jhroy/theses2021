# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv, requests, io, time
from PyPDF2 import PdfFileReader
from selenium import webdriver

finput = "hecURLs.csv"
fichier = "hec2021.csv"
entetes1 = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

f1 = open(finput)
uuids = csv.reader(f1)

for uuid in sorted(uuids):

	annee = 0
	departement = "inconnu"
	diplome = "inconnu"

	urlThese = "http://reflexion.hec.ca/notice?id={}".format(uuid[1])
	print(urlThese)
	
	yo = webdriver.Chrome()
	yo.get(urlThese)

	time.sleep(4)

	resultats = yo.page_source
	page2 = BeautifulSoup(resultats,"html.parser")

	titre = page2.find("title").text
	auteur = "?"

	divs = page2.find_all("div")

	try:
		for div in divs:
			if div.text == "Date de diplomation":
				annee = div.find_next("span").text.strip()
	except:
		annee = 0

	try:
		for div in divs:
			if div.text == "Programme":
				departement = div.find_next("span").text.strip()
	except:
		departement = "inconnu"

	try:
		for div in divs:
			if div.text == "Cheminement":
				diplome = div.find_next("span").text.strip()
	except:
		diplome = "inconnu"

	for div in divs:
		if div.text == "Libre accès à la publication":
			urlPDF = div.find_next("a")["href"]

	try:
		response = requests.get(urlPDF)
		with io.BytesIO(response.content) as open_pdf_file:
			read_pdf = PdfFileReader(open_pdf_file)
			num_pages = read_pdf.getNumPages()
			# print(num_pages)
	except:
		num_pages = None

	langue = "inconnue"

	infos = ["HEC", titre, annee, auteur, departement, langue, diplome, num_pages, urlThese]

	print(infos)

	asterix = open(fichier,"a")
	obelix = csv.writer(asterix)
	obelix.writerow(infos)

	yo.close()

	print("$"*10)
