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
