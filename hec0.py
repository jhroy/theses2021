# coding=utf-8
# ©2021, Jean-Hugues Roy - Licence GNU GPL v3

from bs4 import BeautifulSoup
import csv

fichier = "hecURLs.csv"
sources = ["hec-doctorats.html","hec-maitrises-1.html","hec-maitrises-2.html"]
uuids = []

for source in sources:
	page = BeautifulSoup(open(source), "html.parser")
		
	resultats = page.find("div", id="searchresult").find_all("div")
	print(len(resultats))
	for resultat in resultats:
		try:
			if resultat.a["href"].startswith("/"):
				notice = resultat.a["href"]
				# print(notice)
				notice = notice.split("&")
				# print(notice)
				notice = notice[0].split("%3A")
				# print(notice[-1])
				uuids.append(notice[-1])
		except:
			pass

print(len(uuids))
uuids = set(uuids)
print(len(uuids))

n = 0

for uuid in sorted(uuids):
	n += 1

	infos = [n,uuid]

	asterix = open(fichier,"a")
	obelix = csv.writer(asterix)
	obelix.writerow(infos)