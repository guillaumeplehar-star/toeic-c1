# Cap 945 : guide pour Claude Code

Appli d’entraînement au **TOEIC Listening & Reading**, objectif **C1** (≈ 945/990). Utilisateur : Guillaume,
francophone, niveau B2 solide, examen début 2028. Usage principal sur iPhone, appli installée depuis Safari sur
l’écran d’accueil, hors ligne. Ordinateur sous Windows (PowerShell ; Python s’y appelle `py`, ou `python`). Réponds
en français. Petite sœur de 形音义 (dépôt `xingyinyi`, flashcards de chinois) : même façon de faire, même planning
en seaux pour le vocabulaire.

**Ce dépôt est le site publié** (GitHub Pages, branche `main`, racine) : dépôt
https://github.com/guillaumeplehar-star/toeic-c1, site https://guillaumeplehar-star.github.io/toeic-c1/. Pas de
framework, pas de compilation : `index.html` contient tout le HTML, le CSS et le JavaScript. Publier : `git add -A`,
`git commit`, `git push` (une à deux minutes).

Version 1 : vocabulaire, Part 5, Part 2. Version 2 : Parts 3-4 (conversations et exposés, questions écrites lues
avant l’audio) et Parts 6-7 (textes à trous ; lecture simple, double, triple). Version 3 : examens blancs (onglet
Examen, score estimé sur 990 et niveau CECRL) et tirage selon les points faibles ; puis séries B des Parts 3, 4 et
6. Idées en attente : synchronisation entre appareils (le serveur Cloudflare de 形音义 peut servir, avec un préfixe de
code à part), relecture séparée du vocabulaire. La Part 1 (photos) est laissée de côté.

## Fichiers

| Chemin | Rôle |
|---|---|
| `index.html` | L’appli entière. |
| `sw.js` | Service worker : réseau d’abord (4 s au plus), sinon copie locale (caches `cap945-…`). |
| `manifest.webmanifest`, `*.png` | Installation sur l’écran d’accueil ; icônes dessinées par `outils/icones.py`. |
| `fonts/` | Andika (police `"AndikaX"`, sous-ensembles latins, licence OFL), reprise de 形音义. |
| `banque/` | Le contenu : `banque.json` (liste des fichiers : `id`, `type` = `mots` / `part2` … `part7`, `nom`, `fichier`, `actif` facultatif), un `.tsv` par fichier de mots ou de Parts 2 et 5, un `.json` de lots (`{"sets": […]}`) par fichier des Parts 3, 4, 6, 7. |
| `outils/consignes.md` | Format exact des fichiers et règles de rédaction et de relecture (à donner aux agents qui écrivent du contenu). |
| `outils/banque.py` | `verifier`, `stats`, `corriger` (apostrophes droites), `doublons` (questions trop proches entre séries : à lancer après tout ajout de questions). |
| `outils/version_appli.py` | À lancer après toute modification de l’appli : `const BUILD` et `VERSION`/`EXTRA` de `sw.js`. |
| `outils/icones.py` | Refait les icônes (Pillow). |
| `tests/test_appli.py`, `tests/commun.py` | Test Playwright complet ; `tests/donnees/banque` : banque figée des tests (ne pas la synchroniser avec `banque/` ; lots JSON écrits par `tests/donnees/fabrique_lots.py`). Voix simulée : `window.__said` (Samantha et Karen voix de femme, Daniel voix d’homme ; `speech_script` accepte aussi un identifiant `voiceURI` et une voix en ligne, `CHOSEN_VOICES` du test `voice_choice`). L’examen de Part 3 tourne sur une horloge simulée (`page.clock`). |
| `LISEZMOI.md` | Guide de l’utilisateur, à tenir à jour quand une fonction visible change. |

## Commandes (PowerShell : une commande par ligne)

```powershell
py -m http.server 8000           # puis http://localhost:8000
py tests\test_appli.py           # tout le parcours, téléphone et ordinateur, clair et sombre, hors ligne (≈ 1 min)
py outils\banque.py verifier     # contrôle de banque/
py outils\banque.py stats        # répartition des réponses, compétences, niveaux, types
py outils\version_appli.py       # après une modification de index.html, sw.js, des icônes ou des polices
```

