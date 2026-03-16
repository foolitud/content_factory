# Content Factory 🤖

Bienvenue dans le dépôt de la **Content Factory**. Ce projet est une usine à contenus automatisée conçue pour générer des scripts, des assets marketing et des vidéos (TikTok/Reels) en utilisant la puissance de l'IA et de workflows modulaires appelés "Skills".

## 🚀 Architecture du Projet

Le projet est organisé de manière modulaire :

- **`aventures/`** : Contient les scripts et les données des différentes aventures générées (par ex: *l-interrogatoire-croise*).
- **`.agents/skills/`** : Le cœur de l'usine. Chaque dossier est un "Skill" (compétence) spécifique :
    - `github` : Interaction avec GitHub via la CLI `gh`.
    - `video_generation` : Workflow pour générer des vidéos avec des modèles comme Kling ou Veo.
    - `micro-aventures-parallel` : Génération de récits interactifs.
    - `referral` : Systèmes de recommandation et de croissance.
- **`scripts/`** : Utilitaires et scripts Python pour la logique métier.
- **`prompts/`** : Modèles de prompts utilisés pour guider les LLMs.
- **`references/`** : Documentation de référence pour l'univers et le branding (ex: *Parallel Adventure*).
- **`videos/`** & **`images/`** : Dossiers de sortie pour les médias générés.

## 🛠 Installation & Configuration

1. **Prérequis** :
   - Python 3.10+
   - GitHub CLI (`gh`)
   - Un environnement virtuel (`.venv`)

2. **Configuration** :
   - Copiez `.env.example` vers `.env` et remplissez vos clés API.
   - Les identifiants Google doivent être placés dans `google_credentials.json` (ce fichier est ignoré par git pour votre sécurité).

## 🛡 Confidentialité & Sécurité

Ce projet est configuré pour ne **jamais** uploader de données sensibles grâce au fichier `.gitignore`. Sont exclus :
- Les fichiers `.env`
- Les fichiers de credentials JSON
- Les environnements virtuels localement installés

## 🐙 Utilisation de la CLI GitHub

Ce projet utilise massivement le skill `github`. Vous pouvez utiliser des commandes comme :
```bash
gh repo view     # Voir l'état du dépôt
gh issue list    # Lister les tickets en cours
```

---
*Généré avec ❤️ par la Content Factory.*
