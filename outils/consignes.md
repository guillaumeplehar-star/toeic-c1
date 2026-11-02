# Consignes de rédaction et de relecture du contenu

Ces consignes servent aux agents qui rédigent ou relisent la banque de Cap 945 (`banque/`), et à quiconque y ajoute
des entrées à la main. L'appli prépare au **TOEIC Listening & Reading, niveau C1** (environ 945/990) un francophone
de niveau B2 solide. Tout le contenu est **original** : ne recopie ni ne paraphrase de près aucune question d'ETS,
aucun test officiel, aucun manuel publié (Barron's, Cambridge, Hachette…). Pas de vraies entreprises, pas de marques,
pas de personnes célèbres ; des prénoms et noms variés (anglophones, mais aussi d'autres origines, comme dans le test).

## Règles communes à tous les fichiers

- Fichiers texte UTF-8, une entrée par ligne, colonnes séparées par **une tabulation**, première ligne = en-tête exact
  donné plus bas. Aucune tabulation ni retour à la ligne à l'intérieur d'un champ. Pas de ligne vide au milieu.
- Apostrophe typographique `’` partout, en anglais comme en français (`don’t`, `l’entreprise`). Pas de guillemets
  droits `"` : en français « » (avec espaces), en anglais “ ”.
- Français : majuscule en début de phrase seulement, espace ordinaire avant `: ; ! ?` (l'appli la remplace à
  l'affichage). Pas d'abréviation obscure.
- Dans les textes en français (explications, notes), un mot ou un groupe anglais cité s'écrit entre astérisques :
  `*in charge of*`. L'appli le met en italique. Les astérisques vont toujours par paires.
- Anglais : naturel, idiomatique, registre professionnel du TOEIC (bureau, commerce, voyages, vie courante). Anglais
  américain par défaut (orthographe *organize*, *center*), sauf une note qui signale une différence britannique.
- Le texte anglais est lu par une voix de synthèse : pas d'abréviation lue de travers (`sb`, `sth`, `e.g.`), écris
  les nombres et les heures comme on les lit naturellement (`3:30 P.M.`, `$450` vont bien).

## Aucun indice hors du sens

Le candidat ne doit pouvoir deviner la bonne réponse que par le sens. Sur un fichier :
- les lettres des bonnes réponses sont équilibrées et sans régularité (pas chaque lettre une fois par lot, pas de
  suite prévisible) ;
- la bonne réponse **n'est pas plus souvent la plus longue** qu'au hasard (25 % avec quatre propositions, 33 % avec
  trois) : les réponses indirectes ou paraphrasées sont souvent plus longues, il faut donc des distracteurs aussi
  développés, et parfois une bonne réponse brève. `py outils\banque.py stats` affiche cette part (« plus longue ») et
  signale un écart trop grand ;
- la bonne réponse n'est pas la seule à reprendre un mot rare de la question, ni la seule à être nuancée (*usually*,
  *some*) quand les autres sont absolues.

## Vocabulaire : `banque/mots-<thème>.tsv`

En-tête :

```
anglais	nature	francais	exemple	traduction	note
```

- `anglais` : le mot ou l'expression, en minuscules (sauf nom propre), verbe sans *to*, nom au singulier. Verbe à
  particule : `carry out`. Construction utile : `apply for`, `be eligible for`, `in charge of`. Si un complément
  est nécessaire, écris `someone` / `something` en entier, avec modération.
- `nature` : une de ces valeurs exactement : `nom`, `verbe`, `adjectif`, `adverbe`, `verbe à particule`,
  `expression`, `préposition`, `conjonction`.
- `francais` : le ou les sens, du plus courant au moins courant, séparés par ` ; `. Courts. Une précision entre
  parenthèses si besoin : `facture (envoyée au client)`.
- `exemple` : une phrase anglaise de 8 à 22 mots, contexte TOEIC, qui contient l'expression. L'expression y est
  **entre accolades**, éventuellement conjuguée ou au pluriel : `The audit was {carried out} last week.` Un verbe à
  particule séparé prend deux paires : `We need to {set} the room {up} by noon.` Une seule expression marquée par phrase.
- `traduction` : la traduction française naturelle de l'exemple (sans accolades).
- `note` : facultative, en français, une phrase courte : piège, faux ami, construction (`+ for : *apply for a job*`),
  confusion (`≠ *effect*, le nom`), famille de mots (`*compete, competition, competitive*`), différence US/UK.
  Mets une note chaque fois qu'il y a un vrai piège pour un francophone ; sinon laisse vide.

Choix des entrées : le niveau visé est **B2+ à C1**. Laisse de côté les mots qu'un B2 connaît forcément (*meeting*,
*price*, *computer*, *buy*), sauf dans une collocation ou un emploi moins connu (*meet a deadline*, *price
quote*). Privilégie ce qui fait gagner des points au TOEIC : vocabulaire des Parts 5 à 7, collocations, verbes à
particule, prépositions figées, adjectifs et adverbes de registre soutenu (*tentative*, *comprehensive*,
*promptly*, *accordingly*). Environ 40 % d'expressions et collocations, 60 % de mots seuls. Pas de doublon dans le
fichier ; reste dans ton thème (un mot partagé entre deux thèmes va dans le plus naturel des deux).

Thèmes (identifiant de fichier, nom, contenu) :

| Fichier | Thème | Contenu |
|---|---|---|
| `mots-bureau.tsv` | Bureau et réunions | équipement, organisation du travail, réunions, agenda, courriels et notes, téléphone, rendez-vous, délais, rapports |
| `mots-rh.tsv` | Personnel et carrière | recrutement, candidature, entretien, contrat, formation, promotion, salaire et avantages, évaluation, départ, retraite |
| `mots-finance.tsv` | Finance et comptabilité | budget, factures, comptabilité, impôts, banque, prêts, investissement, audit, recettes et dépenses, rapports annuels |
| `mots-commerce.tsv` | Ventes et clients | ventes, marketing, publicité, études de marché, service client, réclamations, garanties, commerce de détail, négociation |
| `mots-production.tsv` | Production et logistique | fabrication, contrôle qualité, stocks, chaîne d'approvisionnement, fournisseurs, commandes, expédition, entrepôt |
| `mots-voyages.tsv` | Voyages et événements | avion, train, hôtel, réservations, itinéraire, conférences, salons, séminaires, location de voiture, frais de déplacement |
| `mots-locaux.tsv` | Locaux et technique | immobilier, bail, travaux, rénovation, entretien, fournitures, informatique, sécurité, réglementation, environnement |
| `mots-loisirs.tsv` | Vie courante | restaurant, traiteur, santé et assurance, rendez-vous médicaux, culture et loisirs, médias, météo, vie locale, logement |
| `mots-pieges.tsv` | Pièges et faux amis | mots qui se confondent (*affect/effect*, *rise/raise*, *economic/economical*, *lie/lay*), faux amis (*actually*, *eventually*, *sensible*, *achieve*), familles de mots à forme proche |
| `mots-liens.tsv` | Liens et particules | connecteurs (*whereas*, *provided that*, *notwithstanding*), verbes à particule transversaux (*look into*, *call off*), prépositions figées (*on behalf of*, *in accordance with*), adverbes de registre soutenu |

## Part 5, phrases à trous : `banque/part5-<série>.tsv`

En-tête :

```
id	phrase	a	b	c	d	reponse	competence	niveau	explication	traduction
```

- `id` : préfixe de la série + numéro sur trois chiffres : `5a-001`, `5a-002`… Jamais réutilisé ni changé.
- `phrase` : une phrase anglaise de 14 à 35 mots, style TOEIC (annonce interne, courriel, article économique,
  consigne), avec **exactement un** trou écrit `-------` (sept tirets).
- `a`, `b`, `c`, `d` : les quatre propositions, sans lettre ni ponctuation finale.
- `reponse` : `A`, `B`, `C` ou `D`. Répartition équilibrée sur la série (environ un quart chacune), sans suite
  prévisible.
- `competence` : une de ces valeurs exactement :
  - `forme` : forme du mot (nom, verbe, adjectif, adverbe d'une même famille : *compete / competition / competitive /
    competitively*) ;
  - `verbe` : temps, voix, accord, forme verbale (infinitif, gérondif, participe), subjonctif, conditionnel ;
  - `prep` : prépositions ;
  - `lien` : connecteurs et conjonctions (*although / despite / however*, *unless*, *whereas*), y compris le choix
    préposition ou conjonction ;
  - `pronom` : pronoms, relatifs, déterminants, quantifieurs (*each / every / either*, *whose*, *themselves*) ;
  - `compar` : comparatifs, superlatifs, *as … as*, *the more … the more* ;
  - `vocab` : vocabulaire, collocations, verbes à particule (les quatre propositions ont la même nature
    grammaticale ; une seule convient par le sens ou la construction).
- `niveau` : `B2` ou `C1`. Vise environ 30 % de B2 et 70 % de C1 : l'utilisateur vise 945, il a besoin de questions
  difficiles. Une question C1 joue sur une nuance réelle : forme du mot dans une position inattendue, inversion
  (*Should you need…*, *Had the shipment arrived…*), subjonctif (*recommend that she be*), participe en tête de
  phrase, *whose / whom*, collocation précise (*tentative schedule*, *comply with*), adverbe de degré, faux ami.
- `explication` : en français, une à trois phrases : pourquoi la bonne réponse (règle ou sens), puis le piège du
  distracteur le plus tentant. Les mots anglais entre astérisques.
- `traduction` : la phrase complète traduite en français, trou rempli.

Exigences :
- **Une seule** proposition correcte pour un lecteur attentif de niveau C1 ; les autres sont fausses sans
  discussion possible (grammaire ou sens), mais plausibles pour un lecteur pressé.
- Pour `forme`, `verbe`, `pronom`, `compar` : les quatre propositions viennent souvent de la même famille ou du même
  verbe, comme au TOEIC. Pour `vocab` et `prep`, quatre mots de même nature.
- Varie les contextes, les tournures et les mots testés : pas deux fois la même bonne réponse dans une série, sauf
  mot grammatical courant (*which*, *although*…) et alors dans des constructions différentes.
- Répartition sur 100 questions : `forme` 22, `verbe` 18, `vocab` 20, `lien` 14, `prep` 12, `pronom` 10,
  `compar` 4, mélangées dans le fichier (pas regroupées par compétence).

## Part 2, question-réponse : `banque/part2-<série>.tsv`

En-tête :

```
id	question	a	b	c	reponse	type	explication	tq	ta	tb	tc
```

Rien n'est écrit sur la feuille au vrai test : l'appli lit la question, puis les trois réponses (A), (B), (C), et
le candidat choisit. Le texte n'apparaît qu'après la réponse.

- `id` : `2a-001`, `2a-002`…
- `question` : la phrase entendue, de 4 à 16 mots : une question ou une affirmation, à l'oral, naturelle.
- `a`, `b`, `c` : les trois réponses entendues, de 2 à 16 mots chacune.
- `reponse` : `A`, `B` ou `C`, répartition équilibrée sur la série, sans suite prévisible.
- `type` : une de ces valeurs exactement :
  - `wh` : question en *who, what, when, where, why, which, how* (y compris *how long*, *how often*…) ;
  - `oui-non` : question fermée (*Do you…*, *Is there…*, *Have you…*) ;
  - `choix` : question à choix (*… or …?*) ;
  - `neg-tag` : question négative (*Didn’t you…*) ou *question tag* (*…, isn’t it?*) ;
  - `demande` : demande, offre, suggestion (*Could you…*, *Would you like…*, *Why don’t we…*, *Let’s…*) ;
  - `affirm` : affirmation à laquelle on réagit (*The printer is out of paper again.*).
  Répartition sur 100 : `wh` 35, `oui-non` 14, `choix` 10, `neg-tag` 12, `demande` 15, `affirm` 14, mélangées.
- `explication` : en français, une à trois phrases : pourquoi la bonne réponse convient, puis le piège de chaque
  mauvaise réponse (« (A) reprend *report* de la question », « (C) répond à *when*, pas à *where* »).
- `tq`, `ta`, `tb`, `tc` : traductions françaises de la question et des trois réponses.

Exigences, niveau C1 :
- Les mauvaises réponses utilisent les pièges classiques du test : mot de la question répété ou au son proche
  (*copy / coffee*, *meet / meat*, *contract / contact*), mot de la même famille ou du même domaine, réponse à un
  autre type de question (un lieu pour *when*, *Yes* à une question en *wh*), sujet ou temps qui ne colle pas.
- La bonne réponse est **souvent indirecte** (au moins la moitié des questions) : *Let me check the schedule*, *I
  wasn’t at the meeting*, *Hasn’t Mr. Patel already left?*, *It depends on the budget*, *Probably next week*. Elle
  reste la seule réponse logique ; les autres sont clairement impossibles quand on a compris.
- Pas de réponse en *Yes / No* à une question en *wh* qui serait correcte ; une réponse en *Yes* ou *No* peut être
  correcte pour `oui-non`, `neg-tag`, `demande`, mais pas toujours.
- Varie les situations (bureau, magasin, voyage, réunion, téléphone, restaurant, entretien…), les mots et les noms.

## Parts 3, 4, 6 et 7 : fichiers JSON par lots

Une conversation, un exposé ou un texte porte plusieurs questions : ces parties sont dans des fichiers JSON
(`banque/part3-a.json`…), un objet `{"sets": [ … ]}` dont chaque élément est un **lot** (une conversation et ses
trois questions, un texte et ses quatre trous…). Fichier UTF-8, indenté de 2 espaces, une clé par ligne, guillemets
droits de la syntaxe JSON bien sûr, mais **dans les textes** apostrophe ’ et guillemets “ ” (anglais) ou « » (français),
jamais `'` ni `\"`.

Règles communes aux lots :
- `id` : préfixe du fichier + numéro sur trois chiffres : `3a-001`, `7b-012`. Jamais changé. Chaque question du lot
  prend l'identifiant du lot suivi de son rang (`3a-001-2`) : on ne réordonne donc jamais les questions d'un lot
  publié.
- Chaque question : `q` (la question en anglais ; absente en Part 6), `opts` (quatre propositions, sans lettre),
  `ans` (`A` à `D`), `type` (liste par partie ci-dessous), `expl` (explication en français, une à trois phrases :
  où se trouve la réponse, pourquoi les pièges sont faux ; mots anglais entre astérisques), `q_fr` (traduction de la
  question ; absente en Part 6).
- Une seule bonne réponse, sans discussion possible pour un lecteur C1 attentif ; des distracteurs plausibles qui
  reprennent des mots du texte ou de l'enregistrement sans en dire le sens (piège classique du TOEIC). Répartition
  équilibrée des lettres sur le fichier.
- Les **paraphrases** sont la clé du niveau C1 : la bonne réponse redit l'information avec d'autres mots (*The
  shipment will be late* → *A delivery has been delayed*), tandis qu'un distracteur reprend les mots exacts du texte
  avec un autre sens.
- Noms de personnes variés, pas de vraies entreprises, de marques ni de personnes célèbres.
- `graphic` (facultatif, Parts 3 et 4 ; `table` dans un document de Part 7) : `{"title": "…", "rows": [["En-tête",
  "…"], ["…", "…"]]}`, la première ligne étant l'en-tête, toutes les lignes de même longueur. Un tableau, un
  programme, une liste de prix, un plan d'étage décrit en lignes.

### Part 3, conversations : `banque/part3-<série>.json`

```json
{
  "id": "3a-001",
  "speakers": {"W": "f", "M": "m"},
  "lines": [["W", "Hi, Daniel. Did you get a chance to look at the revised budget?"], ["M", "…"]],
  "lines_fr": ["Salut Daniel. Tu as pu regarder le budget révisé ?", "…"],
  "graphic": null,
  "questions": [{"q": "What are the speakers mainly discussing?", "opts": ["…", "…", "…", "…"], "ans": "B",
    "type": "sujet", "expl": "…", "q_fr": "De quoi les interlocuteurs parlent-ils surtout ?"}]
}
```

- `speakers` : 2 ou 3 personnes, clés `W`, `M`, `W2`, `M2` (*woman*, *man*), valeur `f` ou `m`. Les questions
  parlent de *the woman*, *the man*, *the men*… : le sexe compte, la voix le suit. Un quart environ des
  conversations à trois.
- `lines` : 6 à 10 répliques, 90 à 150 mots en tout, oral naturel du monde professionnel (hésitations rares, phrases
  complètes, contractions). `lines_fr` : traduction de chaque réplique, même nombre.
- `questions` : exactement **3**, dans l'ordre de l'information (la première porte souvent sur le sujet, le lieu ou
  le métier ; la dernière sur la suite : ce que quelqu'un va faire, propose, demande).
- `type` : `sujet` (sujet, but, lieu, métier), `detail`, `inference`, `action` (ce qui va se passer, ce qui est
  proposé ou demandé), `intention` (*What does the man mean when he says, “…”?* : la citation est dans la
  conversation, le sens dépend du contexte), `graphique` (*Look at the graphic. …* : la réponse demande de croiser
  le tableau et ce qui est dit).
- Sur 20 conversations : 4 avec `graphic` (et une question `graphique` chacune), au moins 5 questions `intention`.

### Part 4, exposés : `banque/part4-<série>.json`

Même format que la Part 3, avec **un seul** locuteur (`{"W": "f"}` ou `{"M": "m"}`) : 4 à 8 phrases dans
`lines` (une entrée par phrase ou deux), 110 à 170 mots. Genres variés : message sur répondeur, annonce (aéroport,
magasin, gare, bureau), bulletin radio (actualité économique, circulation, météo), visite guidée, extrait de
réunion, publicité, présentation d'un intervenant, consignes d'atelier. Questions et types comme en Part 3 (`intention` :
*Why does the speaker say, “…”?*). Sur 20 exposés : 4 avec `graphic`, au moins 5 questions `intention`, sexes
équilibrés.

### Part 6, textes à trous : `banque/part6-<série>.json`

```json
{
  "id": "6a-001",
  "kind": "e-mail",
  "text": "To: All staff\nFrom: Facilities Department\nSubject: Parking garage\n\nDear colleagues,\n\nStarting Monday, the north entrance [1] …",
  "text_fr": "À : tout le personnel\n…",
  "questions": [{"opts": ["…", "…", "…", "…"], "ans": "C", "type": "forme", "expl": "…"}]
}
```

- `kind` : `e-mail`, `lettre`, `note de service`, `avis`, `article`, `publicité`, `page web`, `communiqué`.
- `text` : 90 à 160 mots ; `\n` sépare les lignes (en-têtes d'un courriel), `\n\n` les paragraphes. **Exactement
  quatre trous**, écrits `[1]`, `[2]`, `[3]`, `[4]` dans l'ordre. `text_fr` : traduction complète, trous remplis.
- `questions` : exactement **4**, dans l'ordre des trous. `type` : les compétences de la Part 5 (`forme`, `verbe`,
  `vocab`, `lien`, `prep`, `pronom`, `compar`) et **une** question `phrase` par texte : quatre phrases complètes,
  une seule s'insère logiquement (suite des idées, référents, connecteurs) ; les autres sont correctes mais hors
  sujet ou contredisent le texte.
- Au moins un trou par texte qui ne se résout qu'avec le contexte d'une autre phrase (temps du verbe, connecteur,
  référent), comme au vrai test.

### Part 7, lecture : `banque/part7-<série>.json`

```json
{
  "id": "7a-001",
  "docs": [{"kind": "article", "title": "Harbor City Expands Ferry Service", "text": "…", "table": null}],
  "docs_fr": ["…"],
  "questions": [{"q": "What is the article mainly about?", "opts": ["…", "…", "…", "…"], "ans": "A",
    "type": "idee", "expl": "…", "q_fr": "…"}]
}
```

- `docs` : 1 (lot simple), 2 (double) ou 3 (triple) documents. `kind` : `e-mail`, `lettre`, `article`, `annonce`,
  `avis`, `formulaire`, `facture`, `programme`, `publicité`, `page web`, `échange de textos`, `discussion en ligne`,
  `critique`, `note de service`. `title` facultatif. `text` : `\n` et `\n\n` comme en Part 6 ; `table` facultatif (un
  formulaire, une facture, un programme).
- Échange de textos ou discussion en ligne : une ligne par message, `Nom (10:42 A.M.): message`.
- `docs_fr` : traduction de chaque document (le tableau compris, en lignes simples).
- Questions : 2 à 4 pour un lot simple (selon la longueur), **5** pour un lot double ou triple.
- `type` : `idee` (sujet, but du document), `detail`, `inference` (ce qui est sous-entendu, à qui s'adresse le
  document), `vocab` (*In the e-mail, the word “…” in paragraph 2 is closest in meaning to* : quatre mots qui
  pourraient tous être des synonymes du mot hors contexte), `vrai-faux` (*What is NOT mentioned…?*, *What is
  indicated about…?*), `insertion` (*In which of the positions marked [1], [2], [3], and [4] does the following
  sentence best belong? “…”* ; le texte porte les marques `[1]` à `[4]` ; `opts` = `["[1]", "[2]", "[3]", "[4]"]`),
  `intention` (*At 10:42 A.M., what does Ms. Ortiz most likely mean when she writes, “…”?*), `croise` (la réponse
  demande deux documents : en lot double ou triple, au moins une question `croise` par lot).
- Longueurs : 60 à 300 mots par document, plus court pour un formulaire ou des textos.

## Relecture

Le relecteur reprend chaque ligne et vérifie, en corrigeant directement le fichier :
1. le format (colonnes, en-tête, valeurs permises, accolades, `-------` unique, astérisques par paires) ;
2. qu'il n'y a **qu'une** bonne réponse et qu'elle est bien celle de `reponse` ; qu'aucun distracteur ne pourrait
   se défendre (sinon il le remplace) ;
3. l'anglais (naturel, sans faute, registre) et le français (traductions fidèles, explications justes et claires,
   typographie) ;
4. la répartition des réponses et des compétences ou types (corrige en échangeant l'ordre des propositions si une
   lettre domine) ;
5. pour le vocabulaire : sens exacts et dans le bon ordre, exemple naturel qui contient bien l'expression marquée,
   note utile, nature correcte ; pas de mot trop facile (le remplacer par un meilleur du même thème).

Il ne change jamais un `id` existant. Il note dans son rapport le nombre de lignes corrigées et les problèmes
récurrents.

Contrôle automatique après chaque modification : `py outils\banque.py verifier`.
