# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv, requests, io, time
from PyPDF2 import PdfFileReader

finput = "Poly-sans-pages.csv"
fichier = "poly2021.csv"
entetes = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

f1 = open(finput)
papers = csv.reader(f1)
next(papers)

for paper in papers:
	# print(paper[1])
	print(paper[-1])

	site2 = requests.get(paper[-1], headers=entetes, timeout=20)
	page2 = BeautifulSoup(site2.text, "html.parser")

	urlPDF = page2.find("a", class_="ep_document_link")["href"]
	print(urlPDF)

	try:
		response = requests.get(urlPDF, headers=entetes, timeout=30)
		with io.BytesIO(response.content) as open_pdf_file:
			read_pdf = PdfFileReader(open_pdf_file)
			num_pages = read_pdf.getNumPages()
			# print(num_pages)
	except:
		num_pages = None

	infos = [paper[0], paper[1], paper[2], paper[3], paper[4], paper[5], paper[6], paper[7], num_pages, paper[9]]

	print(infos)

	asterix = open(fichier,"a")
	obelix = csv.writer(asterix)
	obelix.writerow(infos)

	print("!"*10)
