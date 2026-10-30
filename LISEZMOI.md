# Cap 945

Appli d’entraînement au **TOEIC Listening & Reading**, pour viser le niveau **C1** (environ 945 points sur 990).
Elle s’installe sur l’iPhone depuis Safari et marche ensuite hors ligne. Tout le contenu est original : aucune
question d’ETS ni d’un manuel publié.

Cette première version couvre trois choses :

- **Mots** : le vocabulaire du TOEIC au niveau B2+ à C1, en cartes à seaux, avec la voix ;
- **Lecture** : la Part 5 (phrases à trous), en entraînement ou en examen chronométré ;
- **Écoute** : la Part 2 (question-réponse), lue par les voix anglaises de l’appareil.

## 1. Installer l’appli sur l’iPhone

1. Ouvre l’adresse de l’appli dans **Safari** (voir la section 7 pour la publier).
2. Touche **Partager**, puis **Sur l’écran d’accueil**.
3. Ouvre-la depuis l’écran d’accueil : elle garde sa copie et marche sans réseau.

Pour de meilleures voix : **Réglages de l’iPhone › Accessibilité › Contenu énoncé › Voix › Anglais**. Télécharge
une voix « améliorée » ou « premium » par accent (américain, britannique, australien) : elles sont bien plus
naturelles que les voix de base. L’appli les trouve d’elle-même au prochain lancement.

## 2. Mots

Chaque carte montre un mot ou une expression en anglais (ou en français, au choix dans Réglages). Touche **Voir la
réponse** : le sens, une phrase d’exemple où le mot est surligné, sa traduction et, s’il y a un piège, une note
« À retenir ». Réponds **√ Je savais** ou **× Je ne savais pas**.

Le planning fonctionne en **seaux**, comme dans 形音义 :

- un mot su monte d’un seau et revient plus tard : après 1, 3, 7, 14, 30 puis 60 jours ;
- un mot raté retourne au seau 0 et revient dans la même séance, après quatre autres cartes ;
- les révisions du jour passent avant les nouveaux mots ; il n’y a pas de quota, tu t’arrêtes quand tu veux.

En haut, **à revoir** compte les révisions du jour et **nouveaux** les mots jamais vus. **Tous les mots** ouvre la
liste complète, avec une recherche en anglais ou en français.

Dans Réglages, tu choisis les thèmes (dix pour l’instant, de « Bureau et réunions » à « Pièges et faux amis »),
l’ordre des nouveaux mots (mélangés ou thème par thème) et la lecture automatique du mot.

Au clavier : Espace pour la réponse, 1 pour ×, 2 pour √, L pour écouter.

## 3. Lecture : Part 5

Une phrase avec un trou, quatre propositions. Au vrai test, il faut tenir environ 20 secondes par question pour
avoir le temps de finir la Part 7.

- **Entraînement** : correction tout de suite, avec la compétence testée, le niveau (B2 ou C1), l’explication en
  français et la traduction. Le chronomètre passe en orange après 20 secondes.
- **Examen** : 20 secondes par question au compte à rebours, aucune correction avant la fin. Quand le temps est
  écoulé, les questions restantes comptent comme fausses.

Tu choisis le nombre de questions (10, 20 ou 30) et, si tu veux, une seule compétence : forme du mot, temps et
formes verbales, vocabulaire, connecteurs, prépositions, pronoms et déterminants, comparatifs.

À la fin : le score, le temps moyen, le résultat par compétence et la liste des erreurs, chacune avec sa correction.

**Carnet d’erreurs** : une question ratée revient le lendemain, puis 7 jours et 30 jours plus tard si tu la
réussis. Les erreurs du jour passent en premier dans les séries, pour la moitié de la série au plus tant qu’il
reste des questions jamais vues.

Une série en cours est gardée : si l’appli se ferme, tu la reprends depuis l’onglet. Le chronomètre s’arrête
quand l’appli passe en arrière-plan.

