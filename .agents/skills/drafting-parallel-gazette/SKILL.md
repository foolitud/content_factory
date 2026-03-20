---
name: drafting-parallel-gazette
description: Drafts the "Parallel Gazette" (community newsletter) in French. Includes a buffer system to collect news items throughout the month and a structured template (Intro, Menu, Music, News, Help, Gift, Discord).
---

# Parallel Gazette Drafting

## When to use this skill

- To add a snippet of news to the monthly newsletter buffer.
- To draft the full "Parallel Gazette" based on the accumulated buffer and current project context.
- To maintain the "Chill & Transparent" tone of Parallel Adventure.

## Triggers

- `/gazette` or `/newsletter`
- "Rédige la newsletter du mois"
- "Note ça pour la newsletter : [info]"
- "Ajoute à la gazette : [info]"

## Brand Context

Always respect the **Parallel Adventure DNA**:
- **Tone**: Chill & Transparent, professional but human, conversational, "low-ego".
- **Language**: French.
- **Goal**: Co-creation, building in public, sharing doubts and successes.

## Workflow 1: Adding to Buffer

When the user provides a snippet of information with a trigger like "Note ça pour la newsletter", perform the following:

1.  **Read the Buffer**: Check if `.agents/skills/drafting-parallel-gazette/resources/buffer.md` exists.
2.  **Append Information**: Add the new snippet with a timestamp and a bullet point.
3.  **Confirm**: Briefly confirm to the user that the information has been "mis au frais" (stashed).

## Workflow 2: Drafting the Gazette

When the user triggers the drafting process (e.g., `/gazette`):

1.  **Read the Buffer**: Fetch all items from `resources/buffer.md`.
2.  **Gather Context**: Check recent project updates (e.g., player counts, new hires, Studio progress) in the workspace.
3.  **Apply Template**: Use the following structure to draft the email.

### The Template (French)

```markdown
[Salutation amicale et décontractée, ex: "Allez, c'est parti !", "Et bonjour l'équipe !"]

[Petite intro sur l'humeur du moment ou un chiffre clé rapide.]

**Dans la gazette du jour, on va parler de :**
- [Item 1 du menu]
- [Item 2 du menu]
- ...

La lecture va durer [X] minutes. [Optionnel: phrase sur l'ambiance].
[Section Musique : "Je vous mets ma playlist/musique [Style] pour accompagner la lecture"].

---

[P.S. Discord : "Et si vous n'avez toujours pas rejoint notre Discord, c'est par ici."]

---

### [Titre de Section Libre 1 - Basé sur le Buffer]

[Contenu développé à partir des notes accumulées. Le ton doit rester conversationnel.]

### [Titre de Section Libre 2 - Basé sur le Buffer]

[... ainsi de suite pour chaque thématique identifiée dans le mois.]

---

### Vous pouvez nous aider !

Dans la rubrique petites annonces de ce mois-ci, la team Parallel recherche :
- [Demande 1]
- [Demande 2]
- ...
[Lien ou instruction pour répondre.]

---

### [Dernier appel à l'action ou info "chill"]

[Ex: "Lancez vos parties !", "On est à votre écoute sur le Discord".]

---

### Le cadeau, le cadeau, le cadeau

[Une curiosité numérique, un lien sympa, une pépite trouvée sur le web.]
[Explication courte de pourquoi c'est cool.]

[Signature décontractée]
```


## Heuristics & Tone

- **Emoji Usage**: Use emojis naturally to brighten the text (but don't overdo it).
- **Transparency**: If something is hard or a failure, say it.
- **Community**: Use "on", "nous", "ensemble".
- **Humanity**: Mention specific people (Nellya, etc.) when relevant.

## Resources

- **Buffer File**: `/Users/loloamoravain/antigravity/content_factory/.agents/skills/drafting-parallel-gazette/resources/buffer.md`
- **Examples**: `examples/newsletter_1.md`, `examples/newsletter_2.md`
