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

D'autres insititutions ont nécessité un moissonnage qui a été réalisé à partir de la [section Thèses et mémoires d'Érudit](https://www.erudit.org/fr/theses/) et à l'aide d'un script distinct.

Dans trois cas, chacun de ces scripts commençait par parcourir toutes les pages de toutes les années (2000 à 2020) pour une université donnée. Sur chacune de ces pages ([la 20e de l'année 2014 pour l'Université de Montréal](https://www.erudit.org/fr/theses/udem/2014/?page=20), par exemple), le script se connectait à tous les liens qu'elle contenait. Chacun de ces liens nous menait à la page du répertoire institutionnel de l'université contenant les métadonnées et le fichier PDF de la thèse ou du mémoire correspondant. Et c'est ici que mes scripts devaient s'adapter à la structure du code HTML de chaque répertoire pour aller chercher les informations qui m'intéressaient (titre, nom de l'auteur.trice, année, département, etc.), ainsi que pour trouver le fichier PDF, le télécharger, en compter le nombre de pages, puis l'effacer pour ne pas faire exploser le disque dur de mon ordinateur.

Voici les scripts que j'ai rédigés pour&nbsp;:
- l'Université de Montréal ([**udem.py**](udem.py))
- l'Université de Sherbrooke ([**udes.py**](udes.py))
- l'Université Laval ([**laval.py**](laval.py) -- seul ce script est accompagné de commentaires pour en décrire le fonctionnement)

À quelques nuances près, vous verrez que les trois scripts font un travail très semblable.

Enfin, l'UQAC est elle aussi dans Érudit, mais je ne suis pas passé par là. J'ai trouvé plus facile d'exporter [une seule page HTML de son répertoire institutionnel](uqac.html) et d'effectuer un moissonnage à partir de cette unique page, ce qui donne un script beaucoup plus simple ([**uqac.py**](uqac.py)) et un moissonnage plus rapide.

### <img src="images/difficile.png"> Difficile

McGill se trouve dans Érudit, mais quand j'ai voulu y reproduire les scripts que j'avais rédigés pour l'UdeM, l'UdeS et Laval, j'ai rencontré un problème particulier. Les liens que contiennent Érudit pointent vers l'ancien répertoire institutionnel de McGill, appelé Digitool. Quand on clique sur une thèse ou un mémoire de cette université dans Érudit, on est d'abord envoyé vers Digitool, puis on est redirigés vers le nouveau répertoire, [eScholarship](https://escholarship.mcgill.ca/). Le problème, c'est que mon script initialement avait du mal à suivre cette redirection.

Je vous donne un exemple. Pour le mémoire en droit de Sophie Beaudoin sur la procréation assistée, publié en 2012, Érudit nous donne l'URL suivant:

http://digitool.library.mcgill.ca/R/-?func=dbin-jump-full&amp;current_base=GEN01&amp;object_id=110698

En fait, l'URL définitif pour ce mémoire est le suivant:

https://escholarship.mcgill.ca/concern/theses/db78tg815?locale=en

Comme la redirection automatique ne fonctionnait pas quand mon script se connectait au premier URL, je cherchais un point commun entre les deux URL... Mais il n'y en a aucun. Habituellement, chaque thèse ou mémoire a un identifiant unique. Mais dans le cas de McGill, ils en on deux. Un pour l'ancien répertoire (et dans notre exemple, cet identifiant est inscrit dans l'URL juste après `object_id`, à savoir **110698**), un pour le nouveau (toujours dans notre exemple, on le retrouve juste avant le `?locale=en` et il s'agit de **db78tg815**). Comment associer ces deux identifiants?

Eh bien j'ai trouvé sur le site de McGill [un fichier javascript qui joue le rôle de table de correspondance](https://testtool.library.mcgill.ca/redirects.js) entre ces deux identifiants. J'ai transposé cette table de correspondance dans un fichier python (il y a plus de 51&nbsp;000 paires d'identifiants qui y sont associés) que j'ai appelé [**correspondances.py**](correspondances.py). Faites-y une recherche avec les deux identifiants du mémoire de Mme Beaudoin. C'est grâce à cette table que mon script [**mcgill.py**](mcgill.py) a pu moissonner les milliers de documents se trouvant dans le répertoire de McGill.

### :skull: malaaaade

HEC!!! HAAAA!

J'ai commencé par essayer d'en puiser dans [Thèses Canada](https://www.bac-lac.gc.ca/fra/services/theses/Pages/theses-canada.aspx), offert par Bibliothèque et Archives Canada et regroupant normalement. Mais leur outil de recherche se prête mal à une collecte automatisée de données.

Je me suis donc tourné vers 
