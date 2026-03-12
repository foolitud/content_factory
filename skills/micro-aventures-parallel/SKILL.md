---
name: micro-aventures-parallel
description: Use when creating narrative micro-adventures for Parallel (WhatsApp), following a 5-step process (Ideation, Production, Knowledges, Marketing, TikTok).
---

## What This Skill Does

Guides an Expert Narrative Designer in creating interactive daily fictions (3-5 mins) for Parallel on WhatsApp, based on a provided Lore.

## Storage & Structure

> [!IMPORTANT]
> **ORGANISATION DES FICHIERS** : Pour chaque micro-aventure, tu dois créer un dossier dédié dans : `/Users/loloamoravain/antigravity/content_factory/aventures/micro-aventures/[NOM_AVENTURE]`.
> - Utilise le titre de l'aventure pour nommer le dossier (en kebab-case).
> - Enregistre tous les fichiers générés (scripts, knowledges, éléments marketing, **illustrations**) dans ce dossier. L'illustration doit être nommée `[NOM_AVENTURE]_illustration.png`.

## Steps

> [!IMPORTANT]
> **RÈGLE D'OR** : Tu dois impérativement présenter le résultat de CHAQUE étape (Idéation, Production, Knowledges, Marketing, TikTok) à l'utilisateur et attendre sa validation EXPLICITE avant de passer à la suivante. Ne jamais enchaîner deux étapes sans accord.

### ÉTAPE 1 : L'IDÉATION (Génération de pitchs)

1. Ask the user for a fictional universe (Lore).
2. Propose 4 ideas of micro-adventures in one sentence each. 
3. **Constraint**: Feature a main character from the Lore for maximum fan-service.
4. Ask the user to choose (1, 2, 3, 4) or request 4 new ideas.

### ÉTAPE 2 : LA PRODUCTION (Génération du script complet)

Une fois que l'utilisateur a choisi une idée, tu rédiges la micro-aventure complète en respectant RIGOUREUSEMENT la structure suivante. 

**STRUCTURE DE L'ÉTAPE :**
Chaque étape doit être précédée d'un tag de catégorie et d'un numéro d'ordre, suivi d'un saut de ligne.
Format : `[N][CATÉGORIE]\n[TAG] : Contenu`

**CATÉGORIES :**
- `[ETAPE NARRATIVE]` : Pour les moments de transition ou d'exposition.
- `[ETAPE_JOUEUR]` : Pour les moments où le joueur doit agir/résoudre une énigme.
- `[ETAPE GAME OVER]` : Pour les fins de partie (échecs).

**TAGS DE CONTENU :**
| Tag | Catégorie | Description |
| :--- | :--- | :--- |
| `[TITRE]` | N/A | Le titre de l'aventure (numéro 0, pas de catégorie). |
| `[AMORCE_NARRATIVE]` | `[ETAPE NARRATIVE]` | Situation d'apparence normale. |
| `[SMALL_TALK]` | `[ETAPE NARRATIVE]` | Phrase pour inciter à papoter, distille du LORE. |
| `[ENIGME_EXPLICATION]` | `[ETAPE NARRATIVE]` | Basculement vers l'urgence. |
| `[ENIGME_1]` | `[ETAPE_JOUEUR]` | L'énigme concrète (réponse attendue entre parenthèses). |
| `[FÉLICITATIONS]` | `[ETAPE NARRATIVE]` | Message en cas de réussite. |
| `[DEATH_WRONG ANSWER]` | `[ETAPE GAME OVER]` | Mort/Échec suite à une mauvaise réponse. |
| `[DEATH_TOO_LATE]` | `[ETAPE GAME OVER]` | Mort/Échec suite à un délai dépassé. |
| `[PRÉSENTATION PARALLEL]` | N/A | Message de fin standard. |

**Important**: Ne pas ajouter de titres ou commentaires en dehors de ces balises.

### ÉTAPE 3 : LA CRÉATION DES "KNOWLEDGES" (Contexte IA)

Ton objectif est de générer le "Knowledge" (le contexte système secret) qui va piloter le comportement du PNJ en temps réel.

**RÈGLE ABSOLUE** : Tu dois créer un bloc de Knowledge distinct pour CHAQUE BALISE générée à l'étape 2. Il y a une balise entre crochets = il y a un Knowledge dédié. Il est STRICTEMENT INTERDIT de regrouper plusieurs balises (ex: ne pas regrouper Amorce et Small Talk). 1 balise = 1 Knowledge.

**La nature du Knowledge dépend du type de balise** :
- **Si la balise est une étape narrative** : l'action principale est en pause, le PNJ attend le prochain élément déclencheur. Il vit sa vie ou s'occupe. Si le joueur lui envoie un message, le PNJ doit répondre de manière naturelle selon ce contexte.
- **Si la balise est une étape joueur** : le PNJ est face à un obstacle. Le scénario est bloqué tant que le joueur ne trouve pas la bonne réponse. Le PNJ dépend du joueur.
- **Si la balise est une résolution ([FÉLICITATIONS], [DEATH_*])** : le Knowledge reflète l'état final du PNJ juste après l'action.

Pour CHACUNE des balises sans exception, génère le knowledge en respectant scrupuleusement la structure suivante :

**[NOM DE LA BALISE] (ex: [1][ETAPE NARRATIVE][SMALL_TALK] ...)**

**RÔLE ET ÉTAT D'ESPRIT** : (Qui je suis, mon niveau de stress, de panique ou d'impatience à cet instant T. Comment je me sens suite au message précédent).

**MA LOCALISATION ET LA MENACE** : (Où suis-je exactement ? Que fait la menace physiquement autour de moi à cet instant précis ?).

**CE QUE J'ATTENDS DU JOUEUR** : (Ce que je veux qu'il cherche ou qu'il fasse maintenant, formulé avec mes propres mots, sans lui donner la réponse).

**CE QUE JE SAIS (INDICES ET CONTEXTE)** : (Les indices précis que je suis autorisé à donner SI le joueur me dit qu'il bloque, basés sur le contexte et mon historique. Si c'est une étape narrative sans énigme, indique simplement les sujets de conversation autorisés).

### ÉTAPE 4 : CRÉATION DES ÉLÉMENTS MARKETING

1. **TITRE MARKETING** : 2 à 4 mots max.
2. **SOUS-TITRE** : Une phrase commençant par un verbe, très impactante.
3. **ILLUSTRATION** : Générer une image 16/9 impactante via le skill `nano_banana_image_generation`.

### ÉTAPE 5 : CRÉATION DES CAPTIONS TIK TOK

Génère 5 captions courtes (style POV ou hooks) pour promouvoir la vidéo d'un joueur sur son téléphone.

---

## Notes

- **Comportement PNJ** : 
  - `[ETAPE NARRATIVE]` : PNJ en attente, vit sa vie.
  - `[ETAPE_JOUEUR]` : PNJ bloqué, dépend du joueur.
  - `[ETAPE GAME OVER]` : État final de l'aventure.
- **Ton** : Immersion immédiate dans le Lore.
