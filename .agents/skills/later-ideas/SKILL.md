---
name: later-ideas
description: Captures and develops content ideas based on the Parallel Adventure DNA and saves them to Notion.
---

# `later-ideas` Skill

Use this skill when the user wants to save a content idea for later.

## Triggers
- "Garde cette idée", "idée de contenu", "/later", "Je veux enregistrer cette idée".

## Context Extraction
1. **The Idea**: Identify the core concept or draft provided by the user.
2. **Social Network**: Extract the target platform (LinkedIn, YouTube, Instagram, TikTok, Threads, X). Default to "Général" if not specified.

## Logic Flow

1. **Alignment & Development**:
   - Read [parallel_adventure_dna.md](file:///Users/loloamoravain/antigravity/content_factory/references/parallel_adventure_dna.md).
   - Use the pillars (**Experience, Builder, Studio, Engine**) and the **Tone of Voice** (Chill, Transparent, Co-creation, Building in public) to expand the raw idea into 2-3 well-crafted sentences.
   - The goal is to make the idea sound like a "Parallel Adventure" project: interactive, community-driven, and transparent.

2. **Save to Notion**:
   - Target Database ID: `329b3024-3b8c-803e-8bbb-c9fa52094aff`
   - Use `notion-mcp-server_API-post-page` with:
     - `parent`: `{"database_id": "329b3024-3b8c-803e-8bbb-c9fa52094aff"}`
     - `properties`:
       - `Nom`: `{"title": [{"text": {"content": "<Short Title>"}}]}`
       - `Réseaux`: `{"select": {"name": "<Social Network Name>"}}`
     - `children`: An array with a paragraph block containing the developed idea.

3. **Confirmation**:
   - Briefly explain how the idea was developed (mentioning the DNA pillars used) and confirm it's saved in Notion (link to the database: `https://www.notion.so/329b30243b8c803e8bbbc9fa52094aff`).

## Failure Modes
- If the Notion API fails, save the developed idea in a new markdown file in `content_factory/ideas/` and notify the user.
