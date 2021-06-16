# Thèses et mémoires du Québec (2e édition; 2021)

Mise à jour d'une [étude réalisée en 2016](https://github.com/jhroy/theses) sur la longueur des thèses et mémoires du Québec. La première édition couvrait la période 1995-2016 et ne comptait que 13 universités. Cette seconde édition est donc revue (2000 à 2020) et augmentée (17 universités).

## Source des données

Moissonner des données dans les répertoires institutionnels des universités, au Québec, c'est comme faire du ski de fond. Il y a quatre niveaux:

### <img src="images/facile.png"> Facile

Pas moins de onze universités proposent (merci 🙏) le téléchargement de leur répertoire institutionnel (en format CSV ou JSON, notamment):
- [Spectrum](https://spectrum.library.concordia.ca/) de l'Université Concordia
- [Espace ETS](https://espace.etsmtl.ca/)
- [Espace ENAP](http://espace.enap.ca/)
- [Espace INRS](http://espace.inrs.ca/cgi/search/simple)
- [Polypublie](https://publications.polymtl.ca/) de Polytechnique Montréal
- [Archipel](https://archipel.uqam.ca/) de l'UQAM
- [Sémaphore](http://semaphore.uqar.ca/) de l'UQAR
- [Depositum](https://depositum.uqat.ca/) de l'UQAT
- le [Dépôt institutionnel de l'UQO](http://dpndev.uqo.ca/)
- [Cognitio](http://depot-e.uqtr.ca/) de l'UQTR et
- [R libre](https://r-libre.teluq.ca/) de l'Université Téluq

À noter que le [*Repository*](https://eprints.ubishops.ca/) de l'Université Bishop's ne contient aucun mémoire ni thèse, ce qui est indicatif du fait que les répertoires institutionnels ne contiennent peut-être pas toute la production des étudiant.e.s aux cycles supérieurs du Québec.

### <img src="images/intermediaire.png"> Intermédiaire

Quatre insititutions ont nécessité un moissonnage qui a été réalisé à partir de la [section Thèses et mémoires d'Érudit](https://www.erudit.org/fr/theses/) et à l'aide d'un script distinct. Chacun de ces scripts commençait par parcourir toutes les pages de toutes les années (2000 à 2020) pour une université donnée. Sur chacune de ces pages ([la 20e de l'année 2014 pour l'Université de Montréal](https://www.erudit.org/fr/theses/udem/2014/?page=20), par exemple), le script se connectait à tous les liens qu'elle contenait. Chacun de ces liens nous menait à la page du répertoire institutionnel de l'université contenant les métadonnées et le fichier PDF de la thèse ou du mémoire correspondant. Chacun de mes scripts s'adaptait à la structure du code HTML de chaque répertoire pour aller chercher les informations qui m'intéressaient (titre, nom de l'auteur.trice, année, département, etc.)


- <img src="images/difficile.png"> difficile
- :skull: malaaaade



J'ai commencé par essayer d'en puiser dans [Thèses Canada](https://www.bac-lac.gc.ca/fra/services/theses/Pages/theses-canada.aspx), offert par Bibliothèque et Archives Canada et regroupant normalement. Mais leur outil de recherche se prête mal à une collecte automatisée de données.

Je me suis donc tourné vers 