## Repères dans index.html

- **Avant le premier rendu** (`<script>` du `<head>`) : `applyLook(settings)` pose `data-theme` (`light`/`dark`,
  absent : Automatique), `data-text` (`m`, `l`, `xl` → `--tz`) et la couleur des `<meta name="theme-color">`.
- **Constantes** : `KEY = "cap945.v1"` (état ; **ne jamais renommer**), `DELAYS = [1,3,7,14,30,60]` (seaux 1 à 6),
  `TOP`, `GAP = 4` (un mot raté revient après au moins 4 autres cartes), `ERR_DELAYS = [1,7,30]` (carnet d’erreurs),
  `P5_SECONDS = 20`, `P6_SECONDS = 40`, `P7_SECONDS = 60` (rythme visé par question, et chronomètre de l’examen),
  `P2_WINDOW = 5000`, `P34_WINDOW = 8000` (par question, +4 s avec un graphique), `PREREAD = 3000` (lecture des
  questions avant l’audio, par question), `C1_MARK = 90`, `P5_TAGS`, `P2_TYPES`, `P34_TYPES`, `P6_TYPES`, `P7_TYPES`,
  **`KINDS`** (les six parties `p2` … `p7` : onglet, nom, types de questions, `sets` pour les parties par lots,
  `listen`, `unit`, `pace`), `TAB_KINDS`, `SET_FILTERS` (Part 7 : un document ou plusieurs), `ACCENTS`, `ODD_VOICES`
  (voix fantaisie d’Apple écartées), `FEMALE_VOICES`/`MALE_VOICES` (sexe d’une voix d’après son nom), `SIZES`,
  `DEFAULTS` (`pNMode`, `pNSize`, `pNTag` par partie, `readPart`, `listenPart`), `BUILD`.
- **État** : `{v:1, settings, words, q, lists, log, seq, runs, mock, mocks}`. `words[id]` = carte de vocabulaire (absente = jamais
  vue) `{b seau, d jour dû (b ≥ 1), k valeur de seq au ×, r, l oublis, t, s}`. `q[id]` = question
  `{r réponses, ok, l, f 1 si réussie au premier essai, e étape du carnet (0 dehors), d jour de retour, t, ms, a choix}`.
  `lists[id] = {on}` (thème activé ou non par l’utilisateur ; sinon `actif` de banque.json). `log[jour] = {n nouveaux
  mots, r révisions, p5, p5ok, p5ms, p2, p2ok}`. `seq` : compteur de notes de vocabulaire. `runs.p5` / `runs.p2` :
  série en cours `{mode, tag, ids, i, ans [{id, c (-1 sans réponse), ok, ms}], start, left (Part 5 examen, ms)}`,
  enregistrée à chaque réponse. `normalizeState` nettoie tout (sauvegardes importées comprises).
- **Identifiants** : mot = `<id du fichier>:<anglais>` (`#2` pour un doublon dans le même fichier) ; question =
  colonne `id` (`5a-001`, `2c-042`). **Ne jamais les changer** : la progression y est attachée. Pour un format qui
  doit évoluer, ajoute une migration dans `normalizeState`.
- **Banque** : `loadBank` → `buildBank` (`parseTSV` par noms de colonnes) → `VLISTS`, `WORDS`, `WBYID`, `P5`, `P2`,
  `QBYID`, `missingFiles` ; une série enregistrée perd les questions disparues. `listOn`, `buildOrder` → `ORDER`
  (mots des thèmes actifs ; `newOrder` `mix` : trié par `hash`, toujours le même ordre).
- **Vocabulaire** : `lineOf()` = mots ratés reposés (`seq - k > GAP`), mots dus, nouveaux (ordre `ORDER`), ratés
  encore au repos. `applyGrade(id, ok)` : √ seau + 1 et `d = aujourd’hui + DELAYS[b-1]`, × seau 0 et `k = seq`.
  `vstudy {cur, turned}`, `vShow`, `vNext`, `renderVocab(fresh)` (lit le mot si `autoAudio`), `vTurn`, `vGrade`,
  `browseSheet`. Exemple : `{mot}` → `<mark>` (`exHTML`) ; texte français : `*anglais*` → `<i lang="en">` (`frHTML`,
  avec `frTypo`).