## 4. Écoute : Part 2

Comme au vrai test, rien n’est écrit : l’appli lit une question ou une remarque, puis les réponses A, B et C,
avec deux voix différentes et des accents variés. Choisis la réponse logique.

- **Entraînement** : tu peux réécouter ; après ta réponse, le texte complet, la bonne réponse, l’explication des
  pièges (mot répété, son proche, mauvais type de réponse) et la traduction.
- **Examen** : une seule écoute, puis 5 secondes pour répondre. Sans réponse, la question compte fausse.

Les accents entendus se règlent dans **Réglages › Voix** (américain, britannique, australien, canadien), avec la
vitesse. Sans voix anglaise sur l’appareil, le texte s’affiche à la place, et le mode examen n’est pas proposé.

## 5. Progrès

- le compte à rebours jusqu’à l’examen (date à régler dans Réglages) ;
- les mots vus, leur répartition dans les seaux, ton rythme de nouveaux mots et le rythme qu’il faudrait pour avoir
  tout vu un mois avant l’examen ;
- pour chaque partie : les questions faites, la réussite au premier essai, le temps moyen en Part 5, le carnet
  d’erreurs et la réussite par compétence ou par type de question. La plus faible est en haut ; un trait marque le
  repère C1 (90 % de réussite, une estimation : ETS ne publie pas sa table de conversion) ;
- l’activité des deux dernières semaines.

## 6. Sauvegarde et mises à jour

La progression reste sur l’appareil. **Réglages › Sauvegarde › Exporter** crée un fichier `cap945-AAAA-MM-JJ.json`
(sur l’iPhone, choisis « Enregistrer dans Fichiers ») ; **Importer** le relit et remplace la progression actuelle,
après confirmation.

**Réglages › Appli › Vérifier** cherche une nouvelle version et relit la banque de questions. Une nouvelle
version s’annonce aussi d’elle-même par un bandeau « Nouvelle version de l’appli prête ».

## 7. Sur l’ordinateur

Le dossier est le site lui-même : `index.html` contient toute l’appli, `banque/` le contenu.

### Essayer en local

```powershell
py -m http.server 8000
```

puis http://localhost:8000.

### La banque de contenu

`banque/banque.json` liste les fichiers ; chaque fichier `.tsv` (texte séparé par des tabulations, lisible dans un
tableur) contient soit des mots, soit des questions de Part 5, soit des questions de Part 2. Le format exact et les
règles de rédaction sont dans `outils/consignes.md`. Après toute modification :

```powershell
py outils\banque.py verifier
```

`py outils\banque.py stats` donne la répartition des réponses et des compétences par fichier,
`py outils\banque.py corriger` remplace les apostrophes droites par ’.

Ne change jamais l’`id` d’une question ni le mot anglais d’une carte déjà apprise : la progression y est attachée.
Une modification de la banque n’a pas besoin d’une nouvelle version de l’appli : elle se relit à l’ouverture.

### Après une modification de l’appli

```powershell
py outils\version_appli.py
```

met à jour la date de version (Réglages › Appli) et le service worker, sans quoi l’iPhone garderait l’ancienne copie.

### Tests

Une fois : `py -m pip install playwright pillow` puis `py -m playwright install chromium`. Ensuite :

```powershell
py tests\test_appli.py
```

Captures d’écran dans `tests/sortie/captures`.

### Publier sur GitHub Pages

Une fois : crée un dépôt sur GitHub, ajoute-le comme `origin`, pousse la branche `main`, puis dans les réglages
du dépôt : **Pages › Deploy from a branch › main / (root)**. L’adresse sera
`https://<ton compte>.github.io/<nom du dépôt>/`.

Ensuite, à chaque changement :

```powershell
git add -A
git commit -m "…"
git push
```

GitHub Pages met une à deux minutes.

## 8. Licences

Police Andika (SIL, licence OFL, `fonts/OFL.txt`). Contenu de la banque : original, rédigé pour cette appli.
