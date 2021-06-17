# License GNU, GPL v3 -- Jean-Hugues Roy -- 2021
# coding: utf-8

import sys, csv, time, os, requests, json, uuid, re, tika, pytesseract, io
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
from collections import Counter
from tika import parser
from PIL import Image
from pdf2image import convert_from_path

fichierIN = "echantillon.csv"
fichierOUT = "echantillon-langue-verifiee.csv"

cle = "obtenez votre propre clé"
point = "https://api.cognitive.microsofttranslator.com/"
lieu = "canadacentral"

chemin = '/detect'

params = {
    'api-version': '3.0'
}

url_construit = point + chemin

entetesMS = {
    'Ocp-Apim-Subscription-Key': cle,
    'Ocp-Apim-Subscription-Region': lieu,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

entetesRequest = {"User-Agent":"Jean-Hugues Roy, UQAM, roy.jean-hugues@uqam.ca - moissonnage en vue d'un article pour la revue de l'ACFAS"}

f = open(fichierIN)
theses = csv.reader(f)
next(theses)

n = 0

for these in theses:
	if these[0] != "UQO" and these[0] != "HEC":
		n+=1
		methode = ""
		url = these[9]
		print(url)
		elements = url.split("/")
		# print(elements)
		if elements[-1] == "":
			num = elements[-2]
		else:
			num = elements[-1].replace("notice?id=","").replace("?mode=full","")
		print(num)
		# print("-"*5)

		site = requests.get(url, headers=entetesRequest, timeout=20)
		page = BeautifulSoup(site.text, "html.parser")
		# print(page)

		liens = page.find_all(href=re.compile("[pdf,PDF]"))

		print(len(liens))

		liens2 = page.find_all("a", string=re.compile("PDF"))

		for l in liens2:
			liens.append(l)

		print(len(liens))

		hyperliens = []

		for lien in liens:
			if num in lien.get("href") and (".pdf" in lien.get("href") or ".PDF" in lien.get("href")):
				if these[0] == "Laval":
					parties = lien.get("href").split("/")
					fin = parties[-1]
					lelien = "https://corpus.ulaval.ca/jspui/bitstream/20.500.11794/" + num + "/1/" + fin
					hyperliens.append(lelien)
				elif these[0] == "UdeM" and "uqtr" not in url:
					parties = lien.get("href").split("/")
					print(parties)
					fin = parties[-1]
					print(fin)
					lelien = "https://papyrus.bib.umontreal.ca/xmlui/bitstream/handle/1866/" + num + "/" + fin.replace("?sequence=2&isAllowed=y","")
					hyperliens.append(lelien)
				elif these[0] == "UdeS":
					parties = lien.get("href").split("/")
					fin = parties[-1]
					lelien = "https://savoirs.usherbrooke.ca/bitstream/handle/11143/" + num + "/" + fin.replace("?sequence=5&isAllowed=y","")
					hyperliens.append(lelien)
				else:
					hyperliens.append(lien.get("href"))
			elif these[0] == "McGill" and lien.text == "Download PDF":
				hyperliens.append("https://escholarship.mcgill.ca{}".format(lien.get("href")).replace("?locale=en",""))

		print(these[0],hyperliens[0])

		urlPDF = hyperliens[0]

		req = requests.get(urlPDF, headers=entetesRequest)
		
		with open("ledocument.pdf", "wb") as fudge:
				fudge.write(req.content)

		try:

			methode = "tika"	

			contenuPDF = parser.from_file(open("ledocument.pdf", "rb"))
			contenu = contenuPDF["content"]

			x = int(len(contenu)/20)
			print("{} caractères (blocs de {})".format(len(contenu),x))
			blocs = [contenu[i:i+x] for i in range(0, len(contenu), x)]

			langues = []

			for bloc in range(0,17,2):
				texte = blocs[bloc+1][:2000]
				# print(texte)

				texte = texte.replace("\n"," ")
				while "  " in texte:
					texte = texte.replace("  "," ")
				texte = texte.strip()

				print(texte)
				print("-"*5)

				body = [{
					'text': texte
				}]

				allo = requests.post(url_construit, params=params, headers=entetesMS, json=body)
				reponse = allo.json()
				# print(len(reponse))
				langues.append(reponse[0]["language"])

		except:

			methode = "ocr"

			with io.BytesIO(req.content) as open_pdf_file:
				read_pdf = PdfFileReader(open_pdf_file)
				num_pages = read_pdf.getNumPages()

			y = int(num_pages/20)

			feuillets = convert_from_path("ledocument.pdf", 500)

			langues = []

			for page in range(y*3,num_pages,y*2):
				feuillets[page].save("pagePDF.jpg","JPEG")
				texte = str(pytesseract.image_to_string(Image.open("pagePDF.jpg")))

				texte = texte.replace("\n"," ")
				while "  " in texte:
					texte = texte.replace("  "," ")
				texte = texte.strip()

				print(texte)
				print("-"*5)

				body = [{
					'text': texte
				}]

				allo = requests.post(url_construit, params=params, headers=entetesMS, json=body)
				reponse = allo.json()
				# print(len(reponse))
				langues.append(reponse[0]["language"])

		print(methode, langues)
		freq = Counter(langues)
		print(freq)

		if freq.most_common(1)[0][1] > 4:
			lalangue = freq.most_common(1)[0][0]

		these.append(lalangue)

		print(these)

		mark = open(fichierOUT, "a")
		zuck = csv.writer(mark)
		zuck.writerow(these)

		print("•"*10)