# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv, requests, io, time
from PyPDF2 import PdfFileReader
from selenium import webdriver
# from seleniumwire import webdriver
# from selenium.webdriver.support.ui import WebDriverWait

finput = "hecURLs.csv"
fichier = "hec2021.csv"
entetes1 = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

f1 = open(finput)
uuids = csv.reader(f1)

for uuid in sorted(uuids):

	annee = 0
	departement = "inconnu"
	diplome = "inconnu"

	# entetes2 = {
	# 	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:87.0) Gecko/20100101 Firefox/87.0",
	# 	"X-InMedia-Authorization": "Bearer null 4687a079-6f0f-4752-9300-8f9b247599f4 305574369",
	# 	"Content-Type": "application/json",
	# 	"X-microsite-id": "mainSite",
	# 	"TE": "Trailers",
	# 	"Host": "reflexion.hec.ca",
	# 	"Pragma": "no-cache",
	# 	"Connection": "keep-alive",
	# 	"Accept": "*/*",
	# 	# "X-Requested-With": "XMLHttpRequest",
	# 	"Cookie": "_gcl_au=1.1.2020288852.1617822841; _ga=GA1.2.151179651.1617822842; _fbp=fb.1.1617822841668.944885613; JSESSIONID=FF19DE3FB4E3D1CA9840BFAA71C2002C; _gid=GA1.2.1916954449.1617912903",
	# 	"Referer": "https://reflexion.hec.ca/notice?id={}".format(uuid)
	# 	}

	urlThese = "http://reflexion.hec.ca/notice?id={}".format(uuid[1])
	print(urlThese)
	# apiThese = "https://reflexion.hec.ca/in/rest/api/notice?id={}&locale=fr&aspect=Meta&_=1617917901864".format(uuid)
	# print(apiThese)

	# options = {'enable_har': True}

	# yo = webdriver.Firefox(seleniumwire_options=options)
	yo = webdriver.Chrome()
	yo.get(urlThese)

	time.sleep(4)

	# yo.wait_for_request("in/rest/api", timeout=10)

	# print(yo.requests)
	# print(yo.har)

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

	# time.sleep(1)

	yo.close()

	print("$"*10)