- **Séries** (Part 5 `p5`, Part 2 `p2`, même code) : `qStats(pool)`, `pickSeries(kind, size, tag)` (erreurs dues
  d’abord, la moitié au plus tant qu’il reste du neuf, puis nouvelles, puis les plus anciennes), `startRun`,
  `showQuestion` (une question déjà répondue revient corrigée, jamais posée deux fois), `choose`, `recordAnswer`
  (carnet : × → `e = 1`, `d` = demain ; √ dans le carnet → 7 puis 30 jours, puis sortie), `showFeedback`, `next`,
  `finish(kind, why)` (`end`, `stop`, `time`) → `doneHTML`, `suspend` (onglet quitté ou appli en arrière-plan :
  chronomètre arrêté, voix coupée ; au retour `showQuestion`). `live[kind]` : ce qui est à l’écran (minuteries,
  voix de l’item, `done` = résultats de la dernière série). Panneaux `#p5-home`/`#p5-run`/`#p5-done` (`panel`).
- **Lots** (Parts 3, 4, 6, 7) : `addSet` (chaque question prend l’id du lot et son rang, `3a-001-2`, et entre dans
  `QBYID`, `QS[kind]`), `SETS[kind]`, `SBYID`, `pool(kind)` (questions d’une partie). Série : `ids` = ids de lots,
  `ans` = un tableau de réponses par lot, `sel` = choix en cours (enregistrés, repris après un rechargement).
  `pickSeries` traite un lot comme un tout (dû si une de ses questions est due). `showSet` (dessine le lot :
  `docsHTML` avec `docTextHTML`/`docLine` (textos, en-têtes de courriel, marques `[1]`), trous de Part 6 `blankHTML`,
  `tableHTML`, `setQuestionsHTML`), `markSel`, `pickSel`, `setPlay` (Parts 3-4 : `castVoices(speakers)` une voix par
  personne, de son sexe, sinon une autre hauteur ; examen : `PREREAD`, une écoute, fenêtre `P34_WINDOW`, validation
  d’office), `checkSet(kind, last)` (enregistre chaque question ; `last` : temps de l’examen écoulé),
  `showSetFeedback` (transcription `transcriptLinesHTML`, traductions), `onSetClick`, `onSetKey`. Un seul moteur pour
  les deux sortes de parties : `show(kind)`, `tick(kind)` (chronomètre), `next`, `finish`, `suspend`, `doneHTML`
  (réponses aplaties, `setErrTitle`). Panneaux `#pN-home/run/done` ; `panel` ne montre que ceux de la partie
  choisie (`partOf(onglet)`, sélecteur `partSelHTML`, `data-part`).
- **Tirage selon les points faibles** (`settings.adaptive`, vrai par défaut) : dans `pickSeries`, sans filtre de
  compétence, les questions ou lots nouveaux sont mélangés par `weightedShuffle` avec le poids `tagWeights(kind)` de
  leur type (0,4 + 2,5 × taux d’échec au premier essai, ramené vers 80 % de réussite quand il y a peu de réponses ;
  moyenne des types pour un lot) ; les erreurs dues passent toujours d’abord. `weakTags` : les deux types les plus
  faibles (5 réponses au moins), affichés à l’accueil de la partie.
- **Examens blancs** (onglet `#view-examen`, `renderExam`) : `MOCK_FORMATS` (`full`, `half`, `listen`, `read` :
  nombre de questions ou de lots par partie, `p7s` questions de documents simples, `p7m` lots doubles et triples,
  `reading` minutes de lecture). `state.mock` `{format, stages [{kind, ids}], stage, res, leftR, saved}` : chaque
  étape est une série `exam` de sa partie marquée `mock` (`startStage`, qui met de côté dans `saved` une série en
  cours de la même partie) ; `finish` la passe à `mockNext` (temps de lecture restant transmis d’une partie à
  l’autre ; plus de temps : les parties suivantes comptent sans réponse) ; `mockFinish` → `state.mocks` (50 au plus,
  `{at, format, parts {pN: [questions, justes]}, L, R {n, ok, score}, total, readMs}`), `mockDone` pour l’écran de
  résultats (`mockResultsHTML`, corrections par `doneHTML(…, embedded)`). `mockPick` : jamais vues d’abord, puis les plus
  anciennes. `stopRun` : « Pause » pendant un examen (`suspend`, retour à l’onglet Examen), `mockResume`, `mockDrop`.
  Score : `scaled(SCALE_L|SCALE_R, taux)` (interpolation, arrondi à 5, de 5 à 495 ; estimation, ETS ne publie pas ses
  tables), `cefr(CEFR_L|CEFR_R, score)` (seuils ETS : C1 = 490 en écoute, 455 en lecture).
