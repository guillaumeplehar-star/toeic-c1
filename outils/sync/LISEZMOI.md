# Serveur de synchronisation

Cap 945 se synchronise par le serveur de 形音义 (https://xingyinyi-sync.guillaume-plehar.workers.dev, dépôt
`xingyinyi`, dossier `outils/sync`). Ce dossier en garde une **copie** pour les tests : `worker.mjs` (le Cloudflare
Worker) et `serveur_local.mjs` (le même avec `node:sqlite`, Node 22.13 ou plus). Toute modification du serveur se fait
d’abord dans le dépôt `xingyinyi`, puis se recopie ici.

Les deux applis ne se mélangent pas : la clé d’un code est l’empreinte SHA-256 de `"cap945:"` + ses lettres et chiffres
(`"xingyinyi:"` pour 形音义). Le serveur accepte `MAX_CODES` codes en tout (5 par défaut, réglable dans les variables du
Worker sur Cloudflare) : un code de Cap 945 en prend un.

```powershell
node outils\sync\serveur_local.mjs       # le serveur sur http://localhost:8787, pour essayer
py tests\test_sync.py                    # deux appareils et ce serveur
```