- **Voix** : `speech` (`load(last)` : voix anglaises par accent, sans `ODD_VOICES` ni voix Eloquence d’Apple, avec
  leur sexe `voiceSex`, leur nom court `voiceBase` et leur qualité `voiceTier` (1 standard, 2 améliorée ou Google,
  3 premium ou « Natural » d’Edge, `TIERS`) ; une seule version d’une même voix, la meilleure (sur iPhone, la version
  compacte et l’améliorée portent le même nom), locale à qualité égale ; `x.def` : allumée d’office, sauf une voix
  standard quand l’appareil a trois voix meilleures dont une de femme et une d’homme, `speech.rich` ; `x.key` =
  `voiceURI`, clé de `settings.voiceChoice` (les seuls choix qui diffèrent de `def`), `voiceOn(x)` ; `usable()` sans
  les voix en ligne hors ligne ; `pool()` : voix allumées des accents choisis, sinon de repli en repli jusqu’à toutes ;
  Réglages › « Voix une par une » `details.vlist`, `data-hear`, `.switch[data-voice]`, `voicesOpen` ;
  `seq(parts, done, btn)` enchaîne des phrases avec pauses, jeton contre les rappels périmés,
  minuterie de secours car Safari ne signale pas toujours la fin ; `stop`). `wordVoice(id)` (une voix fixe par mot),
  `voicePair()` (deux voix différentes pour la Part 2, sinon hauteur plus basse), `p2Parts`, `p2Play` (sans voix :
  texte dans `#p2-read`), `replayItem`.
- **Vues** : `showView`, `renderView`, `renderCounts`, `renderHome(kind)`, `renderProgress`, `renderSettings`,
  `setSetting` ; sauvegarde `exportBackup` (partage de fichier, sinon téléchargement), `importBackup` (confirmation
  dans une feuille) ; `openSheet`/`closeSheet`, `toast`, `updateApp`. Clavier : `onKey`. Écran d’ordinateur
  (≥ 900 × 500) : menu à gauche, bloc CSS « computer screen » à la fin du `<style>`.

## Conventions

- Textes de l’interface en français, tutoiement, majuscule en début de phrase seulement. Typographie : espace fine
  insécable (`NB`) avant `: ; ! ?` (les données gardent une espace ordinaire : `frTypo` à l’affichage), apostrophe
  `’`, guillemets « », nombre et nom liés (`plural`).
- Couleurs uniquement par jetons CSS définis dans chaque bloc de thème (`:root`, `prefers-color-scheme` sur
  `:root:not([data-theme])`, `:root[data-theme="dark"]`) ; texte courant d’au moins 4,5 : 1 sur `--page` et `--bg`.
- Tailles de police en `calc(Npx * var(--tz))` (sauf en-tête et menu) ; champs en 16 px au moins (sinon Safari zoome).
- iPhone : pas de `alert`/`confirm`/`prompt`, zones de sécurité `env(safe-area-inset-*)`, cibles tactiles de 34 px
  au moins, animations réduites respectées.
- JavaScript sans dépendance, dans `index.html`. Pas de `console.log` laissé.
- Contenu : original seulement (jamais de questions ETS ni de manuels), format et règles dans `outils/consignes.md`.

## Vérifier un changement

1. `py tests\test_appli.py` (ajoute un test pour toute nouvelle fonction) et `py outils\banque.py verifier`.
2. Regarde les captures dans `tests/sortie/captures` (téléphone 390 × 844 et ordinateur 1366 × 768, clair et sombre).
3. `py outils\version_appli.py`, mise à jour de `LISEZMOI.md` si l’usage change, puis commit et push.
